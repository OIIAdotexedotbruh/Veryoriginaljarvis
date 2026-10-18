#!/bin/bash
# Platzhalter für Windows-EXE – auf Linux/macOS direkt ausführbar:
# Startet den Python-HUD-Installer oder öffnet das Web-Preview
DIR="$(cd "$(dirname "$0")/../.." && pwd)"
if command -v python3 >/dev/null; then
  echo "Starte J.A.R.V.I.S. Setup (Python HUD)..."
  python3 "$DIR/installer/src/main.py" 2>&1 || python3 "$DIR/installer/src/main.py"
else
  echo "Öffne Web-Preview..."
  xdg-open "$DIR/web-preview/index.html" 2>/dev/null || open "$DIR/web-preview/index.html" 2>/dev/null || echo "Bitte öffne web-preview/index.html im Browser"
fi
