from __future__ import annotations
from dataclasses import dataclass
from .ai_gateway import AIGateway

SYSTEM="""You are DU-cluster, an international English-first AI business operating system.
Primary domains: AI, technology, Linux, cybersecurity, automation, software, SaaS, creator tools, productivity and digital products.
Never use Algeria or Algerian popularity as a trend criterion. Exclude local-only signals unless globally relevant.
Do not invent metrics, sources, customer data or completed external actions. Do not create fake engagement or deceptive clickbait.
Return practical structured business intelligence."""

@dataclass
class AgentResult:
    agent: str
    result: dict

class AgentRuntime:
    def __init__(self):
        self.ai=AIGateway()

    def execute(self, task:str, context:dict|None=None)->dict:
        context=context or {}
        result=self.ai.generate(SYSTEM,f"Task: {task}\nContext: {context}")
        return {"status":"completed" if result["status"]=="ok" else "provider_not_configured","task":task,"agent":"DU-cluster","result":result}
