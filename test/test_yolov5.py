import tempfile

from app.handlers.yolov5.handler import YoloV5
from app.server.download import download_into

pic = "http://cat_server:8888/cat"


def test_infer_yolov5():
    with tempfile.NamedTemporaryFile() as ntf:
        download_into(pic, ntf, resize=(512, 512))
        handler = YoloV5()
        result = handler.infer(pic)
        assert result.str_repr.startswith("image 1/1:")
        assert result.results[0]["name"] == "cat"
