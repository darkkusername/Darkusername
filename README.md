# AI Venture Factory

Autonomous digital-product venture operating system for the Dark Username project.

Mission: market signal -> validated product -> distribution -> sales -> analytics -> optimization.

V1 principles:
- Human-controlled financial, production, legal and publication gates.
- Provider-agnostic LLM layer.
- Make-compatible webhooks.
- GitHub-first product artifacts.
- No artificial engagement or platform manipulation.
- Every experiment has a budget, success metric and kill condition.

Quick start:
1. Copy .env.example to .env.
2. Install Python 3.11+.
3. pip install -r requirements.txt
4. python -m src.main
5. Run python -m src.demo for a deterministic decision example.

Repository structure: src/ contains the control plane, agents, scoring, memory and policy; prompts/ contains agent system prompts; docs/ contains architecture; tests/ contains deterministic tests.

Production deployment still requires external credentials, hosting and payment/social integrations; those are deliberately not hard-coded.
