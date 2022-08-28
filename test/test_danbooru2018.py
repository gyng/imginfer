import tempfile

from app.handlers.danbooru2018.handler import Danbooru2018
from app.server.download import download_into

pic = "http://cat_server:8888/anime"


def test_infer_easyocr():
    with tempfile.NamedTemporaryFile() as ntf:
        download_into(pic, ntf, resize=(512, 512))
        handler = Danbooru2018()
        result = handler.infer(ntf.name)
        assert result.str_repr.startswith("hinanawi_tenshi")
