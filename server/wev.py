import logging
import sys
import time
from datetime import datetime
from pathlib import Path

from PySide2.QtCore import QUrl
from PySide2.QtGui import QPixmap
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QSplashScreen, QApplication

from server import (
    shutdown_event,
    resources_root,
    config,
    close_window_request_event,
)

_splash_screen = Path(resources_root, "splash.png")

LOGGER = logging.getLogger(__name__)
_app = QApplication(sys.argv)
_pixmap = QPixmap(str(_splash_screen))
_splash = QSplashScreen(_pixmap)
_view = QWebEngineView()
_exit_code = 0


def start():
    LOGGER.info("Opening WebEngineView")
    _splash.show()
    _view.load(
        QUrl(
            f"http://{config.get('flask', 'connect_address')}:{config.get('flask', 'port')}"
        )
    )
    _view.show()
    _view.showMaximized()
    _splash.hide()
    _view.close = _shutdown
    close_window_request_event.subscribe(_shutdown)
    _exit_code = _app.exec_()
    time.sleep(1)
    LOGGER.debug("Main Event Loop Closed")
    sys.exit(_exit_code)


def _shutdown(event):
    LOGGER.info("WebEngineView Closed, Shutting Down...")
    LOGGER.info("Signalling Shutdown")
    shutdown_event.on_next(datetime.now())
    LOGGER.info("Terminating...")
    _app.quit()
