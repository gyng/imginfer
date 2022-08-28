import logging
import tempfile
from typing import Any, Dict, List, Optional, Tuple

from app.handlers import Handler, InferError
from app.server.download import download_into


def infer(
    *,
    enabled_models: List[str],
    uri: str,
    handlers: Dict[str, Handler],
    resize=Optional[Tuple[int, int]],
) -> Dict[str, Any]:
    response: Dict[str, Any] = {"models": enabled_models}

    if not isinstance(enabled_models, list) or len(enabled_models) == 0:
        return {"models": []}

    with tempfile.NamedTemporaryFile() as fh:
        try:
            download_into(uri, fh, resize=resize)
        except InferError as e:
            raise e
        except Exception as e:
            logging.warn(e)
            raise InferError(message="failed to download")

        for mod in enabled_models:
            if handlers.get(mod) is None:
                response[mod] = {"error", f"{mod} not available"}
            try:
                infer_response = handlers[mod].infer(fh.name)
                if not infer_response:
                    response[mod] = {"error": "inference failed"}
                response[mod] = infer_response  # type: ignore
            except InferError as e:
                response[mod] = {"error": e.message}

        return response
