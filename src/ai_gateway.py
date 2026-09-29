from __future__ import annotations
import os
from typing import Any
import httpx

class AIGateway:
    """Provider-agnostic JSON/text gateway. No provider call is made unless configured."""
    def __init__(self):
        self.provider=os.getenv("AI_PROVIDER","").strip().lower()
        self.model=os.getenv("AI_MODEL","").strip()
        self.api_key=os.getenv("AI_API_KEY","").strip()
        self.base_url=os.getenv("AI_BASE_URL","").strip().rstrip("/")

    @property
    def configured(self)->bool:
        return bool(self.provider and self.model and self.api_key and self.base_url)

    def generate(self, system: str, user: str, temperature: float=0.2)->dict[str,Any]:
        if not self.configured:
            return {"status":"not_configured","provider":self.provider or None,"model":self.model or None}
        payload={"model":self.model,"messages":[{"role":"system","content":system},{"role":"user","content":user}],"temperature":temperature}
        r=httpx.post(self.base_url+"/chat/completions",headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"},json=payload,timeout=60)
        r.raise_for_status()
        data=r.json()
        return {"status":"ok","provider":self.provider,"model":self.model,"content":data["choices"][0]["message"]["content"],"raw":data}
