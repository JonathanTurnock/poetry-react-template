import configparser
import logging.config
from os import path
from pathlib import Path

# === === === Paths === === ===
root = Path(path.abspath(path.dirname(__file__))).parent
web_root = Path(root, "web")
resources_root = Path(root, "resources")

# === === === Logging Engine === === ===
# LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
# logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
logging.config.fileConfig(Path(resources_root, "logging.ini"))

# === === === Configuration Files === === ===
config = configparser.ConfigParser()
config.read(Path(resources_root, "config.ini"))
