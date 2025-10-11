import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import fnmatch

class Config:
    """Handles configuration loading and merging from mltiple sources."""
    
    DEFAULT_CONFIG = {
        "mode": "dev",
        "timeout": 10,
        "concurrency": 50,
        "ignore_patterns": [],
        "exclude_urls": [],
        "strict_ssl": False,
    }
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_file = project_root / "linkguard.config.json"
        self.ignore_file = project_root / ".linkguardignore"
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        
    