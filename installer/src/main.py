#!/usr/bin/env python3
# J.A.R.V.I.S. SETUP – Tkinter HUD Installer (YouTube-authentisch)
# Läuft auf Windows/macOS/Linux ohne extra Abhängigkeiten (nur stdlib).
# Für den .exe Build: `pip install pyinstaller` + `python build/build_exe.py`

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, sys, platform, time, random, csv, pathlib

# Import Fragen
try:
    from questionnaire import QUESTIONS, EXAMPLE_ANSWERS, validate_answers, is_complete
except ImportError:
    from installer.src.questionnaire import QUESTIONS, EXAMPLE_ANSWERS, validate_answers, is_complete  # fallback

APP_NAME = "J.A.R.V.I.S. SETUP"
VERSION = "1.0.49 MARK 49"
BG = "#020609"
BG2 = "#0A1E33"
CYAN = "#00D9FF"
GOLD = "#FFC53D"
MUTED = "#6B7E93"
TEXT = "#DCECFF"

STEPS = ["WILLKOMMEN","SYSTEM CHECK","FRAGEBOGEN","STIMME","INSTALLATION","ONLINE"]

class JarvisSetup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} — STARK INDUSTRIES {VERSION}")
        self.geometry("1160x700")
        self.minsize(1000, 620)
        self.configure(bg=BG)
        self.current = 0
        self.answers = [""] * len(QUESTIONS)
        self.profile_path = self.get_profile_path()

        # style
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Rajdhani", 10))
        style.configure("Title.TLabel", foreground=CYAN, font=("Orbitron", 14, "bold"))
        style.configure("Cyan.Horizontal.TProgressbar", troughcolor="#0A1E33", background=CYAN, bordercolor=CYAN)

        self.build_layout()
        self.show_step(0)
        self.boot_sequence()

    def get_profile_path(self):
        if platform.system() == "Windows":
            base = os.environ.get("APPDATA", os.path.expanduser("~"))
            p = os.path.join(base, "JARVIS")
        else:
            p = os.path.join(os.path.expanduser("~"), ".jarvis")
        os.makedirs(p, exist_ok=True)
        return os.path.join(p, "profile.json")

    def build_layout(self):
        # Topbar
        top = tk.Frame(self, bg="#070F1C", height=44, highlightthickness=1, highlightbackground="#0A3A4A")
        top.pack(fill="x", side="top")
        top.pack_propagate(False)
        tk.Label(top, text="◉  J.A.R.V.I.S.   STARK INDUSTRIES • MARK 49 • SETUP", bg="#070F1C", fg=CYAN, font=("Orbitron", 10, "bold")).pack(side="left", padx=12)
        self.clock_lbl = tk.Label(top, text="--:--", bg="#070F1C", fg=MUTED, font=("Share Tech Mono", 9))
        self.clock_lbl.pack(side="right", padx=12)
        self.sys_lbl = tk.Label(top, text="SYSTEM STANDBY", bg="#070F1C", fg=MUTED, font=("Share Tech Mono", 9, "bold"))
        self.sys_lbl.pack(side="right", padx=6)
        self.tick_clock()

        # Body: 3 cols
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        # left nav
        self.left = tk.Frame(body, bg="#081424", highlightthickness=1, highlightbackground="#0A3A4A", width=240)
        self.left.pack(side="left", fill="y", padx=(0,8))
        self.left.pack_propagate(False)

        tk.Label(self.left, text="01 • INSTALLATION", bg="#081424", fg=CYAN, font=("Share Tech Mono", 8)).pack(anchor="w", padx=12, pady=(12,4))
        tk.Label(self.left, text="SETUP SCHRITTE", bg="#081424", fg=CYAN, font=("Orbitron", 9, "bold")).pack(anchor="w", padx=12)

        self.step_buttons = []
        for i, name in enumerate(STEPS):
            b = tk.Button(self.left, text=f"{i+1}. {name}", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9),
                          bd=0, anchor="w", padx=12, pady=6, activebackground="#0A1E33", activeforeground=CYAN,
                          command=lambda idx=i: self.try_goto(idx))
            b.pack(fill="x", padx=8, pady=2)
            self.step_buttons.append(b)

        # progress
        self.pct_lbl = tk.Label(self.left, text="0%", bg="#081424", fg=TEXT, font=("Share Tech Mono", 9, "bold"))
        self.pct_lbl.pack(anchor="w", padx=12, pady=(12,2))
        self.pbar = ttk.Progressbar(self.left, style="Cyan.Horizontal.TProgressbar", mode="determinate", maximum=100)
        self.pbar.pack(fill="x", padx=12, pady=2)

        tk.Label(self.left, text="JARVIS-Setup.exe  • 412 MB\nOffline-fähig • kein Admin nötig\nSmartScreen: Mehr Infos → Trotzdem", bg="#081424", fg=MUTED, font=("Share Tech Mono", 7), justify="left").pack(anchor="w", padx=12, pady=8)

        self.left_log = tk.Text(self.left, bg="#020A12", fg="#8FB3CC", font=("JetBrains Mono", 7), height=8, bd=0, highlightthickness=1, highlightbackground="#0A3A4A", padx=6, pady=6)
        self.left_log.pack(fill="x", padx=8, pady=8)
        self.left_log.insert("1.0", "[BOOT] Warte auf Start...\n")
        self.left_log.config(state="disabled")

        # center
        self.center = tk.Frame(body, bg="#0A1E33", highlightthickness=1, highlightbackground="#0A3A4A")
        self.center.pack(side="left", fill="both", expand=True)

        # canvas for steps
        self.content = tk.Frame(self.center, bg="#0A1E33")
        self.content.pack(fill="both", expand=True, padx=14, pady=14)

        # right – reactor + telemetry
        self.right = tk.Frame(body, bg="#081424", highlightthickness=1, highlightbackground="#0A3A4A", width=260)
        self.right.pack(side="right", fill="y", padx=(8,0))
        self.right.pack_propagate(False)

        tk.Label(self.right, text="02 • REAKTOR & TELEMETRIE", bg="#081424", fg=CYAN, font=("Share Tech Mono", 8)).pack(anchor="w", padx=12, pady=(12,6))

        # reactor canvas
        self.reactor_canvas = tk.Canvas(self.right, bg="#081424", width=180, height=180, highlightthickness=0)
        self.reactor_canvas.pack(pady=6)
        self.draw_reactor()

        self.reactor_lbl = tk.Label(self.right, text="STANDBY • 32% • 18°C", bg="#081424", fg=CYAN, font=("Share Tech Mono", 8))
        self.reactor_lbl.pack()

        # diagnostics
        tk.Label(self.right, text="System Diagnostik", bg="#081424", fg=CYAN, font=("Orbitron", 9, "bold")).pack(anchor="w", padx=12, pady=(10,4))
        self.diag_text = tk.Label(self.right, text="", bg="#0A1E33", fg=TEXT, font=("Share Tech Mono", 8), justify="left", anchor="w")
        self.diag_text.pack(fill="x", padx=8)
        tk.Label(self.right, text="Suit Telemetry", bg="#081424", fg=CYAN, font=("Orbitron", 9, "bold")).pack(anchor="w", padx=12, pady=(10,4))
        self.tele_text = tk.Label(self.right, text="", bg="#0A1E33", fg=TEXT, font=("Share Tech Mono", 8), justify="left", anchor="w")
        self.tele_text.pack(fill="x", padx=8)
        self.update_telemetry()

    def tick_clock(self):
        self.clock_lbl.config(text=time.strftime("%H:%M:%S"))
        self.after(1000, self.tick_clock)

    def draw_reactor(self):
        c = self.reactor_canvas
        c.delete("all")
        cx, cy = 90, 90
        # outer ring
        c.create_oval(cx-78, cy-78, cx+78, cy+78, outline=CYAN, width=2)
        # dashed ring
        for i in range(0, 360, 12):
            a = i * 3.14159/180
            x1 = cx + 68* (1 if i%2==0 else 0.98) * (1) # simplified
            # ticks
            x = cx + 78 * 0.95 * (1)  # placeholder, will draw simple
        # core
        c.create_oval(cx-34, cy-34, cx+34, cy+34, fill=CYAN, outline="", width=0)
        c.create_oval(cx-22, cy-22, cx+22, cy+22, fill="#E8FDFF", outline="")
        c.create_text(cx, cy, text="◉", fill="#006A82", font=("Orbitron", 16, "bold"))
        # 72 ticks simulated as small lines
        import math
        for i in range(72):
            ang = math.radians(i*5)
            r1, r2 = 78, 84 if i%6==0 else 82
            x1 = cx + r1*math.cos(ang); y1 = cy + r1*math.sin(ang)
            x2 = cx + r2*math.cos(ang); y2 = cy + r2*math.sin(ang)
            col = GOLD if i%18==0 else CYAN
            c.create_line(x1, y1, x2, y2, fill=col, width=1 if i%6 else 2)

    def update_telemetry(self):
        def r(a,b): return f"{random.uniform(a,b):.1f}"
        diag = f"OS       Windows 11 x64\nCPU      {r(2.8,3.6)} GHz • {r(12,28)}%\nRAM      {r(6.2,14.8)} GB / 16 GB\nGPU      RTX 4060 • {r(32,78)}% • {r(48,72)}°C\nMIC      Aktiv • {r(-42,-28)} dB\nNET      Stark Satellite • {r(18,42)} ms"
        tele = f"REPULSOR  {r(88,100)}% • NOMINAL\nREACTOR   {r(31,44)}% • STABIL\nTEMP      {r(22,34)}°C\nPOWER     {r(90,100)}%\nVOICE     Whisper small 39 MB"
        self.diag_text.config(text=diag)
        self.tele_text.config(text=tele)
        self.reactor_lbl.config(text=f"{self.sys_lbl.cget('text')} • {r(28,48)}% • {r(16,28)}°C")
        self.after(900, self.update_telemetry)

    def log(self, msg, to="left"):
        widget = self.left_log
        widget.config(state="normal")
        widget.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        widget.see("end")
        widget.config(state="disabled")

    def boot_sequence(self):
        # small boot overlay simulation via log
        seq = [
            "[POST] Stark Industries BIOS v49.2 ... OK",
            "[POST] Memory test 16384 MB ... OK",
            "[POST] Arc Reactor core ... ONLINE",
            "[NET ] Linking to Stark Satellite ... OK",
            "[HUD ] Initializing grid ... OK",
            "[AI  ] Whisper tiny.en 39 MB ... ready",
            "[SYS ] J.A.R.V.I.S. ready. Good evening, Sir.",
        ]
        def push(i=0):
            if i>=len(seq): 
                self.sys_lbl.config(text="ONLINE", fg=CYAN)
                self.log("System online. Willkommen, Sir.", "left")
                return
            self.log(seq[i])
            self.after(220, lambda: push(i+1))
        push()

    def highlight_step(self):
        for i,b in enumerate(self.step_buttons):
            if i==self.current:
                b.config(bg="#0A2A44", fg=CYAN)
            elif i<self.current:
                b.config(bg="#061A2A", fg=TEXT)
            else:
                b.config(bg="#081424", fg=MUTED)
        self.pbar['value'] = (self.current)/(len(STEPS)-1)*100
        self.pct_lbl.config(text=f"{int(self.pbar['value'])}%  •  Schritt {self.current+1}/{len(STEPS)}")

    def try_goto(self, idx):
        if idx <= self.current:
            self.show_step(idx)

    def show_step(self, idx):
        self.current = idx
        self.highlight_step()
        for w in self.content.winfo_children(): w.destroy()

        if idx==0: self.view_welcome()
        elif idx==1: self.view_system()
        elif idx==2: self.view_fragebogen()
        elif idx==3: self.view_voice()
        elif idx==4: self.view_install()
        elif idx==5: self.view_done()

    # --- views
    def view_welcome(self):
        tk.Label(self.content, text="Willkommen, Sir.", bg="#0A1E33", fg=TEXT, font=("Orbitron", 18, "bold")).pack(anchor="w")
        tk.Label(self.content, text="Dieser Setup-Assistent installiert J.A.R.V.I.S. – wie in den YouTube-Videos:\n dunkles HUD, leuchtender Arc Reactor, 1-Klick Sprachanbindung.\n Kein Python nötig. Desktop-Shortcut wird erstellt.\n Du wirst durch einen qualitativen Fragebogen (8 Fragen, min. 5) geführt.", bg="#0A1E33", fg=MUTED, font=("Rajdhani", 10), justify="left").pack(anchor="w", pady=8)
        tk.Label(self.content, text="Paket  JARVIS-Setup.exe • 412 MB • offline-fähig\nEnthalten  Holografisches Dashboard • Voice (Whisper) • Browser-Automation", bg="#0A1E33", fg=TEXT, font=("Share Tech Mono", 9), justify="left").pack(anchor="w", pady=6)
        f=tk.Frame(self.content, bg="#0A1E33"); f.pack(fill="x", pady=12)
        tk.Button(f, text="Installation beginnen →", bg=CYAN, fg="#00111A", font=("Share Tech Mono", 10, "bold"), bd=0, padx=14, pady=8, command=lambda: self.show_step(1)).pack(side="left", padx=4)
        tk.Button(f, text="Demo überspringen", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=1, highlightbackground="#0A3A4A", command=lambda: self.show_step(4)).pack(side="left", padx=4)
        tk.Label(self.content, text="Wie auf YouTube: SmartScreen Warnung normal – Mehr Infos → Trotzdem ausführen (nicht code-signiert).", bg="#0A1E33", fg=GOLD, font=("Share Tech Mono", 8)).pack(anchor="w", pady=6)

    def view_system(self):
        tk.Label(self.content, text="System Diagnose", bg="#0A1E33", fg=CYAN, font=("Orbitron", 13, "bold")).pack(anchor="w")
        tk.Label(self.content, text="Prüfe Voraussetzungen – rechts siehst du Live-Telemetrie wie im Rainmeter Theme.", bg="#0A1E33", fg=MUTED, font=("Rajdhani", 10)).pack(anchor="w", pady=4)
        box=tk.Frame(self.content, bg="#020A12", highlightthickness=1, highlightbackground="#0A3A4A")
        box.pack(fill="x", pady=8, padx=2)
        checks=[("OS","Windows 11 Pro 64-bit","BEREIT"),("RAM","16 GB (15.8 verfügbar)","BEREIT"),("CPU","Intel i7-12700H 14 Kerne","BEREIT"),("GPU","NVIDIA RTX 4060 8GB","BEREIT"),("Storage","84 GB frei (412 MB benötigt)","BEREIT"),("Microphone","Standard Mic Array 48kHz","BEREIT"),("Network","Stark Satellite 28ms","BEREIT")]
        for k,v,s in checks:
            row=tk.Frame(box, bg="#020A12"); row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=k, bg="#020A12", fg=MUTED, font=("Share Tech Mono", 8), width=14, anchor="w").pack(side="left")
            tk.Label(row, text=v, bg="#020A12", fg=TEXT, font=("Share Tech Mono", 8)).pack(side="left")
            tk.Label(row, text=s, bg="#020A12", fg="#2BFF6B", font=("Share Tech Mono", 8, "bold")).pack(side="right")
        f=tk.Frame(self.content, bg="#0A1E33"); f.pack(fill="x", pady=10)
        tk.Button(f, text="← Zurück", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=lambda: self.show_step(0)).pack(side="left")
        tk.Button(f, text="Weiter zum Fragebogen →", bg=CYAN, fg="#00111A", font=("Share Tech Mono", 10, "bold"), bd=0, padx=12, pady=6, command=lambda: self.show_step(2)).pack(side="right")

    def view_fragebogen(self):
        tk.Label(self.content, text="Bevor J.A.R.V.I.S. deine Stimme lernt, lernt er dein Denken kennen.", bg="#0A1E33", fg=TEXT, font=("Orbitron", 11, "bold"), wraplength=700, justify="left").pack(anchor="w")
        tk.Label(self.content, text="Qualitativer Fragebogen – 8 offene Fragen (min. 5 mit 30+ Zeichen, max. 10 Vorgabe erfüllt). Antworten werden lokal in profile.json gespeichert. Keine Skalen, nur deine Worte.", bg="#0A1E33", fg=MUTED, font=("Rajdhani", 9), wraplength=750, justify="left").pack(anchor="w", pady=4)

        # progress lbl
        prog_lbl = tk.Label(self.content, text="", bg="#0A1E33", fg=CYAN, font=("Share Tech Mono", 9, "bold"))
        prog_lbl.pack(anchor="w")

        # scrollable area
        container = tk.Frame(self.content, bg="#0A1E33")
        container.pack(fill="both", expand=True, pady=6)

        canvas = tk.Canvas(container, bg="#0A1E33", highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#0A1E33")
        win = canvas.create_window((0,0), window=inner, anchor="nw")
        def on_conf(e): canvas.configure(scrollregion=canvas.bbox("all")); canvas.itemconfig(win, width=e.width)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", on_conf)
        # mousewheel
        def _wheel(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _wheel)

        text_widgets = []

        def update_prog():
            gultig, ausgefuellt = validate_answers(self.answers)
            prog_lbl.config(text=f"Fortschritt: {gultig} / {len(QUESTIONS)} gültig (30+ Zeichen) • {ausgefuellt} ausgefüllt • Minimum 5 nötig")
            # enable/disable next
            if is_complete(self.answers, 5):
                next_btn.config(state="normal", bg=CYAN, fg="#00111A", text="Weiter zur Stimme →")
            else:
                next_btn.config(state="disabled", bg="#0A3A4A", fg=MUTED, text=f"Mind. 5 Fragen (30+ Zeichen) – jetzt {gultig}")
            # update per item hints
            for idx, (lbl, tw) in enumerate(text_widgets):
                l = len(self.answers[idx].strip())
                if l>=30: lbl.config(text=f"{idx+1}. {QUESTIONS[idx]['frage']}   ✓ gültig ({l} Zeichen)", fg="#2BFF6B")
                elif l>0: lbl.config(text=f"{idx+1}. {QUESTIONS[idx]['frage']}   {l} Zeichen – noch {30-l}", fg=GOLD)
                else: lbl.config(text=f"{idx+1}. {QUESTIONS[idx]['frage']}   leer", fg=MUTED)

        for i,q in enumerate(QUESTIONS):
            item = tk.Frame(inner, bg="#061A2A", highlightthickness=1, highlightbackground="#0A3A4A")
            item.pack(fill="x", pady=5, padx=4)
            lbl = tk.Label(item, text=f"{i+1}. {q['frage']}", bg="#061A2A", fg=TEXT, font=("Rajdhani", 9, "bold"), wraplength=700, justify="left", anchor="w")
            lbl.pack(anchor="w", padx=8, pady=(8,2))
            tk.Label(item, text=f"{q['hint']} • {q['probe']}", bg="#061A2A", fg=MUTED, font=("Share Tech Mono", 7)).pack(anchor="w", padx=8)
            tw = tk.Text(item, height=4, bg="#020A12", fg=TEXT, font=("JetBrains Mono", 9), bd=0, highlightthickness=1, highlightbackground="#0A3A4A", padx=6, pady=6, wrap="word")
            tw.pack(fill="x", padx=8, pady=6)
            tw.insert("1.0", self.answers[i])
            # hint row
            hint = tk.Label(item, text=f"{len(self.answers[i])} Zeichen • mind. 30 Zeichen", bg="#061A2A", fg=MUTED, font=("Share Tech Mono", 7))
            hint.pack(anchor="w", padx=8, pady=(0,6))

            def make_handler(idx, widget, hint_lbl=hint, lbl_ref=lbl):
                def on_key(e=None):
                    self.answers[idx] = widget.get("1.0", "end-1c")
                    hint_lbl.config(text=f"{len(self.answers[idx])} Zeichen • {'✓ gültig' if len(self.answers[idx].strip())>=30 else 'mind. 30 Zeichen'}")
                    update_prog()
                return on_key

            handler = make_handler(i, tw)
            tw.bind("<KeyRelease>", handler)
            tw.bind("<FocusOut>", handler)
            text_widgets.append((lbl, tw))

        # buttons bottom
        btn_frame = tk.Frame(self.content, bg="#0A1E33")
        btn_frame.pack(fill="x", pady=8)
        tk.Button(btn_frame, text="← Zurück", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=lambda: self.show_step(1)).pack(side="left")
        tk.Button(btn_frame, text="Beispiel ausfüllen", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=lambda: self.fill_example(update_prog, text_widgets)).pack(side="left", padx=6)
        tk.Button(btn_frame, text="CSV exportieren", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=self.export_csv).pack(side="left", padx=6)
        next_btn = tk.Button(btn_frame, text="Mind. 5 Fragen (30+ Zeichen)", bg="#0A3A4A", fg=MUTED, font=("Share Tech Mono", 9, "bold"), bd=0, padx=12, pady=6, command=lambda: self.show_step(3))
        next_btn.pack(side="right")
        update_prog()

        # ensure scroll reset
        canvas.yview_moveto(0)

    def fill_example(self, update_fn, widgets):
        for i, txt in enumerate(EXAMPLE_ANSWERS):
            self.answers[i]=txt
        # refill widgets
        for (lbl, tw) in widgets:
            idx = widgets.index((lbl, tw))
            tw.delete("1.0", "end")
            tw.insert("1.0", self.answers[idx])
        update_fn()
        self.log("Beispiel-Antworten eingefüllt (8/8).", "left")
        messagebox.showinfo("Beispiel", "Beispiel-Antworten eingefüllt – alle 8 Fragen gültig.")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="jarvis_qualitativer_fragebogen.csv")
        if not path: return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w=csv.writer(f, delimiter=";")
            w.writerow(["Nummer","Frage","Antwort","Zeichen"])
            for i,q in enumerate(QUESTIONS):
                w.writerow([i+1, q['frage'], self.answers[i], len(self.answers[i])])
        messagebox.showinfo("Export", f"CSV gespeichert:\n{path}")
        self.log(f"CSV exportiert: {path}")

    def view_voice(self):
        tk.Label(self.content, text="Voice Enrollment", bg="#0A1E33", fg=CYAN, font=("Orbitron", 13, "bold")).pack(anchor="w")
        tk.Label(self.content, text="Sage 5× „Jarvis\" – Waveform schlägt aus (34 Bars). Simuliert wie in YouTube-Tutorials (Silero-VAD, Dmitri Voice).", bg="#0A1E33", fg=MUTED, font=("Rajdhani", 10)).pack(anchor="w", pady=4)
        box=tk.Frame(self.content, bg="#020A12", highlightthickness=1, highlightbackground="#0A3A4A")
        box.pack(fill="x", pady=8)
        status = tk.Label(box, text="Bereit – klicke „Zuhören starten\"", bg="#020A12", fg=TEXT, font=("Share Tech Mono", 10, "bold"))
        status.pack(pady=8)
        prog = tk.Label(box, text="0 / 5 erkannt", bg="#020A12", fg=CYAN, font=("Share Tech Mono", 10))
        prog.pack()
        log = tk.Text(box, height=6, bg="#020A12", fg="#8FB3CC", font=("JetBrains Mono", 8), bd=0, highlightthickness=0)
        log.pack(fill="x", padx=8, pady=6)
        log.insert("1.0","[INFO] VAD bereit, Whisper tiny.en geladen.\n")
        log.config(state="disabled")

        # persona
        tk.Label(self.content, text="Persona wählen", bg="#0A1E33", fg=CYAN, font=("Orbitron", 10, "bold")).pack(anchor="w", pady=(10,4))
        persona = tk.StringVar(value="Paul Bettany – britisch, trocken")
        for name in ["Paul Bettany – britisch, trocken","FRIDAY – weiblich, direkt","Stark – jung, frech","Custom – ElevenLabs ID"]:
            tk.Radiobutton(self.content, text=name, variable=persona, value=name, bg="#0A1E33", fg=TEXT, selectcolor="#061A2A", font=("Rajdhani", 9), activebackground="#0A1E33").pack(anchor="w")

        f=tk.Frame(self.content, bg="#0A1E33"); f.pack(fill="x", pady=10)
        tk.Button(f, text="← Zurück", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=lambda: self.show_step(2)).pack(side="left")

        def toggle():
            # simulate enrollment
            status.config(text="Höre zu – sage „Jarvis\" ...", fg=GOLD)
            self.log("Voice pipeline aktiv, VAD läuft...")
            cnt = {"n":0}
            def tick():
                cnt["n"]+=1
                prog.config(text=f"{cnt['n']} / 5 erkannt")
                log.config(state="normal"); log.insert("end", f"[{time.strftime('%H:%M:%S')}] „Jarvis\" erkannt – Confidence 0.{92+random.randint(0,6)} – Sample {cnt['n']}/5\n"); log.see("end"); log.config(state="disabled")
                self.log(f"Sample {cnt['n']}/5 captured.")
                if cnt["n"]<5:
                    self.after(800, tick)
                else:
                    status.config(text="✓ Enrolled – Voiceprint gespeichert", fg="#2BFF6B")
                    prog.config(text="5 / 5 erkannt – fertig")
                    self.log("Voiceprint gespeichert: data/voiceprint.json")
                    nextb.config(state="normal", bg=CYAN, fg="#00111A")
            tick()

        tk.Button(f, text="▶ Zuhören starten", bg=CYAN, fg="#00111A", font=("Share Tech Mono", 10, "bold"), bd=0, padx=12, pady=6, command=toggle).pack(side="left", padx=6)
        tk.Button(f, text="Simulieren (Demo)", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=toggle).pack(side="left", padx=6)
        nextb = tk.Button(f, text="Weiter zur Installation →", bg=CYAN, fg="#00111A", font=("Share Tech Mono", 10, "bold"), bd=0, padx=12, pady=6, command=lambda: self.show_step(4))
        nextb.pack(side="right")

    def view_install(self):
        tk.Label(self.content, text="Installiere J.A.R.V.I.S.", bg="#0A1E33", fg=CYAN, font=("Orbitron", 13, "bold")).pack(anchor="w")
        tk.Label(self.content, text="Wie im YouTube Setup: Python Embedded + Libs (~400 MB) + Whisper (~39 MB) + Rainmeter Skin. Kein Admin nötig.", bg="#0A1E33", fg=MUTED, font=("Rajdhani", 10)).pack(anchor="w", pady=4)
        log = tk.Text(self.content, height=10, bg="#020A12", fg="#8FB3CC", font=("JetBrains Mono", 9), bd=0, highlightthickness=1, highlightbackground="#0A3A4A")
        log.pack(fill="both", expand=True, pady=8)
        log.insert("1.0","[INFO] Bereit zur Installation\n")
        pbar = ttk.Progressbar(self.content, style="Cyan.Horizontal.TProgressbar", mode="determinate", maximum=100)
        pbar.pack(fill="x", pady=4)

        steps = [
            "Entpacke Python 3.11 Embedded ...",
            "Pip install customtkinter pillow faster-whisper ... 412 MB",
            "Lade Whisper tiny.en ... 39 MB (offline STT)",
            "Lade Silero VAD + Dmitri Voice ... 18 MB",
            "Installiere Rainmeter Skin: JARVIS + SHIELD OS ...",
            "Schreibe Registry: Desktop Shortcut (Arc Reactor Icon) ...",
            "Schreibe config.yaml – API Adapter Groq/Gemini ...",
            "Speichere profile.json (8 Antworten, qualitativ) ...",
            "Teste Mikrofon – 34 Bars ... OK",
            "Fertig. J.A.R.V.I.S. bereit.",
        ]
        f=tk.Frame(self.content, bg="#0A1E33"); f.pack(fill="x", pady=6)
        tk.Button(f, text="← Zurück", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=lambda: self.show_step(3)).pack(side="left")
        start_btn = tk.Button(f, text="Installation starten", bg=CYAN, fg="#00111A", font=("Share Tech Mono", 10, "bold"), bd=0, padx=12, pady=6)
        start_btn.pack(side="right")

        def do_install(i=0):
            if i>=len(steps):
                start_btn.config(text="✓ Fertig", state="disabled")
                self.save_profile()
                self.log("Installation abgeschlossen, profile.json gespeichert.")
                self.after(700, lambda: self.show_step(5))
                return
            log.insert("end", f"[{i+1:02}/10] {steps[i]}\n")
            log.see("end")
            self.log(steps[i])
            pbar['value'] = (i+1)/len(steps)*100
            self.after(500, lambda: do_install(i+1))

        start_btn.config(command=lambda: (start_btn.config(state="disabled", text="Installiere ..."), do_install()))

    def save_profile(self):
        data = {
            "meta": {"app": APP_NAME, "version": VERSION, "created": time.strftime("%Y-%m-%dT%H:%M:%S"), "type": "qualitativer Fragebogen 8 Fragen"},
            "answers": {f"F{i+1}": {"frage": q["frage"], "antwort": self.answers[i], "zeichen": len(self.answers[i])} for i,q in enumerate(QUESTIONS)}
        }
        try:
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # also save csv nearby
            csv_path = os.path.join(os.path.dirname(self.profile_path), "jarvis_fragebogen.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                w=csv.writer(f, delimiter=";")
                w.writerow(["Nummer","Frage","Antwort"])
                for i,q in enumerate(QUESTIONS):
                    w.writerow([i+1, q["frage"], self.answers[i]])
        except Exception as e:
            messagebox.showwarning("Speicherfehler", str(e))

    def view_done(self):
        tk.Label(self.content, text="J.A.R.V.I.S. ONLINE", bg="#0A1E33", fg="#2BFF6B", font=("Orbitron", 18, "bold")).pack(anchor="w")
        tk.Label(self.content, text="Guten Abend, Sir. Alle Systeme nominal. Dein Fragebogen wurde gespeichert – J.A.R.V.I.S. kennt jetzt deine Präferenzen.\nDesktop-Verknüpfung „J.A.R.V.I.S.\" wurde erstellt (Cyan Arc Reactor Icon). Sage „Hey Jarvis\" oder klatsche zweimal.", bg="#0A1E33", fg=TEXT, font=("Rajdhani", 10), justify="left").pack(anchor="w", pady=6)
        tk.Label(self.content, text="Hotkey Strg+J überall • \"Jarvis, öffne YouTube\" • Rainmeter: Iron Man → Jarvis.ini → Load", bg="#0A1E33", fg=MUTED, font=("Share Tech Mono", 8)).pack(anchor="w")
        f=tk.Frame(self.content, bg="#0A1E33"); f.pack(fill="x", pady=12)
        tk.Button(f, text="HUD starten →", bg="#2BFF6B", fg="#00220A", font=("Share Tech Mono", 10, "bold"), bd=0, padx=12, pady=6, command=lambda: messagebox.showinfo("J.A.R.V.I.S.", "HUD gestartet – (Demo) Dashboard würde sich öffnen.")).pack(side="left", padx=4)
        tk.Button(f, text="Profil öffnen", bg="#081424", fg=CYAN, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=lambda: os.startfile(self.profile_path) if platform.system()=="Windows" else messagebox.showinfo("Profil", self.profile_path)).pack(side="left", padx=4)
        tk.Button(f, text="Setup beenden", bg="#081424", fg=MUTED, font=("Share Tech Mono", 9), bd=0, padx=10, pady=6, command=self.destroy).pack(side="right")

        # preview json
        preview = tk.Text(self.content, height=10, bg="#020A12", fg="#8FB3CC", font=("JetBrains Mono", 8), bd=0, highlightthickness=1, highlightbackground="#0A3A4A")
        preview.pack(fill="both", expand=True, pady=6)
        try:
            with open(self.profile_path, encoding="utf-8") as fp:
                preview.insert("1.0", fp.read())
        except:
            preview.insert("1.0", json.dumps({f"F{i+1}": self.answers[i] for i in range(len(QUESTIONS))}, ensure_ascii=False, indent=2))
        preview.config(state="disabled")
        self.sys_lbl.config(text="ONLINE • BEREIT", fg="#2BFF6B")
        self.log("J.A.R.V.I.S. online. Welcome home, Sir.")

if __name__ == "__main__":
    app = JarvisSetup()
    app.mainloop()
