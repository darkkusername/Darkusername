from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Any
import httpx

@dataclass(frozen=True)
class MetricoolConfig:
    token: str
    user_id: str
    blog_id: str
    analytics_url: str

    @property
    def configured(self) -> bool:
        return bool(self.token and self.user_id and self.blog_id and self.analytics_url)

def metricool_config() -> MetricoolConfig:
    return MetricoolConfig(
        token=os.getenv("METRICOOL_API_TOKEN", "").strip(),
        user_id=os.getenv("METRICOOL_USER_ID", "").strip(),
        blog_id=os.getenv("METRICOOL_BLOG_ID", "").strip(),
        analytics_url=os.getenv("METRICOOL_ANALYTICS_URL", "").strip(),
    )

def fetch_metricool_analytics(from_date: str, to_date: str, params: dict | None = None) -> dict:
    cfg = metricool_config()
    if not cfg.configured:
        return {"status": "not_configured", "required": ["METRICOOL_API_TOKEN", "METRICOOL_USER_ID", "METRICOOL_BLOG_ID", "METRICOOL_ANALYTICS_URL"]}
    query = {"userId": cfg.user_id, "blogId": cfg.blog_id, "from": from_date, "to": to_date, **(params or {})}
    r = httpx.get(cfg.analytics_url, params=query, headers={"X-Mc-Auth": cfg.token, "Accept": "application/json"}, timeout=60)
    r.raise_for_status()
    return {"status": "ok", "source": "metricool", "data": r.json()}

def shopify_configured() -> bool:
    return bool(os.getenv("SHOPIFY_STORE_DOMAIN", "").strip() and os.getenv("SHOPIFY_ACCESS_TOKEN", "").strip())

def shopify_graphql(query: str, variables: dict | None = None) -> dict[str, Any]:
    domain = os.getenv("SHOPIFY_STORE_DOMAIN", "").strip().replace("https://", "").rstrip("/")
    token = os.getenv("SHOPIFY_ACCESS_TOKEN", "").strip()
    version = os.getenv("SHOPIFY_API_VERSION", "2026-07").strip()
    if not domain or not token:
        return {"status": "not_configured", "required": ["SHOPIFY_STORE_DOMAIN", "SHOPIFY_ACCESS_TOKEN"]}
    url = f"https://{domain}/admin/api/{version}/graphql.json"
    r = httpx.post(url, headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"}, json={"query": query, "variables": variables or {}}, timeout=60)
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        return {"status": "provider_error", "source": "shopify", "errors": data["errors"]}
    return {"status": "ok", "source": "shopify", "data": data.get("data", {})}

def shopify_summary() -> dict[str, Any]:
    query = """query {
      shop { name myshopifyDomain }
      products(first: 10) { nodes { id title status } }
    }"""
    return shopify_graphql(query)

def canva_configured() -> bool:
    return bool(os.getenv("CANVA_ACCESS_TOKEN", "").strip())

def canva_me() -> dict[str, Any]:
    token = os.getenv("CANVA_ACCESS_TOKEN", "").strip()
    if not token:
        return {"status": "not_configured", "required": ["CANVA_ACCESS_TOKEN"]}
    r = httpx.get(
        "https://api.canva.com/rest/v1/users/me",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    return {"status": "ok", "source": "canva", "data": r.json()}

@dataclass(frozen=True)
class IntegrationStatus:
    name: str
    configured: bool
    mode: str

def statuses():
    mc = metricool_config()
    return [
        IntegrationStatus("Metricool", mc.configured, "api" if mc.configured else "provider-credentials-required"),
        IntegrationStatus("Shopify", shopify_configured(), "api" if shopify_configured() else "provider-credentials-required"),
        IntegrationStatus("Canva", canva_configured(), "api" if canva_configured() else "provider-credentials-required"),
    ]

def integration_health() -> dict[str, Any]:
    return {
        "metricool": {"configured": metricool_config().configured},
        "shopify": {"configured": shopify_configured()},
        "canva": {"configured": canva_configured()},
    }
