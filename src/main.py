from fastapi import FastAPI
from .schemas import Opportunity, UnitEconomics
from .orchestrator import VentureOrchestrator
app=FastAPI(title='AI Venture Factory',version='1.0.0'); orchestrator=VentureOrchestrator()
@app.get('/health')
def health(): return {'status':'ok','service':'AI Venture Factory'}
@app.post('/opportunities/evaluate')
def evaluate(opportunity: Opportunity,economics: UnitEconomics): return orchestrator.run(opportunity,economics)
