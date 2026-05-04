#!/bin/bash
# Linux launcher
cd "$(dirname "$0")"
(sleep 2 && xdg-open http://127.0.0.1:8050) &
python3 app.py
