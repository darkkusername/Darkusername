# DU-cluster

The Dark Username Company — AI Business Operating System.

Standalone international, English-first control plane for digital products.

Core loop: global trend intelligence -> opportunity scoring -> product factory -> content factory -> publishing -> Shopify sales -> analytics -> optimization.

Market: International / English-first. Algeria is excluded as a viral/trend criterion. Focus: AI, technology, Linux, cybersecurity, automation, software, SaaS, creator tools, productivity and digital products.

Runtime: Python 3.11+, FastAPI, SQLite development persistence, Docker-ready. The persistence layer is isolated so production can move to PostgreSQL without changing the API contract.

API: /health, /ready, /api/v1/agent/status, /api/v1/dashboard, /api/v1/trends/analyze, /api/v1/trends/recent, /api/v1/opportunities/evaluate, /api/v1/agent/execute, /api/v1/agent/runs.

Integrations: Metricool, Shopify and Canva. Credentials are never hard-coded and actions are only marked complete after provider confirmation.

Business objective: $1,000,000/month is a long-term target, not a guarantee.

Status: DU-cluster v2.1 foundation includes API control plane, international trend scoring, persistent local state, dashboard, Docker runtime, tests and integration contracts. Production hosting and third-party API execution remain environment-dependent.
