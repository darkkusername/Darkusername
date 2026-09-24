import json
from pathlib import Path
from .config import settings

class Memory:
    def __init__(self, path=None):
        self.path = Path(path or settings.database_path); self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists(): self.path.write_text(json.dumps({'events': [], 'decisions': []}, indent=2))
    def _load(self): return json.loads(self.path.read_text())
    def append(self, bucket, item):
        data=self._load(); data.setdefault(bucket, []).append(item); self.path.write_text(json.dumps(data, indent=2, default=str))
    def all(self, bucket): return self._load().get(bucket, [])
