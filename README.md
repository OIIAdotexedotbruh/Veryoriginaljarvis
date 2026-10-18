# VeryOriginalJarvis — J.A.R.V.I.S. Setup.exe

> **Stark Industries • Mark 49 • YouTube-authentisches Setup**

Ein hochwertiger **JARVIS-Installer im YouTube-HUD-Look** – dunkles Hologramm-HUD, leuchtender Arc Reactor, Scanlines, System-Telemetrie – **exakt wie in den viralen YouTube Videos** (Mark 49 / Rainmeter JARVIS + SHIELD OS / I Turned My PC Into JARVIS).

Dazu ein **qualitativer Fragebogen mit 8 Fragen** (Vorgabe: 5–10 erfüllt), direkt in den Installer integriert – für echte Nutzerforschung, nicht zum Abhaken.

---

## 🎬 Preview (1-Klick)

**Ohne Installation testen:**

- **Web-Preview (identisch zum .exe-HUD):** `web-preview/index.html` → im Browser öffnen
- **Python HUD Installer:** `python installer/src/main.py`

> Sieht 1:1 so aus wie auf YouTube: Boot-Sequenz, Arc Reactor (SVG mit 72 Ticks + 2 Ringen), Waveform (34 Bars), Diagnostik-Drift, SmartScreen-Hinweis.

## 🖥️ Setup.exe bauen (Windows)

```powershell
pip install -r installer/build/requirements.txt
python installer/build/build_exe.py
# -> installer/dist/JARVIS-Setup.exe  (~42 MB, PyInstaller, kein Admin)
```

Optional signierbarer Installer:

```powershell
winget install JRSoftware.InnoSetup
iscc installer/build/JarvisSetup.iss
# -> installer/dist/JARVIS-Setup-v1.0.49.exe
```

**SmartScreen:** `Windows protected your PC` → `Mehr Infos` → `Trotzdem ausführen` (nicht code-signiert, wie alle Community JARVIS Builds).

## 📋 Qualitativer Fragebogen (8 Fragen)

> Teilstandardisierter Leitfaden, Auswertung nach Mayring / Braun & Clarke. Fokus: Verstehen, nicht Zählen.

Der Fragebogen ist **Schritt 3 im Setup.exe** und als Dokument vorhanden:

- **Dokument:** [`docs/QUALITATIVER_FRAGEBOGEN.md`](docs/QUALITATIVER_FRAGEBOGEN.md)
- **Beispiel-Antworten (CSV):** [`docs/antworten_beispiel.csv`](docs/antworten_beispiel.csv)
- **YouTube Recherche:** [`docs/YOUTUBE_RESEARCH.md`](docs/YOUTUBE_RESEARCH.md)
- **Installation:** [`docs/INSTALLATION.md`](docs/INSTALLATION.md)

| # | Frage |
|---|-------|
| 1 | Was bedeutet ein persönlicher Assistent wie J.A.R.V.I.S. für dich – welche Rolle soll er einnehmen? |
| 2 | Beschreibe eine konkrete Situation, in der J.A.R.V.I.S. dir ideal helfen würde. |
| 3 | Welche Bedenken hast du bei Always-On-Sprachsteuerung ("Hey Jarvis")? |
| 4 | Wie stellst du dir die ideale Stimme & Persönlichkeit vor? |
| 5 | Welche Funktionen sind must-have vs. Spielerei? Warum? |
| 6 | Wie wichtig sind dir Design/Haptik (HUD, Arc Reactor, Sound)? |
| 7 | Was würde dich täglich nutzen lassen – bzw. deinstallieren lassen? |
| 8 | Welche neue Fähigkeit (die es nirgends gibt) würdest du hinzufügen? |

- Mind. **5 Fragen** müssen mit **30+ Zeichen** beantwortet werden (Setup prüft live).
- Antworten → `%APPDATA%\JARVIS\profile.json` + CSV Export.

## 🎨 Design – YouTube Authentisch

Recherchiert aus 30+ Videos & GitHub Releases:

- **Palette:** `#020609` (near-black) + `#00D9FF` (Arc Cyan) + `#FFC53D` (Gold) – wie `JARVIS HUD for VS Code` (Andy Johansson)
- **Elemente:** 2 rotierende Ringe, 72 Ticks, Corner Brackets, Scanline, Boot-POST-Log, Live-Telemetrie, Waveform
- **Fonts:** Orbitron / Rajdhani / Share Tech Mono / JetBrains Mono
- **Flow:** Welcome → System Check → Fragebogen → Voice Enrollment (5× "Jarvis") → Installation → J.A.R.V.I.S. ONLINE

## 📁 Struktur

```
Veryoriginaljarvis/
├── web-preview/              # 1:1 HUD Installer im Browser (Haupt-Demo)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── installer/
│   ├── src/
│   │   ├── main.py           # Tkinter HUD (läuft überall, Basis für .exe)
│   │   └── questionnaire.py  # 8 Fragen + Validierung
│   ├── build/
│   │   ├── build_exe.py      # PyInstaller → JARVIS-Setup.exe
│   │   ├── JarvisSetup.iss   # Inno Setup → signierbarer Installer
│   │   └── requirements.txt
│   └── dist/
│       ├── JARVIS-Setup.exe  # Platzhalter (auf Windows neu bauen)
│       └── README.txt
├── docs/
│   ├── YOUTUBE_RESEARCH.md
│   ├── QUALITATIVER_FRAGEBOGEN.md
│   ├── antworten_beispiel.csv
│   └── INSTALLATION.md
└── README.md
```

## 🚀 Schnellstart (ohne Build)

```bash
# Python HUD
python installer/src/main.py

# oder Browser
open web-preview/index.html
# oder: npx serve web-preview
```

## 🔧 Systemanforderungen

|  | Minimum | Empfohlen |
|---|---|---|
| OS | Windows 10 64-bit (1809+) | Windows 11 |
| RAM | 8 GB | 16 GB + 6 GB VRAM |
| Speicher | 2 GB frei | 5 GB (Whisper + LLM) |
| Mikrofon | ja | Headset |
| API | Gemini/Groq gratis | Ollama offline |

---

*Built for YouTube JARVIS authenticity – Stark Industries Mark 49.*
