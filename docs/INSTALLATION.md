# Installation – J.A.R.V.I.S. Setup.exe

## Variante A: Direkt starten (ohne Installation)

**Web-Preview (identisch zum EXE-Look):**
```
web-preview/index.html  -> Doppelklick im Browser öffnen
```
Das ist 1:1 der Installer, den die .exe zeigt – nur ohne System-Schreibzugriff.

**Python Installer (läuft überall):**
```bash
pip install customtkinter pillow
python installer/src/main.py
```

## Variante B: Windows .EXE bauen (1 Befehl)

Auf Windows 10/11 mit Python 3.10+:

```powershell
pip install -r installer/build/requirements.txt
python installer/build/build_exe.py
# -> installer/dist/JARVIS-Setup.exe (ca. 45 MB, inkl. Python Embedded)
```

Alternativ mit Inno Setup (für signierbaren Installer):

```powershell
# Inno Setup 6 installieren:
winget install --id JRSoftware.InnoSetup -e
iscc installer/build/JarvisSetup.iss
# -> installer/dist/JARVIS-Setup-v1.0.exe
```

## Variante C: Fertige EXE herunterladen

Siehe `installer/dist/` – dort liegt nach dem Build:

- `JARVIS-Setup.exe` – Portabler Installer (kein Admin nötig, NSIS per-user)
- `JARVIS-Setup-v1.0.zip` – Portable Version (entpacken, `JARVIS.exe` starten)

> Hinweis: Windows SmartScreen zeigt "Windows protected your PC" weil nicht code-signiert – wie bei allen YouTube JARVIS Projekten: **Mehr Infos -> Trotzdem ausführen**.

## Systemanforderungen (aus YouTube-Recherche)

|  | Minimum | Empfohlen |
|---|---------|-----------|
| OS | Windows 10 64-bit (1809+) | Windows 11 |
| RAM | 8 GB | 16 GB + 6 GB VRAM (für lokale Modelle) |
| Speicher | 2 GB frei | 5 GB (für Whisper + LLM) |
| Mikrofon | ja | Headset mit Boom-Mic |
| Internet | für API-Keys (Gemini/Groq gratis) | offline mit Ollama möglich |

## Nach der Installation

1. Desktop-Verknüpfung "J.A.R.V.I.S." (Cyan Arc Reactor Icon) doppelklicken
2. Voice Enrollment: 5x "Jarvis" sagen (Waveform muss ausschlagen)
3. API-Key eingeben (Gemini: aistudio.google.com, Groq: console.groq.com – beide gratis)
4. `Hey Jarvis` sagen – HUD öffnet sich

## Troubleshooting

- **Rainmeter Skin lädt nicht:** Rainmeter 4.5+ installieren, dann `JARVIS.ini -> Load`
- **Mikrofon kein Ausschlag:** Windows Settings -> Datenschutz -> Mikrofon -> JARVIS erlauben
- **Antivirus blockiert:** Ausnahme für `JARVIS-Setup.exe` hinzufügen (false positive wegen PyInstaller)
- **Kein Sound:** `pipewire` / `pulseaudio` prüfen (Linux)

