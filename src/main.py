from fastapi import Depends, FastAPI, HTTPException
from .schemas import Opportunity, UnitEconomics
from .orchestrator import VentureOrchestrator
from .security import require_api_key
from .trends import analyze

app = FastAPI(title="DU-cluster", version="2.0.0", description="International English-first AI Business Operating System")
orchestrator = VentureOrchestrator()

@app.get("/health")
def health():
    return {"status": "ok", "service": "DU-cluster", "version": "2.0.0"}

@app.get("/ready")
def ready():
    return {"status": "ready", "service": "DU-cluster", "mode": "standalone"}

@app.get("/api/v1/agent/status")
def agent_status():
    return {"agent":"DU-cluster","mode":"autonomous-control-plane","market":"international","language":"en","algeria_as_trend_criterion":False}

@app.post("/api/v1/opportunities/evaluate", dependencies=[Depends(require_api_key)])
def evaluate(opportunity: Opportunity, economics: UnitEconomics):
    return orchestrator.run(opportunity, economics)

@app.post("/api/v1/trends/analyze", dependencies=[Depends(require_api_key)])
def analyze_trends(payload: dict):
    items = payload.get("signals", [])
    if not isinstance(items, list):
        raise HTTPException(400, "signals must be an array")
    return {"market":"international","language":"en","signals":analyze(items)}

@app.post("/api/v1/agent/execute", dependencies=[Depends(require_api_key)])
def execute(payload: dict):
    task = str(payload.get("task","")).strip()
    if not task:
        raise HTTPException(400, "task is required")
    return {"status":"accepted","task":task,"next":"Route through specialized agents: TrendScout, OpportunityAnalyzer, ProductBuilder, ContentProducer, Publisher, AnalyticsAgent, Optimizer."}

@app.get("/api/v1/dashboard")
def dashboard():
    return {"brand":"DU-cluster","target":"$1M/month business objective","market":"International","language":"English","kpis":["traffic","leads","conversion","AOV","repeat_purchase"],"integrations":["Metricool","Shopify","Canva"],"automation":"standalone; Make removed"}
