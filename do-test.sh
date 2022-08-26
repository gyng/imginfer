#!/bin/bash
set -euox pipefail

python3 -m black . --check

python3 -m mypy .

flake8 .

isort . --check-only

pytest .
