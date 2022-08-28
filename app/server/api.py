import json
import logging
from typing import Dict, Optional

from flask import Flask, request

from app.handlers import Handler, InferError
from app.handlers.danbooru2018.handler import Danbooru2018
from app.handlers.easyocr.handler import EasyOCR
from app.handlers.yolov5.handler import YoloV5
from app.server.auth import check_flask_auth_header
from app.server.infer import infer

handlers: Dict[str, Handler] = {}


def init_handlers():
    if not handlers.get("yolov5"):
        logging.info("initializing yolov5...")
        handlers["yolov5"] = YoloV5()
    if not handlers.get("easyocr"):
        logging.info("initializing easyocr...")
        handlers["easyocr"] = EasyOCR()
    if not handlers.get("danbooru2018"):
        logging.info("initializing danbooru2018...")
        handlers["danbooru2018"] = Danbooru2018()
    logging.info("done initializing models.")


def make_app(*, api_key: Optional[str]) -> Flask:
    app = Flask("imginfer")

    @app.route("/")
    def home_route():
        return {
            "endpoints": [
                {
                    "methods": ["POST"],
                    "path": "/infer",
                    "accept": ["application/json"],
                    "auth": ["Authorization: Bearer <API_KEY>"],
                    "examples": [
                        r"""{ "uri": "www.example.com/image_url.jpg" }""",
                        r"""{ "uri": "www.example.com/image_url.jpg", "models": ["yolov5", "easyocr"] }""",  # noqa: E501
                        r"""curl -X POST http://localhost:8080/infer -H 'Content-Type: application/json' -H 'Authorization: Bearer <API_KEY>' -d '{ "uri": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/390px-Cat_poster_1.jpg" }'""",  # noqa: E501
                    ],
                },
                {
                    "methods": ["GET"],
                    "path": "/healthcheck",
                },
            ],
            "auth_required": api_key is not None,
            # TODO: make configurable
            "models": ["yolov5", "easyocr", "danbooru2018"],
        }

    @app.route("/infer", methods=["POST"])
    def infer_route() -> dict:
        if not check_flask_auth_header(api_key, request):
            return {"error": "unauthorized"}, 401  # type: ignore

        try:
            req_json = json.loads(request.data)
            if req_json is None or req_json.get("uri") is None:
                return {"error": "bad request"}, 400  # type: ignore
        except Exception as e:
            logging.info(e)
            return {"error": "bad request"}, 400  # type: ignore

        enabled_models = req_json.get("models", ["yolov5", "easyocr", "danbooru2018"])

        try:
            response = infer(
                enabled_models=enabled_models,
                uri=req_json["uri"],
                handlers=handlers,
                resize=(512, 512),
            )
        except InferError as e:
            return {"error": e.message}, 400  # type: ignore

        return response, 200  # type: ignore

    @app.route("/healthcheck")
    def healthcheck_route():
        return {"health": "ok"}, 200  # type: ignore

    return app
