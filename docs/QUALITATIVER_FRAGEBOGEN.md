# Qualitativer Fragebogen: J.A.R.V.I.S. Setup – Erwartung & Erleben

**Format:** Qualitativer, teilstandardisierter Leitfaden  
**Fragen-Anzahl:** **8** (Vorgabe: min. 5, max. 10 erfüllt)  
**Auswertung:** Qualitative Inhaltsanalyse nach Mayring / Thematische Analyse nach Braun & Clarke  
**Durchführung:** Integriert als Schritt 3 im `JARVIS-Setup.exe` + als eigenständiges Interview

> Warum qualitativ? Ziel ist nicht Zählen, sondern Verstehen: Welche Bedeutung, Wünsche und Bedenken verbinden Nutzer:innen mit einem JARVIS wie aus den YouTube-Videos?

---

## Hinweise für Interviewer:in / Setup

- **Dauer:** 12–18 Min. (ca. 90–120 Sek. pro Frage)
- **Antwortformat:** Offenes Textfeld (mind. 30 Zeichen, empfohlen 200–400 Zeichen)
- **Einleitungstext im Installer:** "Bevor J.A.R.V.I.S. deine Stimme lernt, lernt er dein Denken kennen. Keine Pflicht, keine Noten – nur deine Worte. Du kannst jede Frage überspringen, aber je ehrlicher du bist, desto persönlicher wird dein Assistent."

## Die 8 Fragen

### 1. Rolle & Bedeutung
**Was bedeutet ein persönlicher Assistent wie J.A.R.V.I.S. für dich im Alltag – welche Rolle soll er einnehmen?**
*Probe:* Eher Butler, Kollege, Freund, Werkzeug? Wann würdest du "Sir" sagen wollen, wann nicht?
*Leitfaden-Hintergrund:* Ermittelt Metaphern & Rollenverständnis (zentral für Persona-Tuning).

### 2. Kernmoment
**Beschreibe eine konkrete Situation, in der J.A.R.V.I.S. dir ideal helfen würde. Was wäre passiert, was wäre danach anders?**
*Probe:* Montag 07:32 Uhr, du bist spät dran – was tut er?
*Leitfaden-Hintergrund:* Critical Incident, deckt echten Bedarf vs. Spielerei auf.

### 3. Vertrauen & Grenzen
**Welche Bedenken oder Grenzen empfindest du bei einer Always-On-Sprachsteuerung ("Hey Jarvis")?**
*Probe:* Mikrofon im Schlafzimmer? Daten ins Cloud? Was wäre ein Dealbreaker?
*Leitfaden-Hintergrund:* Privacy-Calculus, wichtig für STRICT/OFFLINE-Modus Entscheidung.

### 4. Stimme & Persönlichkeit
**Wie stellst du dir die ideale Stimme und Persönlichkeit von J.A.R.V.I.S. vor (Tonfall, Humor, Förmlichkeit)?**
*Probe:* Paul Bettany (britisch, trocken) oder eher locker? Soll er widersprechen dürfen?
*Leitfaden-Hintergrund:* Voice-ID + ElevenLabs Settings ableiten.

### 5. Must-have vs. Gimmick
**Welche Funktionen sind für dich unverzichtbar, welche wären nur Spielerei? Warum?**
*Probe:* E-Mails schreiben, Code erklären, Lichter steuern, Witze, Games? Woran merkst du "brauche ich täglich"?
*Leitfaden-Hintergrund:* Priorisierung für Plugin-Installation (50+ Plugins im ONEPUNCHMAN411/Jarvis).

### 6. Design & Immersion
**Wie wichtig sind dir Design und Haptik des Setups (HUD, Arc Reactor, Soundeffekte) für das Gefühl, wirklich J.A.R.V.I.S. zu nutzen?**
*Probe:* Reicht dir eine Chatbox oder brauchst du das Leuchten, das Summen, das "Sir"?
*Leitfaden-Hintergrund:* Validiert das aufwändige HUD vs. Minimalismus.

### 7. Adoption & Abbruch
**Was würde dich dazu bringen, J.A.R.V.I.S. täglich zu nutzen – und was würde dich schnell wieder deinstallieren lassen?**
*Probe:* Latenz, falsche Antworten, zu viel Gerede, Abo-Kosten?
*Leitfaden-Hintergrund:* Retention-Risiken, direkte Produkt-Lehren.

### 8. Wunschfähigkeit
**Wenn du J.A.R.V.I.S. eine neue Fähigkeit geben könntest, die es in keinem YouTube-Tutorial gibt – welche wäre das und warum?**
*Probe:* Etwas völlig Utopisches ist erlaubt.
*Leitfaden-Hintergrund:* Innovation, öffnet für wilde Ideen ohne Skalen-Zwang.

---

## Methodisches

| Kriterium | Umsetzung |
|-----------|-----------|
| **Sampling** | 5–12 Teilnehmer (Sättigung bei qualitativen Leitfaden laut Pilotierung 20–30% Iterationsrate) |
| **Transkription** | Setup speichert Antworten als `profile.json` + Export als CSV |
| **Kategoriensystem** | Deduktiv: Rolle, Vertrauen, Funktion, Design, Bindung. Induktiv: In-Vivo Codes aus Antworten |
| **Gütekriterien** | Inter-Coder Reliabilität ~0.80 (Mayring), Member-Check optional |
| **Ethik** | Einwilligung im Installer, lokale Speicherung standardmäßig, Cloud nur mit Opt-In |

## Auswertungs-Leitfaden (kurz)

1. **Offen kodieren:** Jede Antwort in 2–5 Codes zerlegen
2. **Axial kodieren:** Codes zu Themen bündeln (z.B. "Butler vs. Partner")
3. **Selektiv kodieren:** Kernkategorie bilden – z.B. "JARVIS als ruhiger Co-Pilot, nicht als Show"
4. **Zitat-Anker:** Starke O-Töne für Präsentation sichern

## Export

- Im Installer: `%APPDATA%\JARVIS\profile.json` bzw. `~/.jarvis/profile.json`
- In diesem Repo: `docs/antworten_beispiel.csv` (ausgefülltes Beispiel)

---

*Erstellt für: Veryoriginaljarvis – JARVIS-Setup.exe (YouTube-authentisches HUD) – 2026*
