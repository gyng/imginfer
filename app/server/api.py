import json
import logging
import tempfile
from typing import Any, Dict, Optional

from flask import Flask, request

from app.handlers import Handler, InferError
from app.handlers.danbooru2018.handler import Danbooru2018
from app.handlers.easyocr.handler import EasyOCR
from app.handlers.yolov5.handler import YoloV5
from app.server.download import download_into

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
    def infer() -> dict:
        if api_key:
            auth = request.headers.get("Authorization")
            if not auth:
                return {"error": "unauthorized"}, 401  # type: ignore
            token = auth.replace("Bearer ", "")
            if token != api_key:
                return {"error": "unauthorized"}, 401  # type: ignore

        try:
            req_json = json.loads(request.data)
            if req_json is None or req_json.get("uri") is None:
                return {"error": "bad request"}, 400  # type: ignore
        except Exception as e:
            logging.info(e)
            return {"error": "bad request"}, 400  # type: ignore

        enabled_models = req_json.get("models", ["yolov5", "easyocr", "danbooru2018"])
        if not isinstance(enabled_models, list) or len(enabled_models) == 0:
            return {"models": []}, 200  # type: ignore

        with tempfile.NamedTemporaryFile() as ntf:
            try:
                download_into(req_json["uri"], ntf, resize=(512, 512))
                response: Dict[str, Any] = {"models": enabled_models}
            except InferError as e:
                return {"error": e.message}, 400  # type: ignore
            except Exception as e:
                logging.warn(e)
                return {"error": "failed to download"}, 400  # type: ignore

            # TODO: DRY this out
            # yolov5
            if "yolov5" in enabled_models:
                if handlers.get("yolov5") is None:
                    return {"error": "yolov5 not initialized"}, 500  # type: ignore
                try:
                    yolov5 = handlers["yolov5"].infer(ntf.name)
                except InferError as e:
                    return {"error": e.message}, 500  # type: ignore
                if not yolov5:
                    return {"error": "inference failed"}, 500  # type: ignore
                response["yolov5"] = yolov5  # type: ignore

            # easyocr
            if "easyocr" in enabled_models:
                if handlers.get("easyocr") is None:
                    return {"error": "easyocr not initialized"}, 500  # type: ignore
                try:
                    easyocr = handlers["easyocr"].infer(ntf.name)
                except InferError as e:
                    return {"error": e.message}, 500  # type: ignore
                if not easyocr:
                    return {"error": "inference failed"}, 500  # type: ignore
                response["easyocr"] = easyocr

            # easyocr
            if "danbooru2018" in enabled_models:
                if handlers.get("danbooru2018") is None:
                    return {"error": "danbooru2018 not initialized"}, 500  # type: ignore  # noqa: E501
                try:
                    danbooru2018 = handlers["danbooru2018"].infer(ntf.name)
                except InferError as e:
                    return {"error": e.message}, 500  # type: ignore
                if not danbooru2018:
                    return {"error": "inference failed"}, 500  # type: ignore
                response["danbooru2018"] = danbooru2018

            return response, 200  # type: ignore

    @app.route("/healthcheck")
    def healthcheck():
        return {"health": "ok"}, 200  # type: ignore

    return app
