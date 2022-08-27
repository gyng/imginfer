#!/bin/bash
set -euox pipefail

pytest . --showlocals
curl http://cat_server:8888/shutdown || true

python3 -m black . --check

python3 -m mypy .

flake8 .

isort . --check-only
