from src.schemas import Opportunity, UnitEconomics
from src.scoring import opportunity_score

def test_opportunity_score():
 o=Opportunity(id='1',market='x',problem='p',audience='a',demand=80,competition=20,margin=90,recurring_potential=80,development_complexity=20,evidence=['a','b'])
 assert opportunity_score(o)>75

def test_ltv():
 u=UnitEconomics(price_eur=49,gross_margin=.85,monthly_churn=.07,cac_eur=60,arpu_eur=49,months_lifetime=14)
 assert round(u.ltv_eur,2)==583.1
 assert u.ltv_cac>9
