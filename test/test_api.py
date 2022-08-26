import json

import pytest

from app.server.api import init_handlers, make_app


@pytest.fixture(scope="module", autouse=True)
def init():
    init_handlers()


def test_api_root():
    app = make_app(api_key=None)
    res = app.test_client().get("/")
    assert res.status_code == 200
    assert json.loads(res.data.decode("utf-8"))["endpoints"]


def test_api_infer():
    app = make_app(api_key=None)
    cat_pic = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/390px-Cat_poster_1.jpg"  # noqa: E501
    res = app.test_client().post("/infer", json={"uri": cat_pic})
    assert res.status_code == 200
    res_json = json.loads(res.data.decode("utf-8"))
    assert res_json["yolov5"]["results"]


def test_api_infer_auth():
    app = make_app(api_key="hunter2")
    cat_pic = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/390px-Cat_poster_1.jpg"  # noqa: E501
    res = app.test_client().post("/infer", json={"uri": cat_pic})
    assert res.status_code == 401

    res = app.test_client().post(
        "/infer",
        headers={"Authorization": "Bearer bad_key"},
        json={"uri": cat_pic},
    )
    assert res.status_code == 401

    res = app.test_client().post(
        "/infer", headers={"Authorization": "Bearer hunter2"}, json={"uri": cat_pic}
    )
    assert res.status_code == 200
