import os
import shutil

from server.app import app


def flask():
    app.run()


def build():
    print("INFO: Building...")

    print("INFO: Building React App 👷‍")
    os.system('yarn --cwd "client" && yarn --cwd "client" build')
    print("INFO: React App Build complete")

    try:
        print("INFO: Copying React App to web folder")
        shutil.rmtree("web", ignore_errors=True)
        shutil.move("client/build", "web")
        print("INFO: Done 🥳")
    except FileNotFoundError:
        print("ERROR: Failed to copy build from client folder as it doesnt exist")
