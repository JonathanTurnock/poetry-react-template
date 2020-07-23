import glob
import os
import shutil
import sys
from pathlib import Path

from server.app import app

sys.dont_write_bytecode = True

test_html = "build/test-reports/pytest/tests.html"
test_xml = "build/test-reports/pytest/junit.xml"
cov_xml = "build/test-reports/pytest/coverage.xml"
cov_html = "build/test-reports/pytest"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def info(msg):
    print(f"{bcolors.OKGREEN}INFO: {msg}{bcolors.ENDC}")


def warning(msg):
    print(f"{bcolors.WARNING}WARNING: {msg}{bcolors.ENDC}")


def error(msg):
    print(f"{bcolors.FAIL}ERROR: {msg}{bcolors.ENDC}")


def test():
    info("🧪 Running Unit Tests")
    result = os.system(" ".join(
        ["pytest",
         "-o", "junit_family=xunit2",
         f"--html={test_html}",
         f"--junitxml={test_xml}",
         f"--cov-report=xml:{cov_xml}",
         f"--cov-report=html:{cov_html}",
         f"--cov-report=term",
         f"--cov=server",
         f"server/",
         ]
    ))

    info(
        "Unit Tests Run:\n"
        f"📑 Test HTML Report: {Path(os.getcwd(), test_html).as_uri()}\n"
        f"📑 Coverage HTML Report: {Path(os.getcwd(), cov_html, 'index.html').as_uri()}\n"
    )

    if result != 0:
        error(f"🤬 Test Run Failed with exit code {result}, Exiting 🤬")
        sys.exit(result)


def clean():
    info("🧽 Cleaning Folders")
    info("Removing Build Folder")
    shutil.rmtree("build", ignore_errors=True)
    info("Removing Pytest Cache")
    shutil.rmtree(".pytest_cache", ignore_errors=True)
    info("Running PyClean")
    os.system("pyclean server/")
    info("Removing Coverage")
    if os.path.exists(".coverage"):
        os.remove(".coverage")
    info("Removing .egg-info folders")
    for path in glob.glob("*.egg-info"):
        shutil.rmtree(path, ignore_errors=True)
    info("✨ Folders Cleaned ✨")


def dev():
    app.run()


def build():
    info("Building...")
    clean()
    test()

    info("👷 Building React App ‍")
    os.system('yarn --cwd "client" && yarn --cwd "client" build')
    info("React App Build complete")

    try:
        info("Copying React App to web folder")
        shutil.rmtree("web", ignore_errors=True)
        shutil.move("client/build", "web")
        info("🥳 Done 🥳")
    except FileNotFoundError:
        error("Failed to copy build from client folder as it doesnt exist")
