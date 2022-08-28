#!/bin/bash
set -euox pipefail

pytest .

python3 -m black . --check

python3 -m mypy .

flake8 .

isort . --check-only

# Instantly exit cat_server
curl http://cat_server:8888/shutdown || true
