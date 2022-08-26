#!/bin/bash
set -euox pipefail

python3 -m black .

isort .
