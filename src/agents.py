from dataclasses import dataclass
from .schemas import Opportunity, UnitEconomics
from .scoring import opportunity_score, economics_score
from .policy import safety_check

@dataclass
class AgentResult: agent: str; output: dict
class MarketIntelligenceAgent:
    name='market_intelligence'
    def analyze(self,o): return AgentResult(self.name, {'evidence_count':len(o.evidence),'research_required':len(o.evidence)<2})
class ProductManagerAgent:
    name='product_manager'
    def specify(self,o): return AgentResult(self.name, {'problem':o.problem,'audience':o.audience,'mvp':['core outcome','onboarding','payment/lead capture','analytics'],'validation':['landing-page test','customer interviews','paid or pre-order signal']})
class CFOAgent:
    name='cfo'
    def evaluate(self,u): return AgentResult(self.name, {'ltv_eur':round(u.ltv_eur,2),'ltv_cac':round(u.ltv_cac,2),'economics_score':economics_score(u)})
class RiskAgent:
    name='risk'
    def evaluate(self,o):
        ok,reasons=safety_check(o); return AgentResult(self.name, {'pass':ok,'reasons':reasons})
class CEOAgent:
    name='ceo'
    def decide(self,o,u):
        score=opportunity_score(o); eco=economics_score(u); risk_ok,risk_reasons=safety_check(o)
        if not risk_ok: return {'score':score,'action':'HOLD','reasons':risk_reasons}
        if score>=75 and eco>=60: return {'score':score,'action':'BUILD','reasons':['Strong opportunity score','Economics pass']}
        if score>=55: return {'score':score,'action':'VALIDATE','reasons':['Promising but requires validation']}
        return {'score':score,'action':'KILL','reasons':['Opportunity score below build threshold']}
