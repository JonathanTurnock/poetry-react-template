import logging
import sys

from PySide2 import QtWidgets
from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView

LOGGER = logging.getLogger(__name__)


def start():
    LOGGER.info("Starting Web Engine View")
    app = QtWidgets.QApplication(sys.argv)
    view = QWebEngineView()
    view.load(QUrl("http://127.0.0.1:5000"))
    view.show()
    view.closeEvent = lambda event: LOGGER.info("Shutting Down Application!!")
    sys.exit(app.exec_())
