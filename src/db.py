from __future__ import annotations
import json, sqlite3
from pathlib import Path
from datetime import datetime, timezone
DB_PATH=Path("data/ducluster.db")
DB_PATH.parent.mkdir(parents=True,exist_ok=True)
def connect():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
    with connect() as c:
        c.executescript("""CREATE TABLE IF NOT EXISTS trend_signals(id INTEGER PRIMARY KEY AUTOINCREMENT,topic TEXT NOT NULL,score REAL NOT NULL,priority TEXT NOT NULL,payload TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS agent_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,task TEXT NOT NULL,status TEXT NOT NULL,result TEXT NOT NULL,created_at TEXT NOT NULL);""")
def save_trends(items):
    now=datetime.now(timezone.utc).isoformat()
    with connect() as c:
        for x in items: c.execute("INSERT INTO trend_signals(topic,score,priority,payload,created_at) VALUES(?,?,?,?,?)",(x["topic"],x["opportunity_score"],x["priority"],json.dumps(x),now))
def save_run(task,status,result):
    with connect() as c: c.execute("INSERT INTO agent_runs(task,status,result,created_at) VALUES(?,?,?,?)",(task,status,json.dumps(result),datetime.now(timezone.utc).isoformat()))
def recent_trends(limit=20):
    with connect() as c: return [dict(r) for r in c.execute("SELECT * FROM trend_signals ORDER BY id DESC LIMIT ?",(limit,))]
def recent_runs(limit=20):
    with connect() as c: return [dict(r) for r in c.execute("SELECT * FROM agent_runs ORDER BY id DESC LIMIT ?",(limit,))]
