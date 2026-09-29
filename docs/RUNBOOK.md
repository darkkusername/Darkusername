# DU-cluster Runbook

## Local
Install Python 3.11+, run `pip install -r requirements.txt`, configure `.env`, then run `uvicorn src.main:app --reload`.

## Production
Use a secret manager, HTTPS, PostgreSQL, a durable queue such as Redis/Celery, backups, monitoring, rate limits and authenticated access. External publishing remains preview/approval-first until provider confirmation and explicit autonomous mode are implemented.

## Operating loop
Global English trend signals -> scoring -> opportunity -> product -> content -> QA -> publishing -> sales -> analytics -> optimization.

## Market rules
International and English-first. Algeria is not a trend criterion. Local-only signals are ignored unless clearly internationally relevant.

## Truthfulness
Never claim a publication, sale, API action, metric or provider result without confirmation. Revenue targets are planning objectives, not guarantees.
