@echo off
REM J.A.R.V.I.S. Setup – Windows Schnellstart
echo Starting J.A.R.V.I.S. Setup...
python installer\src\main.py 2>nul
if errorlevel 1 (
  echo Python nicht gefunden – oeffne Web-Preview im Browser...
  start web-preview\index.html
)
pause
