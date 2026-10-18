// JARVIS Setup — YouTube-authentische Logik + Qualitativer Fragebogen (8 Fragen)
const STEPS = [
  {id:'welcome', title:'WILLKOMMEN', desc:'Stark Industries Begrüßung'},
  {id:'system', title:'SYSTEM CHECK', desc:'OS • RAM • MIC • GPU'},
  {id:'fragen', title:'QUALITATIVER FRAGEBOGEN', desc:'8 offene Fragen (5-10 Vorgabe)'},
  {id:'voice', title:'STIMME & PERSONA', desc:'Waveform & Enrollment'},
  {id:'install', title:'INSTALLATION', desc:'Pakete & Modelle'},
  {id:'done', title:'ABSCHLUSS', desc:'J.A.R.V.I.S. Online'},
];

const QUESTIONS = [
  {q:'Was bedeutet ein persönlicher Assistent wie J.A.R.V.I.S. für dich im Alltag – welche Rolle soll er einnehmen?', hint:'Butler, Kollege, Freund, Werkzeug? Pflichtfeld, 30–800 Zeichen', probe:'Wann würdest du "Sir" sagen wollen?'},
  {q:'Beschreibe eine konkrete Situation, in der J.A.R.V.I.S. dir ideal helfen würde. Was wäre passiert, was wäre danach anders?', hint:'Critical Incident – Montag 07:32 Uhr, du bist spät dran...', probe:'Was tut er exakt?'},
  {q:'Welche Bedenken oder Grenzen empfindest du bei einer Always-On-Sprachsteuerung ("Hey Jarvis")?', hint:'Mikrofon, Daten, Cloud – Dealbreaker?', probe:'Schlafzimmer? Arbeitsplatz?'},
  {q:'Wie stellst du dir die ideale Stimme und Persönlichkeit von J.A.R.V.I.S. vor (Tonfall, Humor, Förmlichkeit)?', hint:'Paul Bettany trocken/britisch oder locker? Darf er widersprechen?', probe:'Humor ja/nein, wie viel?'},
  {q:'Welche Funktionen sind für dich unverzichtbar, welche wären nur Spielerei? Warum?', hint:'E-Mails, Code, Lichter, Games – woran merkst du "brauche ich"?', probe:'Täglich vs. einmal im Monat'},
  {q:'Wie wichtig sind dir Design und Haptik des Setups (HUD, Arc Reactor, Soundeffekte) für das Gefühl, wirklich J.A.R.V.I.S. zu nutzen?', hint:'Reicht Chatbox oder brauchst du das Leuchten?', probe:'Sound wichtig?'},
  {q:'Was würde dich dazu bringen, J.A.R.V.I.S. täglich zu nutzen – und was würde dich schnell wieder deinstallieren lassen?', hint:'Latenz, falsche Antworten, Abo-Kosten?', probe:'Retention vs. Abbruch'},
  {q:'Wenn du J.A.R.V.I.S. eine neue Fähigkeit geben könntest, die es in keinem YouTube-Tutorial gibt – welche wäre das und warum?', hint:'Utopisch erlaubt – sei wild.', probe:'Warum genau diese?'},
];

let current = 0;
let answers = Array(QUESTIONS.length).fill('');
let bootDone = false;

// --- clock
setInterval(()=>{
  const d=new Date();
  document.getElementById('clock').textContent = d.toLocaleTimeString('de-DE');
},1000);

// --- arc ticks
const ticksEl = document.getElementById('ticks');
for(let i=0;i<72;i++){
  const t=document.createElement('div'); t.className='tick';
  t.style.transform=`translateX(-50%) rotate(${i*5}deg)`;
  if(i%6===0) t.style.height='10px';
  if(i%18===0) t.style.background='#FFC53D';
  ticksEl.appendChild(t);
}
// wave bars
const waveEl=document.getElementById('wave');
for(let i=0;i<34;i++){ const b=document.createElement('i'); waveEl.appendChild(b); }
function setWave(active){
  const bars=waveEl.querySelectorAll('i');
  if(!active){ bars.forEach(b=>b.style.height='6px'); return; }
  bars.forEach((b,idx)=>{
    const h=6+Math.abs(Math.sin(Date.now()/120 + idx*0.6))*28 + Math.random()*6;
    b.style.height=h+'px';
  });
}
setInterval(()=>setWave(document.getElementById('arc').classList.contains('listening')), 90);

// --- diag telemetry (drift)
function rand(a,b){return (Math.random()*(b-a)+a).toFixed(1)}
function paintDiag(){
  const diag=document.getElementById('diag');
  diag.innerHTML=`
    <span>OS</span><strong>Windows 11 x64</strong>
    <span>CPU</span><strong>${rand(2.8,3.6)} GHz • ${rand(12,28)}%</strong>
    <span>RAM</span><strong>${rand(6.2,14.8)} GB / 16 GB</strong>
    <span>GPU</span><strong class="ok">NVIDIA • ${rand(32,78)}% • ${rand(48,72)}°C</strong>
    <span>MIC</span><strong class="ok">Aktiv • ${rand(-42,-28)} dB</strong>
    <span>NET</span><strong class="ok">Stark Satellite • ${rand(18,42)} ms</strong>
  `;
  document.getElementById('tele').innerHTML=`
    <span>REPULSOR</span><strong>${rand(88,100)}% • NOMINAL</strong>
    <span>REACTOR</span><strong class="ok">${rand(31,44)}% • STABIL</strong>
    <span>SUIT TEMP</span><strong>${rand(22,34)}°C</strong>
    <span>POWER</span><strong>${rand(90,100)}%</strong>
    <span>VOICE MODEL</span><strong>Whisper small • 39 MB</strong>
  `;
  document.getElementById('arcReadout').textContent=`${document.getElementById('sysState').textContent} • ${rand(28,48)}% • ${rand(16,28)}°C`;
  document.getElementById('mem').textContent=`${rand(3.1,5.4)} GB frei`;
}
setInterval(paintDiag, 900); paintDiag();

// --- boot sequence (YouTube style)
const bootLines=[
  "[POST] Stark Industries BIOS v49.2 ... OK",
  "[POST] Memory test 16384 MB ... OK",
  "[POST] Arc Reactor core ... ONLINE",
  "[NET ] Linking to Stark Satellite ... OK (23 ms)",
  "[SEC ] Biometric handshake ... OK",
  "[HUD ] Initializing holographic grid ... OK",
  "[AI  ] Loading Whisper (offline) ... 39 MB",
  "[AI  ] Loading LLM adapter (Gemini/Groq) ... ready",
  "[VOX ] Microphone array ... detected",
  "[VOX ] Calibrating repulsors ...",
  "[VOX ] Building it in a cave with a box of scraps ... done",
  "[SYS ] J.A.R.V.I.S. ready. Good evening, Sir.",
];
const bootLog=document.getElementById('bootLog');
const bootProgress=document.getElementById('bootProgress');
let bi=0;
function pushBoot(){
  if(bi>=bootLines.length){ finishBoot(); return; }
  bootLog.textContent += bootLines[bi] + "\n";
  bootLog.scrollTop=bootLog.scrollHeight;
  bootProgress.style.width = Math.round((bi+1)/bootLines.length*100)+'%';
  bi++; setTimeout(pushBoot, 220+Math.random()*240);
}
pushBoot();
function finishBoot(){
  document.getElementById('sysState').textContent='ONLINE';
  document.getElementById('sysState').style.color='var(--cyan)';
  setTimeout(()=>{ document.getElementById('boot').classList.add('hidden'); bootDone=true; render(); toast('System online. Willkommen, Sir.'); }, 500);
}
document.getElementById('boot').addEventListener('click', ()=>finishBoot());
document.addEventListener('keydown', ()=>{ if(!bootDone) finishBoot(); });

// --- steps nav
function renderSteps(){
  const el=document.getElementById('steps');
  el.innerHTML='';
  STEPS.forEach((s,idx)=>{
    const d=document.createElement('div');
    d.className='step'+(idx===current?' active':'')+(idx<current?' done':'');
    d.innerHTML=`<span class="n">${idx<current?'✓':idx+1}</span><span><b>${s.title}</b><br><small style="opacity:0.7">${s.desc}</small></span>`;
    d.onclick=()=>{ if(idx<=current) { current=idx; render(); } };
    el.appendChild(d);
  });
  document.getElementById('bar').style.width = Math.round((current)/(STEPS.length-1)*100)+'%';
  document.getElementById('pct').textContent = Math.round((current)/(STEPS.length-1)*100)+'%';
}

// --- left log
function leftLog(msg, cls=''){
  const el=document.getElementById('leftLog');
  const line=document.createElement('div');
  line.innerHTML=`<span class="mut">[${new Date().toLocaleTimeString()}]</span> <span class="${cls}">${msg}</span>`;
  el.appendChild(line); el.scrollTop=el.scrollHeight;
  if(el.children.length>60) el.removeChild(el.firstChild);
}
function rightLog(msg){
  const el=document.getElementById('rightLog');
  el.textContent = msg;
}

// --- toast
function toast(msg){
  const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 2600);
}

// --- views
function render(){
  renderSteps();
  const v=document.getElementById('view');
  const step=STEPS[current].id;

  if(step==='welcome'){
    v.innerHTML=`
      <div class="hero">
        <div class="label"><i></i> Stark Industries • Setup • Mark 49</div>
        <h1>Willkommen, <span>Sir</span>.</h1>
        <p>Dieser Setup-Assistent installiert <b>J.A.R.V.I.S.</b> – direkt wie in den YouTube-Videos: dunkles HUD, leuchtender Arc Reactor, 1-Klick Sprachanbindung. Kein Python nötig, Starter wird auf dem Desktop platziert. Du wirst durch einen kurzen qualitativen Fragebogen (8 Fragen) geführt – damit J.A.R.V.I.S. nicht nur deine Stimme, sondern dein Denken versteht.</p>
        <div class="kv" style="margin-top:12px; gap:6px">
          <span>Paket</span><strong>JARVIS-Setup.exe • 412 MB • offline-fähig</strong>
          <span>Quelle</span><strong>YouTube-authentisch • Rainmeter HUD + Arc Reactor</strong>
          <span>Enthalten</span><strong>Holografisches Dashboard • Voice (Whisper) • Browser-Automation</strong>
        </div>
        <div class="cta">
          <button class="btn primary" onclick="next()">Installation beginnen →</button>
          <button class="btn ghost" onclick="skipToInstall()">Überspringen (Demo)</button>
        </div>
      </div>
      <div class="card">
        <h3>Was dich erwartet (wie auf YouTube)</h3>
        <ul style="margin:0 0 0 16px; color:var(--muted); line-height:1.7; font-size:13px">
          <li>Schritt 2: System-Check – zeigt echte Diagnostik, simulierte Telemetrie</li>
          <li>Schritt 3: Qualitativer Fragebogen – 8 offene Fragen, min. 5 / max. 10 erfüllt</li>
          <li>Schritt 4: Voice Enrollment – 5× „Jarvis" sagen, Waveform live</li>
          <li>Schritt 5: Installation – 400 MB Python Libs + 40 MB Whisper, Fortschritts-HUD</li>
          <li>Am Ende: „J.A.R.V.I.S. ONLINE" + Desktop-Verknüpfung mit Cyan Icon</li>
        </ul>
      </div>
      <div class="card" style="display:flex; gap:10px; align-items:center">
        <span style="width:8px; height:8px; background:var(--gold); border-radius:50%; box-shadow:var(--gold-glow)"></span>
        <span style="font-family:'Share Tech Mono'; font-size:11px; letter-spacing:0.08em; color:var(--muted)">Hinweis: Windows SmartScreen Warnung ist normal – <b style="color:var(--text)">Mehr Infos → Trotzdem ausführen</b> (nicht code-signiert wie alle Community Builds).</span>
      </div>
    `;
    rightLog('Standby. Warte auf Start. — "Sometimes you gotta run before you can walk."');
  }

  if(step==='system'){
    // simulate checks
    v.innerHTML=`
      <div class="hero">
        <div class="label"><i></i> 02 • System Check</div>
        <h1>System <span>Diagnose</span></h1>
        <p>Prüfe Voraussetzungen. Rechts siehst du Live-Telemetrie – wie im Rainmeter Theme. Tests laufen automatisch.</p>
      </div>
      <div class="card" id="checks"></div>
      <div class="cta">
        <button class="btn ghost" onclick="prev()">← Zurück</button>
        <button class="btn primary" id="toFragen" disabled onclick="next()">Weiter zum Fragebogen →</button>
      </div>
    `;
    runChecks();
  }

  if(step==='fragen'){
    let validCount = answers.filter(a=>a.trim().length>=30).length;
    let all = answers.filter(a=>a.trim().length>0).length;
    v.innerHTML=`
      <div class="hero">
        <div class="label"><i></i> 03 • Qualitativer Fragebogen • 8 Fragen</div>
        <h1>Bevor J.A.R.V.I.S. deine <span>Stimme</span> lernt, lernt er dein Denken kennen.</h1>
        <p>Dies ist ein <b>qualitativer Fragebogen</b> – es geht um Verstehen, nicht Zählen. Offene Textfelder, keine Skalen. Mindestens 5 Fragen sollten beantwortet werden (30+ Zeichen), maximal 8. Du kannst überspringen, aber je ehrlicher du bist, desto persönlicher wird dein Assistent. Antworten werden lokal in <code>profile.json</code> gespeichert.</p>
        <div class="kv" style="margin-top:10px">
          <span>Fortschritt</span><strong id="qProg">${validCount} / ${QUESTIONS.length} gültig • ${all} ausgefüllt • Min:5</strong>
          <span>Typ</span><strong>Teilstandardisierter Leitfaden • Auswertung nach Mayring / Braun & Clarke</strong>
        </div>
        <div class="cta">
          <button class="btn ghost" onclick="exportCSV()">CSV exportieren</button>
          <button class="btn ghost" onclick="fillExample()">Beispiel ausfüllen</button>
        </div>
      </div>
      <div class="q" id="qList"></div>
      <div class="cta">
        <button class="btn ghost" onclick="prev()">← Zurück</button>
        <button class="btn primary" id="toVoice" ${validCount>=5?'':'disabled'} onclick="next()">${validCount>=5?'Weiter zur Stimme →':'Mind. 5 Fragen (30+ Zeichen)'}</button>
      </div>
      <div class="card" style="font-size:12px; color:var(--muted); line-height:1.6">
        <b style="color:var(--text)">Methodik:</b> Offenes, sondierendes Item-Design, Funneling breit→spezifisch, neutrale Formulierung („Was denken Sie?"). Pilotierung mit 5–10 Personen empfohlen. Auswertung: offen → axial → selektiv kodieren, Kernkategorie bilden.
      </div>
    `;
    const qList=document.getElementById('qList');
    QUESTIONS.forEach((item,i)=>{
      const div=document.createElement('div'); div.className='qitem';
      const len=answers[i].length;
      const ok=len>=30;
      div.innerHTML=`
        <h4>${i+1}. ${item.q} <em>${ok?'✓ gültig':len>0?`${len} Zeichen – noch ${30-len}`:'leer'}</em></h4>
        <div style="font-size:11px; color:var(--muted); margin-bottom:6px">${item.hint} • <i>${item.probe}</i></div>
        <textarea placeholder="Deine Worte – 30 Zeichen Minimum, 200–400 empfohlen..." data-i="${i}">${answers[i]}</textarea>
        <div class="hint"><span>${len} Zeichen</span><span class="counter">${ok?'Qualitative Tiefe erreicht':'mind. 30 Zeichen'}</span></div>
      `;
      qList.appendChild(div);
    });
    qList.querySelectorAll('textarea').forEach(ta=>{
      ta.addEventListener('input', e=>{
        const idx=parseInt(e.target.dataset.i);
        answers[idx]=e.target.value;
        // live update counter
        const h4=e.target.parentElement.querySelector('h4 em');
        const hint=e.target.parentElement.querySelector('.hint');
        const len=e.target.value.length;
        h4.textContent = len>=30?'✓ gültig': len>0?`${len} Zeichen – noch ${30-len}`:'leer';
        hint.innerHTML=`<span>${len} Zeichen</span><span class="counter">${len>=30?'Qualitative Tiefe erreicht':'mind. 30 Zeichen'}</span>`;
        e.target.classList.toggle('filled', len>=30);
        // update prog
        const vc=answers.filter(a=>a.trim().length>=30).length;
        const al=answers.filter(a=>a.trim().length>0).length;
        document.getElementById('qProg').textContent=`${vc} / ${QUESTIONS.length} gültig • ${al} ausgefüllt • Min:5`;
        const btn=document.getElementById('toVoice');
        if(vc>=5){ btn.disabled=false; btn.textContent='Weiter zur Stimme →'; }
        else { btn.disabled=true; btn.textContent=`Mind. 5 Fragen (30+ Zeichen) – jetzt ${vc}`; }
        localStorage.setItem('jarvis_answers', JSON.stringify(answers));
      });
      if(ta.value.length>=30) ta.classList.add('filled');
    });
    // restore from storage
    try{ const s=JSON.parse(localStorage.getItem('jarvis_answers')||'null'); if(s) answers=s; }catch{}
  }

  if(step==='voice'){
    v.innerHTML=`
      <div class="hero">
        <div class="label"><i></i> 04 • Stimme & Persona</div>
        <h1>Voice <span>Enrollment</span></h1>
        <p>Sage <b>5× „Jarvis"</b> – rechts schlägt die Waveform aus (34 Bars). Wir simulieren das wie im YouTube-Tutorial (Dmitri Voice, Silero-VAD). Unten wählst du Persona.</p>
      </div>
      <div class="card">
        <h3>Enroll</h3>
        <div class="kv">
          <span>Status</span><strong id="enrollStatus">Bereit – klicke „Zuhören starten"</strong>
          <span>Fortschritt</span><strong id="enrollProg">0 / 5 erkannt</strong>
        </div>
        <div class="cta">
          <button class="btn primary" id="listenBtn" onclick="toggleListen()">▶ Zuhören starten</button>
          <button class="btn ghost" onclick="simulateEnroll()">Simulieren (Demo)</button>
        </div>
        <div class="log" id="enrollLog" style="margin-top:10px; min-height:80px"></div>
      </div>
      <div class="card">
        <h3>Persona wählen</h3>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px">
          <label style="padding:10px; border:1px solid var(--border); border-radius:8px; background:rgba(0,217,255,0.06); cursor:pointer">
            <input type="radio" name="persona" checked> <b>Paul Bettany</b> – britisch, trocken, „Yes, Sir."
          </label>
          <label style="padding:10px; border:1px solid var(--border); border-radius:8px; cursor:pointer">
            <input type="radio" name="persona"> <b>FRIDAY</b> – weiblich, irisch, direkt
          </label>
          <label style="padding:10px; border:1px solid var(--border); border-radius:8px; cursor:pointer">
            <input type="radio" name="persona"> <b>Stark</b> – jung, frech, „Let's build."
          </label>
          <label style="padding:10px; border:1px solid var(--border); border-radius:8px; cursor:pointer">
            <input type="radio" name="persona"> <b>Custom</b> – ElevenLabs Voice ID einfügen
          </label>
        </div>
      </div>
      <div class="cta">
        <button class="btn ghost" onclick="prev()">← Zurück</button>
        <button class="btn primary" id="toInstall" onclick="next()">Weiter zur Installation →</button>
      </div>
    `;
  }

  if(step==='install'){
    v.innerHTML=`
      <div class="hero">
        <div class="label"><i></i> 05 • Installation</div>
        <h1>Installiere <span>J.A.R.V.I.S.</span></h1>
        <p>Wie im YouTube Setup: Python Embedded + Bibliotheken (~400 MB) + Offline Whisper (~39 MB) + Rainmeter Skin. Kein Admin nötig (per-user in <code>%LOCALAPPDATA%\\Programs\\JARVIS</code>).</p>
      </div>
      <div class="card">
        <h3>Schritte</h3>
        <div class="log" id="installLog" style="min-height:160px"></div>
        <div class="progress" style="margin-top:12px"><i id="installProgress" style="width:0%"></i></div>
        <div class="cta">
          <button class="btn primary" id="startInstall" onclick="startInstall()">Installation starten</button>
          <button class="btn ghost" onclick="prev()">← Zurück</button>
        </div>
      </div>
    `;
  }

  if(step==='done'){
    v.innerHTML=`
      <div class="hero" style="border-color:rgba(43,255,107,0.35)">
        <div class="label" style="color:#2BFF6B"><i style="background:#2BFF6B"></i> 06 • Online</div>
        <h1 style="color:#2BFF6B">J.A.R.V.I.S. <span style="color:#2BFF6B; text-shadow:0 0 12px rgba(43,255,107,0.6)">ONLINE</span></h1>
        <p>Guten Abend, Sir. Alle Systeme nominal. Dein Fragebogen wurde gespeichert – J.A.R.V.I.S. kennt jetzt deine Präferenzen. Desktop-Verknüpfung „J.A.R.V.I.S." wurde erstellt (Cyan Arc Reactor Icon). Sage <b>„Hey Jarvis"</b> oder klatsche zweimal.</p>
        <div class="cta">
          <button class="btn primary" style="background:#2BFF6B; border-color:#2BFF6B; color:#00220A" onclick="launchHUD()">HUD starten →</button>
          <button class="btn ghost" onclick="exportAll()">Alle Daten exportieren</button>
        </div>
      </div>
      <div class="card">
        <h3>Was jetzt?</h3>
        <ul style="margin:0 0 0 16px; color:var(--muted); line-height:1.7; font-size:13px">
          <li>Drücke <b style="color:var(--text)">Strg + J</b> überall um J.A.R.V.I.S. zu rufen</li>
          <li>Sage „Jarvis, öffne YouTube" / „Schreib eine E-Mail an..."</li>
          <li>Rainmeter: Rechtsklick Desktop → Iron Man → Jarvis.ini → Load</li>
          <li>Config liegt in <code>%APPDATA%\\JARVIS\\profile.json</code></li>
        </ul>
      </div>
      <div class="card">
        <h3>Dein qualitatives Profil (Vorschau)</h3>
        <pre id="profilePreview" style="background:rgba(2,10,20,0.8); border:1px solid var(--border); border-radius:8px; padding:12px; font-family:'JetBrains Mono'; font-size:11px; line-height:1.6; color:#8FB3CC; max-height:220px; overflow:auto"></pre>
      </div>
    `;
    const preview=document.getElementById('profilePreview');
    if(preview){
      const obj={};
      QUESTIONS.forEach((q,i)=> obj[`Frage ${i+1}`]=answers[i]||'(leer)');
      preview.textContent=JSON.stringify(obj,null,2);
    }
    document.getElementById('sysState').textContent='ONLINE • BEREIT';
    document.getElementById('arc').classList.remove('listening');
    toast('J.A.R.V.I.S. online. "Welcome home, Sir."');
  }
}

function next(){
  if(current < STEPS.length-1){ current++; render(); leftLog(`→ ${STEPS[current].title}`, 'ok'); }
}
function prev(){ if(current>0){ current--; render(); } }
function skipToInstall(){ current=4; render(); }

// --- checks simulation
function runChecks(){
  const checks=[
    {k:'OS', v:'Windows 11 Pro 64-bit (22631)', ok:true},
    {k:'RAM', v:'16 GB (15.8 verfügbar)', ok:true},
    {k:'CPU', v:'Intel i7-12700H • 14 Kerne', ok:true},
    {k:'GPU', v:'NVIDIA RTX 4060 • 8 GB VRAM', ok:true},
    {k:'Storage', v:'412 MB frei benötigt • 84 GB frei', ok:true},
    {k:'Microphone', v:'Standard Mic Array • 48 kHz', ok:true},
    {k:'Network', v:'Stark Satellite • 28 ms', ok:true},
  ];
  const el=document.getElementById('checks');
  el.innerHTML=`<div class="kv">${checks.map(c=>`<span>${c.k}</span><strong class="${c.ok?'ok':'bad'}">${c.v} • ${c.ok?'BEREIT':'FEHLER'}</strong>`).join('')}</div>`;
  leftLog('System-Check abgeschlossen – alle Systeme nominal.', 'ok');
  setTimeout(()=>{ document.getElementById('toFragen').disabled=false; }, 900);
}

// --- voice enrollment simulation
let listening=false;
function toggleListen(){
  listening=!listening;
  const btn=document.getElementById('listenBtn');
  const arc=document.getElementById('arc');
  const status=document.getElementById('enrollStatus');
  if(listening){
    arc.classList.add('listening');
    btn.textContent='■ Zuhören stoppen';
    btn.style.background='var(--red)'; btn.style.borderColor='var(--red)'; btn.style.color='white';
    status.textContent='Höre zu – sage „Jarvis" ...';
    leftLog('Voice pipeline: VAD aktiv, Whisper tiny.en bereit.', 'ok');
    // fake detections
    let c=0;
    window._enrollInt=setInterval(()=>{
      c++; document.getElementById('enrollProg').textContent=`${Math.min(c,5)} / 5 erkannt`;
      const log=document.getElementById('enrollLog');
      const line=document.createElement('div'); line.textContent=`[${new Date().toLocaleTimeString()}] „Jarvis" erkannt – Confidence 0.${92+Math.floor(Math.random()*6)} – Sample ${c}/5`;
      log.appendChild(line); log.scrollTop=log.scrollHeight;
      leftLog(`Voiceprint Sample ${c}/5 captured.`, 'ok');
      if(c>=5){ clearInterval(window._enrollInt); listening=false; arc.classList.remove('listening'); btn.textContent='✓ Enrolled – 5/5'; btn.disabled=true; status.textContent='Enrolled – Voiceprint gespeichert (data/voiceprint.json)'; toast('Voiceprint gespeichert – erkenne nur noch dich.'); if(document.getElementById('toInstall')) document.getElementById('toInstall').disabled=false; }
    }, 900);
  } else {
    arc.classList.remove('listening');
    btn.textContent='▶ Zuhören starten';
    btn.style.background=''; btn.style.borderColor=''; btn.style.color='';
    status.textContent='Pausiert';
    clearInterval(window._enrollInt);
  }
}
function simulateEnroll(){
  document.getElementById('enrollProg').textContent='5 / 5 erkannt';
  document.getElementById('enrollLog').textContent='[Demo] 5 Samples simuliert – Voiceprint.json geschrieben. In echtem EXE via Silero-VAD + Dmitri Stimme.';
  leftLog('Voiceprint simuliert – übersprungen (Demo).', 'ok');
}

// --- install simulation
const installStepsLogs=[
  'Entpacke Python 3.11 Embedded ...',
  'Pip install customtkinter pillow faster-whisper ... 412 MB',
  'Lade Whisper tiny.en ... 39 MB (offline STT)',
  'Lade Silero VAD + Dmitri Voice ... 18 MB',
  'Installiere Rainmeter Skin: JARVIS + SHIELD OS ...',
  'Schreibe Registry: Desktop Shortcut (Arc Reactor Icon) ...',
  'Schreibe config.yaml – API Adapter Groq/Gemini ...',
  'Speichere profile.json (8 Antworten, qualitativ) ...',
  'Teste Mikrofon – AnalyserNode 34 Bars ... OK',
  'Fertig. J.A.R.V.I.S. bereit.',
];
function startInstall(){
  const log=document.getElementById('installLog');
  const bar=document.getElementById('installProgress');
  const btn=document.getElementById('startInstall');
  btn.disabled=true; btn.textContent='Installiere ...';
  let i=0;
  const int=setInterval(()=>{
    const line=document.createElement('div');
    line.innerHTML=`<b>[${String(i+1).padStart(2,'0')}/10]</b> ${installStepsLogs[i]}`;
    log.appendChild(line); log.scrollTop=log.scrollHeight;
    leftLog(installStepsLogs[i], 'ok');
    bar.style.width = Math.round((i+1)/installStepsLogs.length*100)+'%';
    setWave(true);
    i++;
    if(i>=installStepsLogs.length){
      clearInterval(int);
      btn.textContent='✓ Fertig';
      setWave(false);
      setTimeout(()=>next(), 700);
    }
  }, 520);
}

// --- exports
function exportCSV(){
  let csv='Frage;Antwort\n';
  QUESTIONS.forEach((q,i)=> csv+=`"${i+1}. ${q.q.replace(/"/g,'""')}";"${(answers[i]||'').replace(/"/g,'""')}"\n`);
  const blob=new Blob([csv], {type:'text/csv;charset=utf-8;'});
  const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='jarvis_qualitativer_fragebogen.csv'; a.click();
  toast('CSV exportiert.');
}
function exportAll(){
  const obj={meta:{created:new Date().toISOString(), type:'qualitativer Fragebogen 8 Fragen', tool:'JARVIS-Setup.exe MARK 49'}, answers: {}};
  QUESTIONS.forEach((q,i)=> obj.answers[`F${i+1}`]={frage:q.q, antwort:answers[i]||null, chars:(answers[i]||'').length});
  const blob=new Blob([JSON.stringify(obj,null,2)], {type:'application/json'});
  const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='profile.json'; a.click();
  toast('profile.json exportiert.');
}
function fillExample(){
  const ex=[
    'Für mich ist JARVIS wie ein ruhiger Butler – er soll im Hintergrund arbeiten, nur sprechen wenn ich ihn rufe, und nie proaktiv dazwischenquatschen. Wie Alfred, nicht wie Clippy.',
    'Montag 7:32, ich bin spät: JARVIS hat schon meine Mails überflogen, sagt mir welche dringend sind, startet das Auto-Navi und legt die Präsentation auf den Desktop. Ich spare 12 Minuten.',
    'Always-On macht mir Angst wegen Firmen-Meetings und nachts. Mikrofon muss ein Hardware-Mute haben und lokal erkennen, nicht alles in die Cloud schicken.',
    'Ich will Paul Bettany – britisch, trocken, leicht humorvoll. Er darf widersprechen, aber nie belehren. Humor nur wenn ich humorvoll bin.',
    'Unverzichtbar: E-Mails zusammenfassen, Code erklären, Kalender. Spielerei: Games und Witze – nett, aber ich deinstalliere nicht wegen fehlendem TicTacToe.',
    'Sehr wichtig. Ohne das cyan Leuchten und den Reactor fühlt es sich nur wie ChatGPT an. Das HUD macht das Iron-Man-Gefühl – das ist der halbe Grund, es zu nutzen.',
    'Täglich nutzen würde ich ihn wenn er schnell ist (<1s), keine Abo-Kosten hat und sich Dinge über Wochen merkt. Deinstallieren bei Halluzinationen oder wenn er Daten leakt.',
    'Er soll meine Handbewegungen per Webcam verstehen – Minority-Report-Gesten für Fenster schieben. Gibt es in keinem Tutorial und wäre echte Magie.'
  ];
  answers=ex.slice();
  localStorage.setItem('jarvis_answers', JSON.stringify(answers));
  render(); toast('Beispiel ausgefüllt – 8/8 Fragen, alle gültig.');
}
function launchHUD(){
  toast('HUD gestartet – (Demo) öffne Dashboard...');
  window.open('https://github.com/OIIAdotexedotbruh/Veryoriginaljarvis', '_blank');
}

// init
leftLog('JARVIS Setup geladen – warte auf Boot...', 'mut');
rightLog('Diagnostik initialisiere ...');
