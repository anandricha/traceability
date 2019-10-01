from flask import Flask
from tracebility.database import DB

def create_app():
    app = Flask(__name__)
    DB.init()
    return app

app = create_app()
from tracebility import routes