import logging
import threading

from server import wev, config, flask_app, wev_ipc_handler

LOGGER = logging.getLogger(__name__)


def start():
    start_headless() if config.getboolean(
        "app", "headless"
    ) else start_with_head()


def do():
    LOGGER.info("Bootstrapping Services")
    # Add Services and Workers


def start_with_head():
    LOGGER.info("Running with Embedded Chrome")
    do()

    LOGGER.info("Spawning Server Thread")
    flask_thread = threading.Thread(target=flask_app.start, daemon=True)
    flask_thread.start()
    ipc_listener_thread = threading.Thread(
        target=wev_ipc_handler.start_listener, daemon=True
    )
    ipc_listener_thread.start()
    wev.start()


def start_headless():
    LOGGER.info("Running headless")
    do()
    flask_app.start()


if __name__ == "__main__":
    start()
