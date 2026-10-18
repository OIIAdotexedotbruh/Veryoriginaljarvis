# Qualitativer Fragebogen – 8 Fragen (5-10 Vorgabe)
# Wird sowohl im Web-Preview als auch im Python-Installer verwendet.

QUESTIONS = [
    {
        "id": 1,
        "frage": "Was bedeutet ein persönlicher Assistent wie J.A.R.V.I.S. für dich im Alltag – welche Rolle soll er einnehmen?",
        "hint": "Butler, Kollege, Freund, Werkzeug?",
        "probe": "Wann würdest du 'Sir' sagen wollen?"
    },
    {
        "id": 2,
        "frage": "Beschreibe eine konkrete Situation, in der J.A.R.V.I.S. dir ideal helfen würde. Was wäre passiert, was wäre danach anders?",
        "hint": "Critical Incident – Montag 07:32 Uhr",
        "probe": "Was tut er exakt?"
    },
    {
        "id": 3,
        "frage": "Welche Bedenken oder Grenzen empfindest du bei einer Always-On-Sprachsteuerung (\"Hey Jarvis\")?",
        "hint": "Mikrofon, Daten, Cloud – Dealbreaker?",
        "probe": "Schlafzimmer / Arbeitsplatz?"
    },
    {
        "id": 4,
        "frage": "Wie stellst du dir die ideale Stimme und Persönlichkeit von J.A.R.V.I.S. vor (Tonfall, Humor, Förmlichkeit)?",
        "hint": "Paul Bettany trocken/britisch oder locker?",
        "probe": "Darf er widersprechen?"
    },
    {
        "id": 5,
        "frage": "Welche Funktionen sind für dich unverzichtbar, welche wären nur Spielerei? Warum?",
        "hint": "E-Mails, Code, Lichter, Games",
        "probe": "Täglich vs. einmal im Monat"
    },
    {
        "id": 6,
        "frage": "Wie wichtig sind dir Design und Haptik des Setups (HUD, Arc Reactor, Soundeffekte) für das Gefühl, wirklich J.A.R.V.I.S. zu nutzen?",
        "hint": "Reicht Chatbox oder brauchst du das Leuchten?",
        "probe": "Sound wichtig?"
    },
    {
        "id": 7,
        "frage": "Was würde dich dazu bringen, J.A.R.V.I.S. täglich zu nutzen – und was würde dich schnell wieder deinstallieren lassen?",
        "hint": "Latenz, falsche Antworten, Abo-Kosten?",
        "probe": "Retention vs. Abbruch"
    },
    {
        "id": 8,
        "frage": "Wenn du J.A.R.V.I.S. eine neue Fähigkeit geben könntest, die es in keinem YouTube-Tutorial gibt – welche wäre das und warum?",
        "hint": "Utopisch erlaubt – sei wild.",
        "probe": "Warum genau diese?"
    },
]

EXAMPLE_ANSWERS = [
    "Für mich ist JARVIS wie ein ruhiger Butler – er soll im Hintergrund arbeiten, nur sprechen wenn ich ihn rufe, und nie proaktiv dazwischenquatschen. Wie Alfred, nicht wie Clippy.",
    "Montag 7:32, ich bin spät: JARVIS hat schon meine Mails überflogen, sagt mir welche dringend sind, startet das Auto-Navi und legt die Präsentation auf den Desktop. Ich spare 12 Minuten.",
    "Always-On macht mir Angst wegen Firmen-Meetings und nachts. Mikrofon muss ein Hardware-Mute haben und lokal erkennen, nicht alles in die Cloud schicken.",
    "Ich will Paul Bettany – britisch, trocken, leicht humorvoll. Er darf widersprechen, aber nie belehren. Humor nur wenn ich humorvoll bin.",
    "Unverzichtbar: E-Mails zusammenfassen, Code erklären, Kalender. Spielerei: Games und Witze – nett, aber ich deinstalliere nicht wegen fehlendem TicTacToe.",
    "Sehr wichtig. Ohne das cyan Leuchten und den Reactor fühlt es sich nur wie ChatGPT an. Das HUD macht das Iron-Man-Gefühl – das ist der halbe Grund, es zu nutzen.",
    "Täglich nutzen würde ich ihn wenn er schnell ist (<1s), keine Abo-Kosten hat und sich Dinge über Wochen merkt. Deinstallieren bei Halluzinationen oder wenn er Daten leakt.",
    "Er soll meine Handbewegungen per Webcam verstehen – Minority-Report-Gesten für Fenster schieben. Gibt es in keinem Tutorial und wäre echte Magie."
]

def validate_answers(answers):
    """Gibt (gültig, ausgefüllt) zurück. Gültig = >=30 Zeichen."""
    gultig = sum(1 for a in answers if len(a.strip()) >= 30)
    ausgefüllt = sum(1 for a in answers if len(a.strip()) > 0)
    return gultig, ausgefüllt

def is_complete(answers, minimum=5):
    gultig, _ = validate_answers(answers)
    return gultig >= minimum
