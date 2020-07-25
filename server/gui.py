import logging
from pathlib import Path

from PySide2.QtCore import QUrl
from PySide2.QtGui import QPixmap, QCloseEvent
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QSplashScreen
from rx.subject import Subject

from server import config, resources_root
from server.ipc_handler import ipc_shutdown_event

LOGGER = logging.getLogger(__name__)


class WebView(QWebEngineView):
    close_window_event: Subject

    def __init__(self):
        super(WebView, self).__init__()
        self.load(
            QUrl(
                f"http://{config.get('flask', 'connect_address')}:{config.get('flask', 'port')}"
            )
        )
        self.showMaximized()
        self.close_window_event = Subject()
        self._subscribe_to_ipc_events()

    def close(self, *args, **kwargs):
        self._close()

    def closeEvent(self, close_event: QCloseEvent):
        close_event.ignore()
        self._close()

    def _close(self):
        LOGGER.info("Broadcasting Close Application Event")
        self.close_window_event.on_next(True)

    def _subscribe_to_ipc_events(self):
        ipc_shutdown_event.subscribe(self.close)


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__(
            QPixmap(str(Path(resources_root, "splash.png")))
        )
