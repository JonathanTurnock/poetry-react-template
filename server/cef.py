import logging
import platform
import sys

from cefpython3 import cefpython as cef

from . import config

LOGGER = logging.getLogger(__name__)


def start():
    LOGGER.info("Starting Embedded Chrome")
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(
        url=f"http://"
        f"{config.get('app', 'host_addr')}:"
        f"{config.get('app', 'host_port')}",
        window_title=config.get("app", "display_name"),
    )
    cef.MessageLoop()
    cef.Shutdown()


def check_versions():
    ver = cef.GetVersion()
    logging.info(f"CEF Python {ver['version']}")
    logging.info(f"Chromium {ver['chrome_version']}")
    logging.info(f"CEF {ver['cef_version']}")
    logging.info(
        f"Python {platform.python_version()} {platform.architecture()[0]}"
    )
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"
