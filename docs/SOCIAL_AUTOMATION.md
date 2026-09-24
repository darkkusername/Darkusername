# Social Distribution Layer

## Supported architecture
The system prepares one canonical content asset, then creates platform-specific variants and sends them through approved APIs or a connected publishing provider.

### YouTube
Use OAuth and the YouTube Data API/Make YouTube module for authorized uploads, metadata and thumbnails. YouTube requires an authorized OAuth application for uploads.

### TikTok
Use TikTok Content Posting API. Direct posting requires creator authorization and the app's required review/audit path; unaudited clients can be restricted to private visibility.

### Instagram
Use Meta's authorized publishing APIs for eligible professional accounts. Keep credentials in Make keychains/secrets, never in GitHub.

### Make
Recommended flow:
1. Custom webhook receives a content job.
2. Validate schema and campaign id.
3. Route by platform.
4. Publish through a connected provider/API.
5. Store post id/status.
6. Return result.

Do not automate fake engagement, account farms, repetitive spam, or evasion of platform limits. The growth engine optimizes genuine content, testing and conversion.
