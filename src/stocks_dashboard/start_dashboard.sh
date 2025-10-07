#!/usr/bin/env bash
set -euo pipefail

FULL_PATH=$(pwd)
python3 -m venv venv
source venv/bin/activate
streamlit run $FULL_PATH/stocks.py &
