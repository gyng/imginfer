from io import BytesIO
import logging
import shutil
from typing import Any, Optional, Tuple

import requests
from PIL import Image

from app.handlers import InferError


def download_into(
    url: str, tmp: Any, *, resize: Optional[Tuple[int, int]] = (512, 512)
):
    """
    url: eg, https://example.com/mypic.jpg
    tmp: Tempfile.TemporaryNamedFile
    resize: max bounds eg, (512, 512)
    """
    try:
        response = requests.get(url, stream=True)
    except Exception as e:
        logging.error(f"Failed to download url {url}")
        logging.error(e)
        raise InferError("failed to retrieve image")
    with open(tmp.name, "wb") as out_file:
        if resize is not None:
            im = Image.open(BytesIO(response.content))
            im.thumbnail(resize, Image.LANCZOS)
            im.save(out_file.name, "BMP")
        else:
            shutil.copyfileobj(response.raw, out_file)

    del response
