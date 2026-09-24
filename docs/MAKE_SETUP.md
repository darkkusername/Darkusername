# Make production handoff

The Make organization/team was detected and the existing Dark Nomad Autonomous AI Agent scenario is active. Its current OpenAI connection is healthy.

## Social gateway
Create/activate a Custom Webhook scenario named `AI Venture Factory — Social Distribution Gateway`. The webhook accepts JSON:

`{ "job_id":"...", "platform":"youtube|tiktok|instagram", "content":"...", "media_url":"https://...", "scheduled_for":"ISO-8601", "campaign_id":"..." }`

Route each platform to its approved connector. Credentials must be connected by the owner in Make. Do not place API tokens in GitHub or webhook payloads.

## Production modules
- YouTube: Upload Video / Update Video Details / Set Thumbnail.
- TikTok: Content Posting API through an approved Make HTTP/custom integration or publishing provider.
- Instagram: authorized Meta publishing integration or approved publishing provider.

## Reliability
Use sequential processing where ordering matters, retry transient errors, log post ids, and keep a dead-letter path for failed jobs. Make webhooks process incoming requests immediately by default and can be configured for sequential processing.
