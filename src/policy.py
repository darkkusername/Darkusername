from .config import settings
from .schemas import Opportunity
SENSITIVE_ACTIONS={'spend_money','publish','production_deploy','legal_claim'}
def requires_human(action): return settings.approval_mode != 'fully_autonomous' and action in SENSITIVE_ACTIONS
def approve_experiment(budget_eur):
    if budget_eur <= 0: return False, 'Budget must be positive.'
    if budget_eur > settings.max_experiment_eur: return False, 'Budget exceeds experiment limit.'
    return True, 'Within configured experiment limit.'
def safety_check(o: Opportunity):
    reasons=[]
    if not o.problem.strip(): reasons.append('Empty problem statement.')
    if not o.evidence: reasons.append('No evidence supplied; research required before launch.')
    return len(reasons)==0, reasons
