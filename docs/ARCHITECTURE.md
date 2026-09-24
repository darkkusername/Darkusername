# AI Venture Factory Architecture

Control plane: CEO agent is a decision layer, not an unrestricted executor. Specialist agents produce evidence and plans. Policy gates control sensitive actions.

Agents: CEO, Market Intelligence, Product Manager, Developer, Designer, Copywriter, Growth, Data Analyst, CFO, Risk/QA.

State machine: DISCOVER -> SCORE -> BUILD -> TEST -> LAUNCH -> MEASURE -> SCALE or KILL.

Make integration: call POST /opportunities/evaluate from a webhook, then route BUILD to the product-factory scenario, VALIDATE to research, and HOLD/KILL to logging. The repository does not fabricate credentials.

Scaling: replace JSON memory with PostgreSQL, add Redis/task queue, object storage, observability and secrets management before high-volume production.
