from app.handlers.easyocr.handler import EasyOCR

pic = "http://cat_server:8888/textpic"


def test_infer_easyocr():
    handler = EasyOCR()
    result = handler.infer(pic)
    assert result.str_repr.startswith("Helvetica")
    assert result.results[0]["text"] == "Helvetica"
