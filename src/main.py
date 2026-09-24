from fastapi import Depends, FastAPI
from .schemas import Opportunity, UnitEconomics
from .orchestrator import VentureOrchestrator
from .security import require_api_key

app = FastAPI(title="AI Venture Factory", version="1.1.0")
orchestrator = VentureOrchestrator()

@app.get("/health")
def health():
    return {"status": "ok", "service": "AI Venture Factory", "version": "1.1.0"}

@app.get("/ready")
def ready():
    return {"status": "ready", "service": "AI Venture Factory"}

@app.post("/opportunities/evaluate", dependencies=[Depends(require_api_key)])
def evaluate(opportunity: Opportunity, economics: UnitEconomics):
    return orchestrator.run(opportunity, economics)
