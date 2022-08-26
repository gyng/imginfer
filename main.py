from app.server.api import init_handlers, make_app
from app.server.auth import api_key

if api_key:
    print("API_KEY environment variable found; auth required")
else:
    print("API_KEY environment variable not found; auth not required")

init_handlers()

# gunicorn expects flask_app to be exposed,
# so don't wrap this in `if __name__ == "__main__":`
flask_app = make_app(api_key=api_key)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080, debug=False)
