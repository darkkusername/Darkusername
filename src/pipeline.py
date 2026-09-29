from __future__ import annotations
from .agents_v2 import AgentRuntime

class BusinessPipeline:
    def __init__(self): self.runtime=AgentRuntime()

    def run(self, task:str, context:dict|None=None)->dict:
        stages=[
            ("trend","Validate international English-first demand signals."),
            ("opportunity","Convert validated signals into monetizable opportunities."),
            ("product","Design the product, offer and lead magnet."),
            ("content","Create platform-specific content angles."),
            ("qa","Check factual accuracy, policy, brand and publishing readiness."),
        ]
        results=[]
        for name,instruction in stages:
            r=self.runtime.execute(f"{instruction}\nUser task: {task}",context)
            results.append({"stage":name,**r})
            if r["status"]=="provider_not_configured":
                break
        return {"pipeline":"DU-cluster","task":task,"results":results}
