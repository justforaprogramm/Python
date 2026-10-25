#!/usr/bin/env python3
"""Gamepad Vibrations-Test als Webapp (Linux).

Installation:  pip install flask pygame
Start:         python3 vibration_tester.py
Aufruf:        http://localhost:5000
"""
import os
import threading
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", "1")

import pygame
from flask import Flask, jsonify, request

app = Flask(__name__)

lock = threading.Lock()
state = {
    "pads": [],          # [{"id": int, "name": str, "rumble": bool}]
    "selected": None,    # Gamepad-Index oder None
    "strength": 255,     # 1..255
    "balance": 50,       # 0..100 (0 = nur tiefer Motor, 100 = nur hoher Motor)
    "running": False,
}


def controller_loop():
    """Besitzt pygame/SDL komplett: Gamepads scannen und Rumble senden."""
    pygame.init()
    pygame.joystick.init()
    joysticks = {}
    last_scan = 0.0
    last_rumble = 0.0
    active = None  # aktuell vibrierendes Joystick-Objekt

    while True:
        pygame.event.pump()
        now = time.time()

        if now - last_scan > 1.0:
            last_scan = now
            joysticks = {}
            pads = []
            for i in range(pygame.joystick.get_count()):
                try:
                    js = pygame.joystick.Joystick(i)
                    joysticks[i] = js
                    pads.append({"id": i, "name": js.get_name()})
                except pygame.error:
                    pass
            with lock:
                state["pads"] = pads
                if state["selected"] not in joysticks:
                    state["selected"] = None
                    state["running"] = False

        with lock:
            sel = state["selected"]
            running = state["running"]
            strength = state["strength"] / 255.0
            balance = state["balance"] / 100.0

        js = joysticks.get(sel)

        # Wechsel des Geräts oder Aus: altes Gerät stoppen
        if active is not None and (not running or js is not active):
            try:
                active.stop_rumble()
            except pygame.error:
                pass
            active = None

        if running and js is not None and now - last_rumble > 0.4:
            last_rumble = now
            low = strength * min(1.0, 2 * (1 - balance))
            high = strength * min(1.0, 2 * balance)
            try:
                js.rumble(low, high, 1000)
                active = js
            except pygame.error:
                pass

        time.sleep(0.05)


@app.get("/api/state")
def get_state():
    with lock:
        return jsonify(state)


@app.post("/api/set")
def set_state():
    data = request.get_json(force=True)
    with lock:
        if "selected" in data:
            state["selected"] = data["selected"]
            state["running"] = False
        if "strength" in data:
            state["strength"] = max(1, min(255, int(data["strength"])))
        if "balance" in data:
            state["balance"] = max(0, min(100, int(data["balance"])))
        if "running" in data:
            state["running"] = bool(data["running"]) and state["selected"] is not None
        return jsonify(state)


PAGE = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gamepad Vibrations-Test</title>
<style>
  :root { --pink: #ff4081; --pink-dark: #8e2250; --bg: #121212; --fg: #fff; }
  * { box-sizing: border-box; }
  body { margin: 0; min-height: 100vh; background: var(--bg); color: var(--fg);
         font-family: system-ui, sans-serif; display: flex; flex-direction: column; padding: 16px; }
  h1 { font-size: 1.4rem; margin: 0 0 12px; }
  .row { display: flex; gap: 8px; }
  select, button { font: inherit; border-radius: 8px; padding: 10px 14px; }
  select { flex: 1; background: var(--bg); color: var(--fg); border: 2px solid var(--pink); }
  button { background: var(--pink); color: #000; border: none; cursor: pointer; font-weight: 600; }
  button:disabled { background: var(--pink-dark); cursor: default; }
  main { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; }
  .slider { width: min(85%, 480px); }
  input[type=range] { width: 100%; accent-color: var(--pink); }
  #toggle { margin-top: 24px; padding: 14px 40px; font-size: 1.1rem; }
  small { opacity: .7; }
</style>
</head>
<body>
  <h1>Gamepad Vibrations-Test</h1>
  <div class="row">
    <select id="pad"></select>
    <button id="reload">Neu laden</button>
  </div>
  <main>
    <div id="none">Kein Gamepad ausgewählt</div>
    <div id="controls" class="slider" hidden>
      <div>Stärke: <span id="sv">255</span>/255</div>
      <input id="strength" type="range" min="1" max="255" value="255">
      <div style="margin-top:16px">Motor-Balance: <span id="bv">50</span> %
        <small>(0 = tief, 100 = hoch)</small></div>
      <input id="balance" type="range" min="0" max="100" value="50">
      <div style="text-align:center"><button id="toggle">An</button></div>
    </div>
  </main>
<script>
const $ = id => document.getElementById(id);
let running = false, lastKey = "";

async function post(body) {
  const r = await fetch("/api/set", {method: "POST", headers: {"Content-Type": "application/json"},
                                     body: JSON.stringify(body)});
  return r.json();
}

function render(s) {
  const key = JSON.stringify(s.pads) + s.selected;
  if (key !== lastKey) {
    lastKey = key;
    $("pad").innerHTML = "";
    const ph = new Option(s.pads.length ? "Gamepad wählen ▾" : "Kein Gamepad gefunden", "");
    $("pad").add(ph);
    s.pads.forEach(p => $("pad").add(new Option(p.name, p.id)));
    $("pad").value = s.selected === null ? "" : s.selected;
  }
  const has = s.selected !== null;
  $("none").hidden = has;
  $("controls").hidden = !has;
  running = s.running;
  $("toggle").textContent = running ? "Aus" : "An";
}

async function poll() { render(await (await fetch("/api/state")).json()); }

$("pad").onchange = async e => render(await post({selected: e.target.value === "" ? null : +e.target.value}));
$("reload").onclick = poll;
$("strength").oninput = e => { $("sv").textContent = e.target.value; post({strength: +e.target.value}); };
$("balance").oninput = e => { $("bv").textContent = e.target.value; post({balance: +e.target.value}); };
$("toggle").onclick = async () => render(await post({running: !running}));

poll();
setInterval(poll, 1000);
</script>
</body>
</html>
"""


@app.get("/")
def index():
    return PAGE


if __name__ == "__main__":
    threading.Thread(target=controller_loop, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, threaded=True)