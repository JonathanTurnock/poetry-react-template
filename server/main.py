import logging
import sys
import threading
import time
from abc import ABC, abstractmethod
from os import path
from pathlib import Path

from PySide2.QtWidgets import QApplication
from flask import Flask
from flask import send_from_directory, jsonify
from flask_graphql import GraphQLView
from rx.subject import Subject

from server import config, ipc_handler, web_root, gql, health
from server.gui import SplashScreen, WebView

LOGGER = logging.getLogger("main")

app = Flask(__name__, root_path=web_root)
app.add_url_rule(
    "/api/graphql",
    view_func=GraphQLView.as_view("graphql", schema=gql.schema, graphiql=True),
)


@app.route("/")
def index():
    return send_from_directory(web_root, "index.html")


@app.route("/<file>")
def web(file):
    if path.exists(Path(web_root, file)):
        return send_from_directory(web_root, file)
    else:
        return index()


@app.route("/api/health", methods=["GET"])
def check_health():
    return jsonify(health.get_app_health())


def do():
    LOGGER.info("Bootstrapping Services")
    # Add Services and Workers


class Application(ABC):
    """
    Main Application Interface, exposes methods for starting and shutting down the application gracefully
    """

    shutdown_event = Subject()

    @abstractmethod
    def start(self):
        return NotImplemented

    @abstractmethod
    def shutdown(self):
        return NotImplemented

    @staticmethod
    def start_flask():
        app.run(
            host=config.get("flask", "bind_address"),
            port=config.getint("flask", "port"),
        )

    @staticmethod
    def get_app(headless=config.getboolean("app", "headless")):
        return HeadlessApplication() if headless else FullApplication()


class FullApplication(Application):
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._splash = SplashScreen()
        self._view = WebView()
        self._view.close_window_event.subscribe(self.shutdown)
        self._flask_thread = threading.Thread(
            target=FullApplication.start_flask, daemon=True
        )
        self._ipc_listener_thread = threading.Thread(
            target=ipc_handler.start_listener, daemon=True
        )
        self._exit_code = 0

    def start(self):
        LOGGER.info("Starting full application")
        self._splash.show()

        do()

        LOGGER.info("Spawning Flask server thread")
        self._flask_thread.start()

        LOGGER.info("Spawning IPC server thread")
        self._ipc_listener_thread.start()

        LOGGER.info("Showing window view & hiding splash screen")
        self._view.show()
        self._splash.hide()

        LOGGER.info("Starting main event loop")
        self._exit_code = self._app.exec_()

        LOGGER.info(
            f"Event loop closed with response {self._exit_code} setting exit code."
        )

    def shutdown(self, *args, **kwargs):
        LOGGER.info("Shutting Down")

        LOGGER.info("Broadcasting Shutdown event")
        FullApplication.shutdown_event.on_next(True)

        LOGGER.info("Quitting Application")
        self._app.quit()

        LOGGER.info(f"Exiting with Exit Code {self._exit_code}")
        sys.exit(self._exit_code)


class HeadlessApplication(Application):
    def start(self):
        LOGGER.info("Starting Headless Application")
        do()
        HeadlessApplication.start_flask()

    def shutdown(self):
        LOGGER.info("Shutting Down Application")
        HeadlessApplication.shutdown_event.on_next(True)
        time.sleep(1)
        sys.exit()


if __name__ == "__main__":
    application = Application.get_app()
    application.start()
