import logging
import shutil
from typing import Any

import requests

from app.handlers import InferError


def download_into(url: str, tmp: Any):
    try:
        response = requests.get(url, stream=True)
    except Exception as e:
        logging.error(f"Failed to download url {url}")
        logging.error(e)
        raise InferError("failed to retrieve image")
    with open(tmp.name, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
