import os
import pathlib
from os import path

from flask import Flask, send_file

app = Flask("cat_server")
current = pathlib.Path(__file__).parent.resolve()


@app.route("/cat", methods=["GET"])
def cat():
    picpath = path.join(current, "cat.jpg")
    return send_file(picpath, mimetype="image/jpg"), 200  # type: ignore


@app.route("/meow", methods=["GET"])
def meow():
    return "meow", 200


@app.route("/textpic", methods=["GET"])
def textpic():
    picpath = path.join(current, "text.png")
    return send_file(picpath, mimetype="image/png"), 200  # type: ignore


@app.route("/anime", methods=["GET"])
def anime():
    picpath = path.join(current, "anime.jpg")
    return send_file(picpath, mimetype="image/jpg"), 200  # type: ignore


@app.get("/shutdown")
def shutdown():
    os._exit(0)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
