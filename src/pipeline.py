from __future__ import annotations
from .agents_v2 import AgentRuntime

STAGES=[
    ("trend","TrendScout","Validate current international English-first demand signals. Return only evidence present in the supplied context or clearly mark hypotheses."),
    ("opportunity","OpportunityAnalyzer","Convert validated signals into monetizable opportunities. Separate measured facts from hypotheses."),
    ("product","ProductStrategist","Design a product ladder: lead magnet, entry offer, core product, bundle/recurring offer. Do not claim demand or revenue without evidence."),
    ("content","ContentProducer","Create platform-native English content for YouTube, Shorts, TikTok/Reels and Instagram. Do not duplicate copy and do not use deceptive clickbait."),
    ("qa","QAAgent","Check factual accuracy, international scope, brand alignment, policy/safety and publishing readiness. Flag unsupported claims."),
    ("optimizer","Optimizer","Define measurable KPIs, experiments and feedback loops. Treat the $1M/month objective as a target, never a guarantee."),
]

class BusinessPipeline:
    def __init__(self):
        self.runtime=AgentRuntime()

    def run(self,task:str,context:dict|None=None)->dict:
        context=dict(context or {})
        results=[]
        previous={}
        for name,agent,instruction in STAGES:
            stage_context={**context,"previous_stage":previous,"pipeline_stage":name}
            r=self.runtime.execute(f"{instruction}\nUser task: {task}",stage_context)
            item={"stage":name,"agent":agent,**r}
            results.append(item)
            previous=item.get("result",{})
            if r["status"]=="provider_not_configured":
                return {"pipeline":"DU-cluster","task":task,"status":"provider_not_configured","completed_stages":[x["stage"] for x in results[:-1]],"blocked_at":name,"results":results}
        return {"pipeline":"DU-cluster","task":task,"status":"completed","completed_stages":[x["stage"] for x in results],"results":results}
