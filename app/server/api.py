from typing import Dict, Optional

from flask import Flask, request

from app.handlers import Handler
from app.handlers.yolov5.handler import YoloV5  # type: ignore

handlers: Dict[str, Handler] = {}


def init_handlers():
    if not handlers.get("yolov5"):
        handlers["yolov5"] = YoloV5()


def make_app(*, api_key: Optional[str]) -> Flask:
    app = Flask("imginfer")

    @app.route("/")
    def home():
        return {
            "endpoints": [
                {
                    "methods": ["POST"],
                    "path": "/infer",
                    "accept": ["application/json"],
                    "auth": ["Authorization: Bearer <API_KEY>"],
                    "examples": [
                        r"""{ "uri": "www.example.com/image_url.jpg" }""",
                        r"""curl -X POST http://localhost:8080/infer -H 'Content-Type: application/json' -H 'Authorization: Bearer <API_KEY>' -d '{ "uri": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/390px-Cat_poster_1.jpg" }'""",  # noqa: E501
                    ],
                }
            ]
        }

    @app.route("/infer", methods=["POST"])
    def infer() -> dict:
        if api_key:
            auth = request.headers.get("Authorization")
            if not auth:
                return "", 401  # type: ignore
            token = auth.replace("Bearer ", "")
            if token != api_key:
                return "", 401  # type: ignore

        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return f"Bad Content-Type {content_type}", 400  # type: ignore

        req_json = request.json
        if req_json is not None:
            if not handlers.get("yolov5"):
                return "yolov5 not initialized", 500  # type: ignore
            yolov5 = handlers["yolov5"].infer(req_json["uri"])

        if not yolov5:
            return "Inference failed", 500  # type: ignore

        return {"yolov5": yolov5}, 200  # type: ignore

    return app
