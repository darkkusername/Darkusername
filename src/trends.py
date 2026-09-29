from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import re

FOCUS = ("ai","artificial intelligence","technology","linux","cybersecurity","automation","software","saas","creator","productivity","digital product","developer","python","cloud","open source")

@dataclass
class TrendSignal:
    topic: str
    why_now: str
    recency_signal: float
    international_relevance: float
    audience_relevance: float
    content_potential: float
    monetization_potential: float
    product_fit: float
    urgency: float
    competition_risk: float
    opportunity_score: float
    priority: str
    angles: dict[str,str]
    offers: dict[str,str]
    next_action: str

def _clamp(v: float) -> float:
    return max(0.0, min(100.0, round(v, 2)))

def score_signal(item: dict[str, Any]) -> TrendSignal | None:
    topic = str(item.get("topic") or item.get("query") or "").strip()
    if not topic:
        return None
    text = topic.lower()
    if any(x in text for x in ("algeria","algerian","algiers","football","celebrity gossip")):
        return None
    relevance = 85.0 if any(k in text for k in FOCUS) else 45.0
    recency = float(item.get("recency_signal", 80))
    audience = float(item.get("audience_relevance", relevance))
    content = float(item.get("content_potential", 75))
    monetization = float(item.get("monetization_potential", 65))
    product = float(item.get("product_fit", 70))
    urgency = float(item.get("urgency", 75))
    competition = float(item.get("competition_risk", 40))
    score = _clamp((recency + relevance + audience + content + monetization + product + urgency) / 7 - competition * .15)
    priority = "NOW" if score >= 75 else "NEXT" if score >= 55 else "WATCH"
    return TrendSignal(
        topic=topic,
        why_now=str(item.get("why_now") or "Fresh international English-language signal."),
        recency_signal=_clamp(recency), international_relevance=_clamp(relevance),
        audience_relevance=_clamp(audience), content_potential=_clamp(content),
        monetization_potential=_clamp(monetization), product_fit=_clamp(product),
        urgency=_clamp(urgency), competition_risk=_clamp(competition),
        opportunity_score=score, priority=priority,
        angles={
            "youtube": f"{topic}: what changed, why it matters, and practical applications",
            "short": f"3 things creators/developers should know about {topic}",
            "reel_tiktok": f"Fast explainer: {topic}",
            "carousel": f"{topic}: 7 practical takeaways"
        },
        offers={
            "lead_magnet": f"Free practical checklist: {topic}",
            "low_ticket": f"{topic} Starter Kit",
            "core_product": f"{topic} Master Playbook",
            "bundle": f"{topic} Creator & Automation Bundle",
            "saas": f"Workflow assistant for {topic}"
        },
        next_action=f"Validate demand and create one English-first content test for {topic} within 24 hours."
    )

def normalize_topic(topic: str) -> str:
    topic = re.sub(r"\\s+", " ", topic.lower()).strip()
    return re.sub(r"[^a-z0-9+#. -]", "", topic)

def deduplicate(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for item in items:
        topic = str(item.get("topic") or item.get("query") or "").strip()
        key = normalize_topic(topic)
        if not key:
            continue
        current = groups.get(key)
        if current is None or float(item.get("recency_signal", 0)) > float(current.get("recency_signal", 0)):
            groups[key] = {**item, "topic": topic}
    return list(groups.values())

def analyze(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored = [score_signal(x) for x in deduplicate(items)]
    result = [asdict(x) for x in scored if x]
    return sorted(result, key=lambda x: x["opportunity_score"], reverse=True)

def top_opportunities(items: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    return analyze(items)[:max(1, limit)]
