from .schemas import Opportunity, UnitEconomics
from .orchestrator import VentureOrchestrator
if __name__=='__main__':
 o=Opportunity(id='demo-ai-prompts',market='AI productivity',problem='Beginners struggle to turn AI into repeatable workflows.',audience='freelancers and small digital businesses',demand=82,competition=48,margin=92,recurring_potential=75,development_complexity=30,evidence=['search demand','customer interviews'])
 u=UnitEconomics(price_eur=49,gross_margin=.85,monthly_churn=.07,cac_eur=60,arpu_eur=49,months_lifetime=14)
 print(VentureOrchestrator().run(o,u))
