import pathlib
from os import path

from flask import Flask, send_file

app = Flask("cat_server")


@app.route("/cat", methods=["GET"])
def cat():
    current = pathlib.Path(__file__).parent.resolve()
    cat_path = path.join(current, "cat.jpg")
    return send_file(cat_path, mimetype="image/jpg"), 200  # type: ignore


@app.route("/meow", methods=["GET"])
def meow():
    return "meow", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
