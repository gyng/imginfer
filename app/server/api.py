from typing import Dict, Optional

from flask import Flask, request

from app.handlers import Handler, InferError
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
                },
                {
                    "methods": ["GET"],
                    "path": "/cat",
                },
            ]
        }

    @app.route("/infer", methods=["POST"])
    def infer() -> dict:
        if api_key:
            auth = request.headers.get("Authorization")
            if not auth:
                return {"error": "unauthorized"}, 401  # type: ignore
            token = auth.replace("Bearer ", "")
            if token != api_key:
                return {"error": "unauthorized"}, 401  # type: ignore

        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return {"error": f"bad content-type {content_type}"}, 400  # type: ignore

        req_json = request.json
        if req_json is not None:
            if not handlers.get("yolov5"):
                return {"error": "yolov5 not initialized"}, 500  # type: ignore

            try:
                yolov5 = handlers["yolov5"].infer(req_json["uri"])
            except InferError as e:
                return {"error": e.message}, 500  # type: ignore

        if not yolov5:
            return {"error": "Inference failed"}, 500  # type: ignore

        return {"yolov5": yolov5}, 200  # type: ignore

    @app.route("/healthcheck")
    def healthcheck():
        return {"health": "ok"}, 200  # type: ignore

    return app
