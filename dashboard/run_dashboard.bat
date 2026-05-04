@echo off
REM Windows launcher — double-click to run
cd /d "%~dp0"
start "" http://127.0.0.1:8050
python app.py
pause
