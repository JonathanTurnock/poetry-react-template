import glob
import os
import shutil
import sys
from pathlib import Path

from server.main import Application

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
    fmt()
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

    info("Removing webrtc_event_logs")
    shutil.rmtree("webrtc_event_logs", ignore_errors=True)

    info("Removing Logs")
    for path in glob.glob("*.log"):
        try:
            os.remove(path)
        except:
            pass

    info("✨ Folders Cleaned ✨")


def dev():
    fmt()
    application = Application.get_app()
    application.start()


def fmt():
    info("🖤 Formatting Code using Black 🖤")
    os.system("black server")
    info("❄️ Validating with flake8 ❄️")
    os.system("flake8 --ignore=E501 server")


def build():
    info("Building...")
    clean()
    test()

    info("👷 Building React App‍")
    result = os.system('yarn --cwd "client" && yarn --cwd "client" build')

    if result != 0:
        error(f"🤬 Yarn Build Failed with exit code {result}, Exiting 🤬")
        sys.exit(result)

    info("React App Build Complete")

    try:
        info("Copying React App to Web folder")
        try:
            shutil.rmtree("web")
            shutil.move("client/build", "web")
            info("Successfully Copied Build to Web")
        except Exception as e:
            error(f"Failed to Copy Build due to {e}")
        info("🥳 Done 🥳")
    except FileNotFoundError:
        error("Failed to copy build from client folder as it doesnt exist")
