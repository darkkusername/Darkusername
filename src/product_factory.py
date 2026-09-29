from __future__ import annotations
from dataclasses import dataclass
from .ai_gateway import AIGateway

@dataclass
class ProductFactory:
    ai:AIGateway
    def generate(self,topic:str,audience:str="")->dict:
        prompt=f"""Design a digital product around {topic} for an international English-speaking audience.
Audience: {audience or "technology-focused creators, developers and learners"}.
Return product promise, target problem, contents, deliverables, lead magnet, low-ticket offer, core offer, bundle/upsell, pricing hypotheses and QA checklist. Clearly mark hypotheses."""
        return self.ai.generate("You are DU-cluster Product Strategist. Never fabricate demand or revenue evidence.",prompt)
