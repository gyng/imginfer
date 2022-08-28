import tempfile

from app.handlers.easyocr.handler import EasyOCR
from app.server.download import download_into

pic = "http://cat_server:8888/textpic"


def test_infer_easyocr():
    with tempfile.NamedTemporaryFile() as ntf:
        download_into(pic, ntf, resize=(512, 512))
        handler = EasyOCR()
        result = handler.infer(pic)
        assert result.str_repr.startswith("Helvetica")
        assert result.results[0]["text"] == "Helvetica"
