from __future__ import annotations
import os
from dataclasses import dataclass
import httpx

@dataclass(frozen=True)
class MetricoolConfig:
    token:str
    user_id:str
    blog_id:str
    analytics_url:str

    @property
    def configured(self)->bool:
        return bool(self.token and self.user_id and self.blog_id and self.analytics_url)

def metricool_config()->MetricoolConfig:
    return MetricoolConfig(
        token=os.getenv("METRICOOL_API_TOKEN","").strip(),
        user_id=os.getenv("METRICOOL_USER_ID","").strip(),
        blog_id=os.getenv("METRICOOL_BLOG_ID","").strip(),
        analytics_url=os.getenv("METRICOOL_ANALYTICS_URL","").strip(),
    )

def fetch_metricool_analytics(from_date:str,to_date:str,params:dict|None=None)->dict:
    cfg=metricool_config()
    if not cfg.configured:
        return {"status":"not_configured","required":["METRICOOL_API_TOKEN","METRICOOL_USER_ID","METRICOOL_BLOG_ID","METRICOOL_ANALYTICS_URL"]}
    query={"userId":cfg.user_id,"blogId":cfg.blog_id,"from":from_date,"to":to_date,**(params or {})}
    r=httpx.get(cfg.analytics_url,params=query,headers={"X-Mc-Auth":cfg.token,"Content-Type":"application/json"},timeout=60)
    r.raise_for_status()
    return {"status":"ok","source":"metricool","data":r.json()}

@dataclass(frozen=True)
class IntegrationStatus:
    name:str
    configured:bool
    mode:str

def statuses():
    mc=metricool_config()
    return [
      IntegrationStatus("Metricool",mc.configured,"api" if mc.configured else "connected-provider-required"),
      IntegrationStatus("Shopify",bool(os.getenv("SHOPIFY_STORE_DOMAIN") and os.getenv("SHOPIFY_ACCESS_TOKEN")),"api" if os.getenv("SHOPIFY_ACCESS_TOKEN") else "oauth-required"),
      IntegrationStatus("Canva",bool(os.getenv("CANVA_ACCESS_TOKEN")),"api" if os.getenv("CANVA_ACCESS_TOKEN") else "oauth-required"),
    ]
