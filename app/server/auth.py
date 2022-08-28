import os
from typing import Optional

from flask import Request

# API_KEY=key
# If provided, needs Authorization header
api_key = os.environ.get("API_KEY")


def check_flask_auth_header(_api_key: Optional[str], request: Request) -> bool:
    if not _api_key:
        return True

    auth = request.headers.get("Authorization")

    if not auth:
        return False

    token = auth.replace("Bearer ", "")
    if token == _api_key:
        return True

    return False
