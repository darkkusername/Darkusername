from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .schemas import Opportunity, UnitEconomics
from .orchestrator import VentureOrchestrator
from .security import require_api_key
from .trends import analyze, top_opportunities
from .pipeline import BusinessPipeline
from .memory_store import init_memory, put, get, list_namespace
from .content_factory import ContentFactory
from .product_factory import ProductFactory
from .ai_gateway import AIGateway
from .integrations import statuses, integration_health, fetch_metricool_analytics, shopify_summary, canva_me
from .publishing import schedule_content
from .ops import system_status
import os, httpx, json
from .db import (
    init_db, save_trends, save_run, recent_trends, recent_runs,
    save_performance_event, recent_performance, performance_summary,
    save_business_record, recent_business_records, save_opportunity, recent_opportunities, save_integration_sync, recent_integration_syncs,
)

app=FastAPI(title="DU-cluster",version="2.4.0",description="International English-first AI Business Operating System")
cors_origins=[x.strip() for x in os.getenv("CORS_ORIGINS","*").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=cors_origins,allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
orchestrator=VentureOrchestrator()
pipeline=BusinessPipeline()
ai=AIGateway()
content_factory=ContentFactory(ai)
product_factory=ProductFactory(ai)
init_db()
init_memory()
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/health")
def health():
    return {"status":"ok","service":"DU-cluster","version":"2.3.0"}

@app.get("/ready")
def ready():
    return {"status":"ready","service":"DU-cluster","mode":"standalone","storage":"sqlite","ai_provider_configured":ai.configured}

@app.get("/api/v1/ops/status",dependencies=[Depends(require_api_key)])
def ops_status():
    return system_status()

@app.get("/api/v1/agent/status")
def agent_status():
    return {
        "agent":"DU-cluster",
        "mode":"autonomous-control-plane",
        "market":"international",
        "language":"en",
        "algeria_as_trend_criterion":False,
        "agents":["TrendScout","OpportunityAnalyzer","ProductStrategist","ProductBuilder","ContentStrategist","ContentProducer","QAAgent","Publisher","AnalyticsAgent","Optimizer"],
    }

@app.post("/api/v1/opportunities/evaluate",dependencies=[Depends(require_api_key)])
def evaluate(opportunity:Opportunity,economics:UnitEconomics):
    result=orchestrator.run(opportunity,economics)
    record=save_opportunity({"opportunity":opportunity.model_dump(),"economics":economics.model_dump(),"decision":result})
    return {"record":record,"decision":result}

@app.post("/api/v1/trends/analyze",dependencies=[Depends(require_api_key)])
def analyze_trends(payload:dict):
    items=payload.get("signals",[])
    if not isinstance(items,list):
        raise HTTPException(400,"signals must be an array")
    result=analyze(items)
    save_trends(result)
    return {"market":"international","language":"en","signals":result}

@app.post("/api/v1/trends/ingest",dependencies=[Depends(require_api_key)])
def trends_ingest():
    key=os.getenv("SERPAPI_KEY","").strip()
    if not key:
        raise HTTPException(503,"SERPAPI_KEY is not configured")
    params={"engine":"google_trends_trending_now","geo":os.getenv("TREND_GEO","US"),"hl":"en","hours":24,"api_key":key}
    r=httpx.get("https://serpapi.com/search.json",params=params,timeout=45)
    r.raise_for_status()
    data=r.json()
    raw=data.get("trending_searches",data.get("trending_searches_results",[]))
    signals=[]
    for x in raw:
        if isinstance(x,dict):
            q=x.get("query") or x.get("title")
            if q:
                signals.append({"topic":q,"recency_signal":90,"why_now":"Fresh international English-language trending signal."})
    result=analyze(signals)
    save_trends(result)
    return {"market":"international","language":"en","geo":params["geo"],"count":len(result),"signals":result}

@app.get("/api/v1/trends/recent",dependencies=[Depends(require_api_key)])
def trends_recent():
    return {"signals":recent_trends()}

@app.get("/api/v1/trends/opportunities",dependencies=[Depends(require_api_key)])
def trend_opportunities(limit:int=10):
    rows=recent_trends(max(10,limit*5))
    items=[json.loads(r["payload"]) for r in rows]
    return {"market":"international","language":"en","opportunities":top_opportunities(items,limit)}

@app.post("/api/v1/agent/execute",dependencies=[Depends(require_api_key)])
def execute(payload:dict):
    task=str(payload.get("task","")).strip()
    if not task:
        raise HTTPException(400,"task is required")
    context=payload.get("context") or {}
    run_id=f"run-{os.urandom(6).hex()}"
    result=pipeline.run(task,context)
    status="completed" if result["results"] and result["results"][-1]["status"]=="completed" else "provider_not_configured"
    put("runs",run_id,{"task":task,"status":status,"results":result["results"]})
    save_run(task,status,result)
    return {"run_id":run_id,"status":status,"task":task,"results":result["results"]}

@app.post("/api/v1/pipeline/run",dependencies=[Depends(require_api_key)])
def pipeline_run(payload:dict):
    task=str(payload.get("task","")).strip()
    if not task:
        raise HTTPException(400,"task is required")
    result=pipeline.run(task,payload.get("context") or {})
    save_run(task,result["results"][-1]["status"],result)
    return result

@app.post("/api/v1/products/generate",dependencies=[Depends(require_api_key)])
def generate_product(payload:dict):
    topic=str(payload.get("topic","")).strip()
    if not topic:
        raise HTTPException(400,"topic is required")
    result=product_factory.generate(topic,str(payload.get("audience","")))
    record=save_business_record("products",{"topic":topic,"audience":str(payload.get("audience","")),"result":result})
    return {"record":record,"generation":result}

@app.get("/api/v1/products/recent",dependencies=[Depends(require_api_key)])
def products_recent(limit:int=50):
    return {"items":recent_business_records("products",limit)}

@app.post("/api/v1/content/generate",dependencies=[Depends(require_api_key)])
def generate_content(payload:dict):
    topic=str(payload.get("topic","")).strip()
    if not topic:
        raise HTTPException(400,"topic is required")
    result=content_factory.generate(topic,str(payload.get("offer","")))
    record=save_business_record("content_assets",{"topic":topic,"offer":str(payload.get("offer","")),"result":result})
    return {"record":record,"generation":result}

@app.get("/api/v1/content/recent",dependencies=[Depends(require_api_key)])
def content_recent(limit:int=50):
    return {"items":recent_business_records("content_assets",limit)}

@app.post("/api/v1/analytics/event",dependencies=[Depends(require_api_key)])
def analytics_event(payload:dict):
    platform=str(payload.get("platform","")).strip()
    content_id=str(payload.get("content_id","")).strip()
    metric=str(payload.get("metric","")).strip()
    if not platform or not content_id or not metric:
        raise HTTPException(400,"platform, content_id and metric are required")
    try:
        value=float(payload.get("value"))
    except (TypeError,ValueError):
        raise HTTPException(400,"value must be numeric")
    save_performance_event(platform,content_id,metric,value,payload)
    return {"status":"recorded","platform":platform,"content_id":content_id,"metric":metric,"value":value}

@app.get("/api/v1/analytics/recent",dependencies=[Depends(require_api_key)])
def analytics_recent(limit:int=100):
    return {"events":recent_performance(min(max(limit,1),500))}

@app.get("/api/v1/analytics/summary",dependencies=[Depends(require_api_key)])
def analytics_summary(limit:int=500):
    return {"source":"measured_performance_events","summary":performance_summary(min(max(limit,1),2000))}

@app.post("/api/v1/optimizer/run",dependencies=[Depends(require_api_key)])
def optimizer_run(payload:dict):
    from .agents_v2 import AgentRuntime
    runtime=AgentRuntime()
    summary=performance_summary(500)
    task=str(payload.get("task","Optimize content and product performance using the measured KPI summary.")).strip()
    context={"measured_kpis":summary,"rule":"Use only measured data; clearly label hypotheses and do not invent missing metrics."}
    result=runtime.execute("Analyze KPI evidence, identify measurable experiments and next actions.",context,agent="Optimizer")
    record=save_business_record("experiments",{"task":task,"evidence":summary,"result":result})
    return {"optimizer":"Optimizer","status":result["status"],"task":task,"evidence":summary,"experiment_record":record,"result":result}

@app.get("/api/v1/opportunities/recent",dependencies=[Depends(require_api_key)])
def opportunities_recent(limit:int=50):
    return {"items":recent_opportunities(limit)}

@app.get("/api/v1/optimizer/experiments",dependencies=[Depends(require_api_key)])
def optimizer_experiments(limit:int=50):
    return {"items":recent_business_records("experiments",limit)}

@app.get("/api/v1/integrations/status",dependencies=[Depends(require_api_key)])
def integration_status():
    return {"integrations":[s.__dict__ for s in statuses()],"health":integration_health()}

@app.post("/api/v1/integrations/metricool/sync",dependencies=[Depends(require_api_key)])
def metricool_sync(payload:dict):
    result=fetch_metricool_analytics(str(payload.get("from","")),str(payload.get("to","")),payload.get("params") or {})
    save_integration_sync("Metricool",result.get("status","unknown"),result)
    return result

@app.get("/api/v1/integrations/shopify/summary",dependencies=[Depends(require_api_key)])
def shopify_integration_summary():
    result=shopify_summary()
    save_integration_sync("Shopify",result.get("status","unknown"),result)
    return result

@app.get("/api/v1/integrations/canva/me",dependencies=[Depends(require_api_key)])
def canva_integration_me():
    result=canva_me()
    save_integration_sync("Canva",result.get("status","unknown"),result)
    return result

@app.get("/api/v1/integrations/syncs",dependencies=[Depends(require_api_key)])
def integration_syncs(limit:int=50):
    return {"items":recent_integration_syncs(limit)}

@app.put("/api/v1/memory/{namespace}/{key}",dependencies=[Depends(require_api_key)])
def memory_put(namespace:str,key:str,payload:dict):
    put(namespace,key,payload)
    return {"status":"saved","namespace":namespace,"key":key}

@app.get("/api/v1/memory/{namespace}",dependencies=[Depends(require_api_key)])
def memory_list(namespace:str):
    return {"namespace":namespace,"items":list_namespace(namespace)}

@app.get("/api/v1/agent/runs",dependencies=[Depends(require_api_key)])
def agent_runs():
    return {"runs":recent_runs()}

@app.post("/api/v1/publishing/schedule",dependencies=[Depends(require_api_key)])
def publishing_schedule(payload:dict):
    result=schedule_content(payload)
    if result.get("status")=="invalid":
        raise HTTPException(400,result.get("error","invalid publishing payload"))
    return result

@app.get("/api/v1/publishing/recent",dependencies=[Depends(require_api_key)])
def publishing_recent(limit:int=50):
    return {"items":recent_business_records("publishing_jobs",limit)}

@app.get("/api/v1/dashboard")
def dashboard():
    return {
        "brand":"DU-cluster",
        "target":"$1M/month business objective",
        "market":"International",
        "language":"English",
        "kpis":["traffic","leads","conversion","AOV","repeat_purchase"],
        "integrations":["Metricool","Shopify","Canva"],
        "automation":"standalone",
    }
