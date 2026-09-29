from fastapi import Depends, FastAPI, HTTPException\nfrom fastapi.staticfiles import StaticFiles
from .schemas import Opportunity, UnitEconomics
from .orchestrator import VentureOrchestrator
from .security import require_api_key
from .trends import analyze
from .pipeline import BusinessPipeline
from .memory_store import init_memory, put, get, list_namespace
from .content_factory import ContentFactory
from .product_factory import ProductFactory
from .ai_gateway import AIGateway
from .integrations import statuses\nfrom .ops import system_status\nimport os, httpx
from .db import init_db, save_trends, save_run, recent_trends, recent_runs
app=FastAPI(title="DU-cluster",version="2.2.0",description="International English-first AI Business Operating System")
orchestrator=VentureOrchestrator(); pipeline=BusinessPipeline(); ai=AIGateway(); content_factory=ContentFactory(ai); product_factory=ProductFactory(ai); init_db(); init_memory()\napp.mount("/web", StaticFiles(directory="web"), name="web")
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
@app.post("/api/v1/trends/ingest",dependencies=[Depends(require_api_key)])
def trends_ingest():
    key=os.getenv("SERPAPI_KEY","").strip()
    if not key: raise HTTPException(503,"SERPAPI_KEY is not configured")
    params={"engine":"google_trends_trending_now","geo":os.getenv("TREND_GEO","US"),"hl":"en","hours":24,"api_key":key}
    r=httpx.get("https://serpapi.com/search.json",params=params,timeout=45)
    r.raise_for_status(); data=r.json()
    raw=data.get("trending_searches",data.get("trending_searches_results",[]))
    signals=[]
    for x in raw:
        if isinstance(x,dict):
            q=x.get("query") or x.get("title")
            if q: signals.append({"topic":q,"recency_signal":90,"why_now":"Fresh international English-language trending signal."})
    result=analyze(signals); save_trends(result)
    return {"market":"international","language":"en","geo":params["geo"],"count":len(result),"signals":result}
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
@app.post("/api/v1/products/generate",dependencies=[Depends(require_api_key)])
def generate_product(payload:dict):
    topic=str(payload.get("topic","")).strip()
    if not topic: raise HTTPException(400,"topic is required")
    return product_factory.generate(topic,str(payload.get("audience","")))

@app.post("/api/v1/content/generate",dependencies=[Depends(require_api_key)])
def generate_content(payload:dict):
    topic=str(payload.get("topic","")).strip()
    if not topic: raise HTTPException(400,"topic is required")
    return content_factory.generate(topic,str(payload.get("offer","")))

@app.get("/api/v1/integrations/status",dependencies=[Depends(require_api_key)])
def integration_status():
    return {"integrations":[s.__dict__ for s in statuses()]}

@app.put("/api/v1/memory/{namespace}/{key}",dependencies=[Depends(require_api_key)])
def memory_put(namespace:str,key:str,payload:dict):
    put(namespace,key,payload)
    return {"status":"saved","namespace":namespace,"key":key}

@app.get("/api/v1/memory/{namespace}",dependencies=[Depends(require_api_key)])
def memory_list(namespace:str):
    return {"namespace":namespace,"items":list_namespace(namespace)}

@app.get("/api/v1/agent/runs",dependencies=[Depends(require_api_key)])
def agent_runs(): return {"runs":recent_runs()}
@app.get("/api/v1/dashboard")
def dashboard(): return {"brand":"DU-cluster","target":"$1M/month business objective","market":"International","language":"English","kpis":["traffic","leads","conversion","AOV","repeat_purchase"],"integrations":["Metricool","Shopify","Canva"],"automation":"standalone; Make removed"}
