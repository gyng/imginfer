import json

import pytest
from flask import Flask

from app.server.api import init_handlers, make_app


@pytest.fixture(scope="module", autouse=True)
def init():
    init_handlers()


@pytest.fixture()
def public_app():
    app = make_app(api_key=None)
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def private_app():
    app = make_app(api_key="hunter2")
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


cat_pic = "http://cat_server:8888/cat"
cat_meow = "http://cat_server:8888/meow"


def test_api_root(public_app: Flask):
    res = public_app.test_client().get("/")
    assert res.status_code == 200
    assert json.loads(res.data.decode("utf-8"))["endpoints"]


def test_api_infer(public_app: Flask):
    res = public_app.test_client().post("/infer", json={"uri": cat_pic})
    assert res.status_code == 200
    res_json = json.loads(res.data.decode("utf-8"))
    assert res_json["yolov5"]["results"]


def test_api_infer_missing_uri(public_app: Flask):
    res = public_app.test_client().post("/infer", json={"foo": "bar"})
    assert res.status_code == 400
    res_json = json.loads(res.data.decode("utf-8"))
    assert res_json["error"] == "bad request"


def test_api_infer_invalid_request_json(public_app: Flask):
    res = public_app.test_client().post(
        "/infer", headers={"content-type": "application/json"}
    )
    assert res.status_code == 400
    res_json = json.loads(res.data.decode("utf-8"))
    assert res_json["error"] == "bad request"


def test_api_infer_invalid_image(public_app: Flask):
    res = public_app.test_client().post("/infer", json={"uri": cat_meow})
    assert res.status_code == 500
    res_json = json.loads(res.data.decode("utf-8"))
    assert res_json["error"] == f"could not infer {cat_meow}"


def test_api_infer_invalid_uri(public_app: Flask):
    res = public_app.test_client().post("/infer", json={"uri": "rubbish"})
    assert res.status_code == 500
    res_json = json.loads(res.data.decode("utf-8"))
    assert res_json["error"] == "could not infer rubbish"


def test_api_infer_auth(private_app: Flask):
    res = private_app.test_client().post("/infer", json={"uri": cat_pic})
    assert res.status_code == 401

    res = private_app.test_client().post(
        "/infer",
        headers={"Authorization": "Bearer bad_key"},
        json={"uri": cat_pic},
    )
    assert res.status_code == 401

    res = private_app.test_client().post(
        "/infer", headers={"Authorization": "Bearer hunter2"}, json={"uri": cat_pic}
    )
    assert res.status_code == 200
