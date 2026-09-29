from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class IntegrationStatus:
    name:str
    configured:bool
    mode:str

def statuses():
    return [
      IntegrationStatus("Metricool",bool(os.getenv("METRICOOL_API_KEY")),"api" if os.getenv("METRICOOL_API_KEY") else "connected-provider-required"),
      IntegrationStatus("Shopify",bool(os.getenv("SHOPIFY_STORE_DOMAIN") and os.getenv("SHOPIFY_ACCESS_TOKEN")),"api" if os.getenv("SHOPIFY_ACCESS_TOKEN") else "oauth-required"),
      IntegrationStatus("Canva",bool(os.getenv("CANVA_ACCESS_TOKEN")),"api" if os.getenv("CANVA_ACCESS_TOKEN") else "oauth-required"),
    ]
