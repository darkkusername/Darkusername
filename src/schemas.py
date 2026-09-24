from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field

def now(): return datetime.now(timezone.utc)

class Stage(str, Enum):
    DISCOVER='discover'; SCORE='score'; BUILD='build'; TEST='test'; LAUNCH='launch'; MEASURE='measure'; SCALE='scale'; KILL='kill'

class Opportunity(BaseModel):
    id: str; market: str; problem: str; audience: str
    demand: float = Field(ge=0, le=100)
    competition: float = Field(ge=0, le=100)
    margin: float = Field(ge=0, le=100)
    recurring_potential: float = Field(ge=0, le=100)
    development_complexity: float = Field(ge=0, le=100)
    evidence: list[str] = []

class UnitEconomics(BaseModel):
    price_eur: float = Field(gt=0); gross_margin: float = Field(gt=0, le=1)
    monthly_churn: float = Field(ge=0, lt=1); cac_eur: float = Field(ge=0)
    arpu_eur: float = Field(gt=0); months_lifetime: float = Field(gt=0)
    @property
    def ltv_eur(self): return self.arpu_eur * self.gross_margin * self.months_lifetime
    @property
    def ltv_cac(self): return self.ltv_eur / self.cac_eur if self.cac_eur else float('inf')

class Decision(BaseModel):
    opportunity_id: str; score: float; stage: Stage; action: str; reasons: list[str]
    requires_human: bool = False; created_at: datetime = Field(default_factory=now)

class Experiment(BaseModel):
    id: str; name: str; budget_eur: float; success_metric: str; kill_condition: str; status: str = 'planned'
