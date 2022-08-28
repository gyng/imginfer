#!/bin/bash
set -euox pipefail

pytest . || curl http://cat_server:8888/shutdown

python3 -m black . --check

python3 -m mypy .

flake8 .

isort . --check-only

curl http://cat_server:8888/shutdown || true
