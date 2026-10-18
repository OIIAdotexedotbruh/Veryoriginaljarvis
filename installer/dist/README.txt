J.A.R.V.I.S. SETUP – STARK INDUSTRIES MARK 49

Dieses Verzeichnis enthält nach dem Build die fertige Windows-EXE:

  JARVIS-Setup.exe              -> Einzel-Datei Installer (PyInstaller, ~42 MB, kein Admin nötig)
  JARVIS-Setup-v1.0.49.exe      -> Inno Setup Installer (signierbar, mit Autostart-Option)

So baust du die EXE auf Windows:

  1. Python 3.10+ installieren (Haken "Add to PATH")
  2. In diesem Repo:
       pip install -r installer/build/requirements.txt
       python installer/build/build_exe.py
  3. Optional mit Inno Setup 6:
       winget install JRSoftware.InnoSetup
       iscc installer/build/JarvisSetup.iss

SmartScreen Hinweis (wie in jedem YouTube Tutorial):
  Windows zeigt "Windows protected your PC" weil nicht code-signiert.
  Klicke: Mehr Infos -> Trotzdem ausführen.

Ohne Windows kannst du den identischen Installer direkt starten:

  python installer/src/main.py
  oder
  web-preview/index.html im Browser öffnen (1:1 gleiches HUD)

Alle Antworten des qualitativen Fragebogens landen in:
  Windows: %APPDATA%\JARVIS\profile.json
  Linux/macOS: ~/.jarvis/profile.json
  + CSV Export im Setup

