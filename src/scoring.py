from .schemas import Opportunity, UnitEconomics

def opportunity_score(o: Opportunity) -> float:
    return round(0.30*o.demand + 0.25*o.margin + 0.20*o.recurring_potential + 0.15*(100-o.competition) + 0.10*(100-o.development_complexity), 2)

def economics_score(u: UnitEconomics) -> float:
    return round((min(u.ltv_cac, 8.0)/8)*100, 2)
