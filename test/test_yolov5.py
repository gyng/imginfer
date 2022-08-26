from app.handlers.yolov5.handler import YoloV5


def test_infer_yolov5():
    cat_pic = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/390px-Cat_poster_1.jpg"  # noqa: E501
    handler = YoloV5()
    result = handler.infer(cat_pic)
    assert result.str_repr.startswith("image 1/1:")
    assert result.results[0]["name"] == "cat"
