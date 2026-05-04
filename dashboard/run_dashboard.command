#!/bin/bash
# macOS launcher — double-click to run
cd "$(dirname "$0")"
(sleep 2 && open http://127.0.0.1:8050) &
python3 app.py
