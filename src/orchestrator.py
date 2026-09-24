from .agents import CEOAgent, MarketIntelligenceAgent, ProductManagerAgent, CFOAgent, RiskAgent
from .memory import Memory
from .schemas import Opportunity, UnitEconomics, Decision, Stage

class VentureOrchestrator:
    def __init__(self,memory=None):
        self.memory=memory or Memory(); self.ceo=CEOAgent(); self.market=MarketIntelligenceAgent(); self.product=ProductManagerAgent(); self.cfo=CFOAgent(); self.risk=RiskAgent()
    def run(self,opportunity,economics):
        results={'market':self.market.analyze(opportunity).output,'product':self.product.specify(opportunity).output,'cfo':self.cfo.evaluate(economics).output,'risk':self.risk.evaluate(opportunity).output}
        d0=self.ceo.decide(opportunity,economics)
        stage={'BUILD':Stage.BUILD,'VALIDATE':Stage.TEST,'KILL':Stage.KILL,'HOLD':Stage.DISCOVER}[d0['action']]
        d=Decision(opportunity_id=opportunity.id,score=d0['score'],stage=stage,action=d0['action'],reasons=d0['reasons'])
        self.memory.append('decisions',d.model_dump())
        return {'decision':d.model_dump(),'agents':results}
