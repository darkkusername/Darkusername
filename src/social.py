from dataclasses import dataclass
from enum import Enum

class Platform(str, Enum):
    YOUTUBE='youtube'; TIKTOK='tiktok'; INSTAGRAM='instagram'

@dataclass
class SocialPost:
    platform: Platform
    text: str
    media_url: str | None = None
    scheduled_for: str | None = None

class SocialPolicy:
    """Platform-safe publishing policy. Never simulates engagement or creates spam accounts."""
    max_posts_per_asset = 1
    def validate(self, post: SocialPost):
        if not post.text.strip(): raise ValueError('Post text cannot be empty')
        return {'ok': True, 'platform': post.platform.value}
