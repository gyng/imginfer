#!/bin/bash
set -euox pipefail

# https://pytorch.org/get-started/locally/

pip uninstall -y torch torchvision torchaudio

if [ "$1" == "cu113" ]; then
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
elif [ "$1" == "cu116" ]; then
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
else
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
fi
