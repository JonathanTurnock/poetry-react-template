import shutil
from server.app import app

def flask():
    app.run()

def build():
    shutil.rmtree("build")
    shutil.move("client/build", "build")