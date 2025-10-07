#!/usr/bin/env bash
set -euo pipefail

FULL_PATH=$(pwd)
python3 -m venv src/venv
source src/venv/bin/activate
streamlit run $FULL_PATH/src/stocks.py &
