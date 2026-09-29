# DU-cluster

**The Dark Username Company — AI Business Operating System**

DU-cluster is a standalone control plane for an international, English-first digital-products business. It replaces the abandoned Make prototype with application code and explicit APIs.

## Core loop
Global trend intelligence → opportunity scoring → product factory → content factory → publishing → Shopify sales → analytics → optimization.

## Market
- International / English-first.
- Algeria is explicitly excluded as a viral/trend criterion.
- Primary opportunity domains: AI, technology, Linux, cybersecurity, automation, software, SaaS, creator tools, productivity and digital products.

## Integrations
Metricool, Shopify and Canva can be connected through provider APIs. Credentials are never hard-coded and actions are only marked complete after provider confirmation.

## Run
```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Open `web/index.html` for the dashboard concept or serve it with any static web server.

## Docker
```bash
docker compose up --build
```

## API
- GET /health
- GET /ready
- GET /api/v1/agent/status
- GET /api/v1/dashboard
- POST /api/v1/trends/analyze
- POST /api/v1/opportunities/evaluate
- POST /api/v1/agent/execute

## Business objective
The system is designed around a long-term **$1,000,000/month revenue objective**. This is a target, not a guaranteed result.

## Status
The repository contains the standalone v2 foundation, trend scoring engine, API control plane, dashboard, Docker runtime and architecture documentation. External production deployment and third-party credentials remain environment-dependent.
