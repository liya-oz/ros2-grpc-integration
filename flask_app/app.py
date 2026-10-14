"""Flask HTTP API that retrieves the latest message through gRPC."""

from pathlib import Path

import grpc
from flask import Flask, Response, jsonify, send_from_directory

from flask_app.grpc_client import get_latest_message

FRONTEND_DIRECTORY = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIRECTORY),
    static_url_path="/static",
)


@app.get("/")
def index() -> Response:
    """Serve the vanilla JavaScript frontend from Flask's origin."""
    return send_from_directory(FRONTEND_DIRECTORY, "index.html")


@app.get("/hello")
def hello() -> Response | tuple[Response, int]:
    """Return the latest ROS message as JSON."""
    try:
        response = get_latest_message()
    except grpc.RpcError as error:
        app.logger.error("Could not retrieve the latest message: %s", error)
        return jsonify({"error": "Could not retrieve the latest message"}), 502

    return jsonify({"message": response.message})
