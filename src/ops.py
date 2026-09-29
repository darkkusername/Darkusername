from __future__ import annotations
import os
from .ai_gateway import AIGateway
from .integrations import statuses

def system_status():
    ai=AIGateway()
    return {
      "service":"DU-cluster",
      "mode":"standalone",
      "ai_provider_configured":ai.configured,
      "integrations":[s.__dict__ for s in statuses()],
      "environment":{"python":os.getenv("PYTHON_VERSION","runtime"),"database":os.getenv("DATABASE_URL","sqlite:///data/ducluster.db")}
    }
