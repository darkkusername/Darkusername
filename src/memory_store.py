from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
DB_PATH=Path("data/ducluster.db")
DB_PATH.parent.mkdir(parents=True,exist_ok=True)
def _db():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_memory():
    with _db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS agent_memory(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          namespace TEXT NOT NULL,
          key TEXT NOT NULL,
          value TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          UNIQUE(namespace,key)
        )""")
def put(namespace:str,key:str,value:object):
    init_memory()
    with _db() as c:
        c.execute("""INSERT INTO agent_memory(namespace,key,value,updated_at)
          VALUES(?,?,?,?)
          ON CONFLICT(namespace,key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at""",
          (namespace,key,json.dumps(value),datetime.now(timezone.utc).isoformat()))
def get(namespace:str,key:str):
    init_memory()
    with _db() as c:
        r=c.execute("SELECT value FROM agent_memory WHERE namespace=? AND key=?",(namespace,key)).fetchone()
    return json.loads(r["value"]) if r else None
def list_namespace(namespace:str):
    init_memory()
    with _db() as c:
        rows=c.execute("SELECT key,value,updated_at FROM agent_memory WHERE namespace=? ORDER BY updated_at DESC",(namespace,)).fetchall()
    return [{"key":r["key"],"value":json.loads(r["value"]),"updated_at":r["updated_at"]} for r in rows]
