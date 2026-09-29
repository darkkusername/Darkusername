from __future__ import annotations
from dataclasses import dataclass
from .ai_gateway import AIGateway

@dataclass
class ContentFactory:
    ai:AIGateway
    def generate(self,topic:str,offer:str="")->dict:
        prompt=f"""Create an English-first international content package for: {topic}.
Offer: {offer or "relevant digital product"}
Return: YouTube title+outline, Short hook+script, TikTok/Reel hook+script, Instagram carousel outline, CTA, SEO keywords.
Adapt each format; do not duplicate identical copy. Do not invent factual claims."""
        return self.ai.generate("You are DU-cluster Content Producer. Be factual, useful and non-deceptive.",prompt)
