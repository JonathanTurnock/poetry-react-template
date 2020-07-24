import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtCore import QUrl
from PySide2.QtGui import QPixmap
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QSplashScreen

from server import (
    shutdown_event,
    resources_root,
    close_window_request_event,
    config,
)
from server.wev_ipc_handler import IpcHandler

LOGGER = logging.getLogger(__name__)


class WebEnv:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.pixmap = QPixmap(str(Path(resources_root, "splash.png")))
        self.splash = QSplashScreen(self.pixmap)
        self.ipc_handler = IpcHandler(asyncio.get_event_loop())
        self.view = QWebEngineView()

    def start(self):
        LOGGER.info("Opening WebEngineView")
        self.splash.show()
        self.ipc_handler.start()
        self.view.load(
            QUrl(
                f"http://{config.get('flask', 'connect_address')}:{config.get('flask', 'port')}"
            )
        )
        self.view.show()
        self.view.showMaximized()
        self.splash.hide()
        self.view.closeEvent = self.shutdown
        close_window_request_event.subscribe(lambda status: self.view.close())
        sys.exit(self.app.exec_())

    def shutdown(self, event):
        LOGGER.info("WebEngineView Closed, Shutting Down...")
        LOGGER.info("Waiting for IPC Handler Thread to terminate")
        self.ipc_handler.wait()
        LOGGER.info("Signalling Shutdown")
        shutdown_event.on_next(datetime.now())


def start():
    web_env = WebEnv()
    web_env.start()
