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
CREATE TABLE IF NOT EXISTS agent_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,task TEXT NOT NULL,status TEXT NOT NULL,result TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS performance_events(id INTEGER PRIMARY KEY AUTOINCREMENT,platform TEXT NOT NULL,content_id TEXT NOT NULL,metric TEXT NOT NULL,value REAL NOT NULL,observed_at TEXT NOT NULL,payload TEXT NOT NULL);""")
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

def save_performance_event(platform:str,content_id:str,metric:str,value:float,payload:dict|None=None):
    with connect() as c:
        c.execute("INSERT INTO performance_events(platform,content_id,metric,value,observed_at,payload) VALUES(?,?,?,?,?,?)",
                  (platform,content_id,metric,float(value),datetime.now(timezone.utc).isoformat(),json.dumps(payload or {})))

def recent_performance(limit=100):
    with connect() as c:
        return [dict(r) for r in c.execute("SELECT * FROM performance_events ORDER BY id DESC LIMIT ?",(limit,))]

def performance_summary(limit=500):
    rows=recent_performance(limit)
    groups={}
    for r in rows:
        key=(r["platform"],r["content_id"],r["metric"])
        g=groups.setdefault(key,{"platform":r["platform"],"content_id":r["content_id"],"metric":r["metric"],"values":[]})
        g["values"].append(float(r["value"]))
    out=[]
    for g in groups.values():
        vals=g["values"]
        out.append({**{k:g[k] for k in ("platform","content_id","metric")},
                    "observations":len(vals),"latest":vals[0],"average":round(sum(vals)/len(vals),4),
                    "min":min(vals),"max":max(vals)})
    return out
