from app.handlers.yolov5.handler import YoloV5


cat_pic = "http://cat_server:8888/cat"


def test_infer_yolov5():
    handler = YoloV5()
    result = handler.infer(cat_pic)
    assert result.str_repr.startswith("image 1/1:")
    assert result.results[0]["name"] == "cat"
