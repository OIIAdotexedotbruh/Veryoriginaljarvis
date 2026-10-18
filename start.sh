#!/bin/bash
# J.A.R.V.I.S. Setup – macOS/Linux Schnellstart
DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null; then
  echo "Starte Python HUD..."
  python3 "$DIR/installer/src/main.py"
else
  echo "Python nicht gefunden – öffne Web-Preview..."
  xdg-open "$DIR/web-preview/index.html" 2>/dev/null || open "$DIR/web-preview/index.html"
fi
