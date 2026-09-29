from fastapi import Depends, FastAPI, HTTPException
from .schemas import Opportunity, UnitEconomics
from .orchestrator import VentureOrchestrator
from .security import require_api_key
from .trends import analyze
from .pipeline import BusinessPipeline
from .db import init_db, save_trends, save_run, recent_trends, recent_runs
app=FastAPI(title="DU-cluster",version="2.1.0",description="International English-first AI Business Operating System")
orchestrator=VentureOrchestrator(); pipeline=BusinessPipeline(); init_db()
@app.get("/health")
def health(): return {"status":"ok","service":"DU-cluster","version":"2.1.0"}
@app.get("/ready")
def ready(): return {"status":"ready","service":"DU-cluster","mode":"standalone","storage":"sqlite"}
@app.get("/api/v1/agent/status")
def agent_status(): return {"agent":"DU-cluster","mode":"autonomous-control-plane","market":"international","language":"en","algeria_as_trend_criterion":False,"agents":["TrendScout","OpportunityAnalyzer","ProductStrategist","ProductBuilder","ContentStrategist","ContentProducer","QAAgent","Publisher","AnalyticsAgent","Optimizer"]}
@app.post("/api/v1/opportunities/evaluate",dependencies=[Depends(require_api_key)])
def evaluate(opportunity:Opportunity,economics:UnitEconomics): return orchestrator.run(opportunity,economics)
@app.post("/api/v1/trends/analyze",dependencies=[Depends(require_api_key)])
def analyze_trends(payload:dict):
    items=payload.get("signals",[])
    if not isinstance(items,list): raise HTTPException(400,"signals must be an array")
    result=analyze(items); save_trends(result); return {"market":"international","language":"en","signals":result}
@app.get("/api/v1/trends/recent",dependencies=[Depends(require_api_key)])
def trends_recent(): return {"signals":recent_trends()}
@app.post("/api/v1/agent/execute",dependencies=[Depends(require_api_key)])
def execute(payload:dict):
    task=str(payload.get("task","")).strip()
    if not task: raise HTTPException(400,"task is required")
    result={"status":"accepted","task":task,"next":"Route through specialized agents and require provider confirmation before external actions."}
    save_run(task,"accepted",result); return result
@app.post("/api/v1/pipeline/run",dependencies=[Depends(require_api_key)])
def pipeline_run(payload:dict):
    task=str(payload.get("task","")).strip()
    if not task: raise HTTPException(400,"task is required")
    result=pipeline.run(task,payload.get("context") or {})
    save_run(task,result["results"][-1]["status"],result)
    return result
@app.get("/api/v1/agent/runs",dependencies=[Depends(require_api_key)])
def agent_runs(): return {"runs":recent_runs()}
@app.get("/api/v1/dashboard")
def dashboard(): return {"brand":"DU-cluster","target":"$1M/month business objective","market":"International","language":"English","kpis":["traffic","leads","conversion","AOV","repeat_purchase"],"integrations":["Metricool","Shopify","Canva"],"automation":"standalone; Make removed"}
