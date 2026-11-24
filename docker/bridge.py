# -*- coding: utf-8 -*-
"""
Runs a persistent bore TCP tunnel from the local Docker PostgreSQL container to Render,
and pushes the active TLS Postgres URL to Render's live bot and environment config.
"""

import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

PG_USER = os.getenv("PG_USER", "satbot")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")
PG_DB = os.getenv("PG_DB", "sat_master")
PG_HOST = os.getenv("PG_HOST", "postgres")
PG_PORT = os.getenv("PG_PORT", "5432")
BORE_SERVER = os.getenv("BORE_SERVER", "bore.pub")
RENDER_APP_URL = os.getenv("RENDER_APP_URL", "https://sat-master-bot.onrender.com").rstrip("/")
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
RENDER_API_KEY = os.getenv("RENDER_API_KEY", "").strip()
RENDER_SERVICE_ID = os.getenv("RENDER_SERVICE_ID", "").strip()

LISTEN_RE = re.compile(r"listening at ([^\s:]+):(\d+)")
REMOTE_PORT_RE = re.compile(r"remote_port\s*=\s*(\d+)")

_state_lock = threading.Lock()
_current_db_url: str | None = None


def log(msg: str) -> None:
    print(f"[bridge] {msg}", flush=True)


def http_json(method: str, url: str, payload: dict | None = None, headers: dict | None = None, timeout: int = 20) -> tuple[int, dict]:
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
        return resp.status, (json.loads(raw) if raw else {})


def build_db_url(public_host: str, public_port: str) -> str:
    user = urllib.parse.quote(PG_USER, safe="")
    password = urllib.parse.quote(PG_PASSWORD, safe="")
    return f"postgresql://{user}:{password}@{public_host}:{public_port}/{PG_DB}?sslmode=require"


def push_to_live_bot(db_url: str) -> bool:
    url = f"{RENDER_APP_URL}/internal/database-url"
    for attempt in range(1, 6):
        try:
            status, body = http_json(
                "POST",
                url,
                payload={"database_url": db_url},
                headers={"Authorization": f"Bearer {BOT_TOKEN}"},
                timeout=30,
            )
            if status == 200:
                log(f"Render live bot switched to local Docker Postgres (HTTP 200): {body}")
                return True
            log(f"Unexpected live bot response HTTP {status}: {body}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            log(f"Attempt {attempt}/5 live bot HTTP {e.code}: {err_body}")
        except Exception as e:
            log(f"Attempt {attempt}/5 failed notifying live bot: {e}")
        time.sleep(min(attempt * 3, 12))
    return False


def update_render_env_var(db_url: str) -> None:
    if not RENDER_API_KEY or not RENDER_SERVICE_ID:
        return
    url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/env-vars/DATABASE_URL"
    try:
        status, _ = http_json(
            "PUT",
            url,
            payload={"value": db_url},
            headers={"Authorization": f"Bearer {RENDER_API_KEY}"},
            timeout=20,
        )
        log(f"Persisted DATABASE_URL on Render env vars (HTTP {status}).")
    except urllib.error.HTTPError as e:
        log(f"Render env var update HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
    except Exception as e:
        log(f"Failed persisting Render env var: {e}")


def register_tunnel(public_host: str, public_port: str) -> None:
    db_url = build_db_url(public_host, public_port)
    with _state_lock:
        global _current_db_url
        _current_db_url = db_url
    log(f"Tunnel active at {public_host}:{public_port} -> local {PG_HOST}:{PG_PORT}")
    # Wait briefly for bore remote listener to accept traffic before Render connects.
    time.sleep(1.5)
    push_to_live_bot(db_url)
    update_render_env_var(db_url)


def heartbeat_loop() -> None:
    health_url = f"{RENDER_APP_URL}/health"
    while True:
        time.sleep(60)
        with _state_lock:
            db_url = _current_db_url
        if not db_url:
            continue
        try:
            status, body = http_json("GET", health_url, timeout=20)
            if status == 200 and body.get("storage") == "postgres" and body.get("database") is True:
                continue
            log(f"Render health shows storage={body.get('storage')} database={body.get('database')}; re-pushing URL...")
            push_to_live_bot(db_url)
        except urllib.error.HTTPError as e:
            log(f"Health heartbeat HTTP {e.code}; re-pushing URL...")
            push_to_live_bot(db_url)
        except Exception as e:
            log(f"Health heartbeat check error: {e}")


def run_bore_forever() -> None:
    cmd = ["bore", "local", str(PG_PORT), "--to", BORE_SERVER, "--local-host", PG_HOST]
    while True:
        log(f"Starting tunnel: {' '.join(cmd)}")
        with _state_lock:
            global _current_db_url
            _current_db_url = None
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        registered = False
        assert proc.stdout is not None
        for line in proc.stdout:
            text = line.rstrip()
            if text:
                log(f"bore: {text}")
            if not registered:
                m = LISTEN_RE.search(text)
                if m:
                    registered = True
                    threading.Thread(target=register_tunnel, args=(m.group(1), m.group(2)), daemon=True).start()
                    continue
                m2 = REMOTE_PORT_RE.search(text)
                if m2:
                    registered = True
                    threading.Thread(target=register_tunnel, args=(BORE_SERVER, m2.group(1)), daemon=True).start()
        code = proc.wait()
        log(f"bore exited with code {code}; restarting in 3s...")
        time.sleep(3)


def main() -> None:
    if not BOT_TOKEN or not PG_PASSWORD:
        log("BOT_TOKEN and PG_PASSWORD must be set in .env.docker")
        sys.exit(1)
    threading.Thread(target=heartbeat_loop, daemon=True).start()
    run_bore_forever()


if __name__ == "__main__":
    main()
