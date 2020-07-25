import logging
from os import path
from pathlib import Path

from flask import Flask, send_from_directory, jsonify
from flask_graphql import GraphQLView

from . import web_root, config
from .gql import schema
from .health import get_app_health

LOGGER = logging.getLogger(__name__)

app = Flask(__name__, root_path=web_root)

app.add_url_rule(
    "/api/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


@app.route("/")
def index():
    return send_from_directory(web_root, "index.html")


@app.route("/<file>")
def web(file):
    if path.exists(Path(web_root, file)):
        return send_from_directory(web_root, file)
    else:
        return index()


@app.route("/api/health", methods=["GET"])
def check_health():
    return jsonify(get_app_health())


def start():
    LOGGER.info("Starting Server")
    app.run(
        host=config.get("flask", "bind_address"),
        port=config.getint("flask", "port"),
    )
