import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import fnmatch


class Config:
    """Handles configuration loading and merging from multiple sources."""

    DEFAULT_CONFIG: Dict[str, Any] = {
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
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file and ignore file."""
        # Load JSON config if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    # Merge with default config
                    self.config.update(file_config)

            except (json.JSONDecodeError, PermissionError, IOError) as e:
                # ✅ FIXED: Silently fall back to defaults instead of raising
                pass
            except Exception:
                # ✅ FIXED: Catch all other exceptions
                pass

        # Load ignore patterns with fallback logic:
        # 1. If .linkguardignore exists → use only that (explicit override)
        # 2. Otherwise → recursively collect all .gitignore files
        all_patterns: Set[str] = set()

        if self.ignore_file.exists():
            # .linkguardignore takes priority (explicit configuration)
            try:
                all_patterns = self._parse_ignore_file(self.ignore_file)
            except Exception:
                # ✅ FIXED: Silently fall back if ignore file is unreadable
                all_patterns = set()
        else:
            # Fallback: Collect all .gitignore patterns recursively
            all_patterns = self._collect_gitignore_patterns()

        # Merge with existing patterns
        existing = set(self.config.get("ignore_patterns", []))
        self.config["ignore_patterns"] = list(existing.union(all_patterns))

    def _collect_gitignore_patterns(self) -> Set[str]:
        """Recursively collect patterns from all .gitignore files in the project."""
        patterns: Set[str] = set()

        for gitignore_path in self.project_root.rglob(".gitignore"):
            try:
                patterns.update(self._parse_ignore_file(gitignore_path))
            except Exception:
                # ✅ FIXED: Skip unreadable .gitignore files
                continue

        return patterns

    def _parse_ignore_file(self, ignore_path: Path) -> Set[str]:
        """Parse a .gitignore or .linkguardignore file."""
        patterns: Set[str] = set()

        try:
            with open(ignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Handle negation patterns (for future enhancements)
                    if line.startswith("!"):
                        # Remove negation for now, can be handled later
                        line = line[1:].strip()

                    # Remove trailing slashes for directory patterns
                    if line.endswith("/"):
                        line = line[:-1]

                    patterns.add(line)

        except Exception as e:
            # ✅ FIXED: Re-raise to be caught by caller
            raise ValueError(f"Error reading ignore file {ignore_path}: {e}")

        return patterns

    def merge_cli_config(self, cli_config: Dict[str, Any]) -> None:
        """Merge command line configuration with existing config."""
        for key, value in cli_config.items():
            if key == "ignore_patterns" and value:
                # Merge ignore patterns from CLI with existing ones
                existing = set(self.config.get("ignore_patterns", []))
                self.config["ignore_patterns"] = list(existing.union(set(value)))
            else:
                # Override other values
                self.config[key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)

    def should_ignore_path(self, file_path: Path) -> bool:
        """Check if a given path matches any ignore patterns."""
        ignore_patterns = self.config.get("ignore_patterns", [])

        # Convert path to string for pattern matching
        path_str = str(file_path)
        path_parts = file_path.parts

        for pattern in ignore_patterns:
            # Handle directory patterns (with or without trailing slash)
            dir_pattern = pattern.rstrip("/")

            # Check if any part of the path matches the pattern
            for part in path_parts:
                if fnmatch.fnmatch(part, dir_pattern):
                    return True

            # Also check the full path
            if fnmatch.fnmatch(path_str, pattern):
                return True

            # Check relative path patterns
            if fnmatch.fnmatch(file_path.name, dir_pattern):
                return True

        return False

    def should_exclude_url(self, url: str) -> bool:
        """Check if a URL matches any exclusion patterns."""
        exclude_patterns = self.config.get("exclude_urls", [])

        for pattern in exclude_patterns:
            if fnmatch.fnmatch(url, pattern):
                return True

        return False

    def get_ignore_patterns(self) -> List[str]:
        """Get the list of ignore patterns."""
        return self.config.get("ignore_patterns", [])

    def get_exclude_urls(self) -> List[str]:
        """Get the list of excluded URL patterns."""
        return self.config.get("exclude_urls", [])

    def __repr__(self) -> str:
        return f"Config({self.config})"


def load_config(project_root: Path, cli_overrides: Optional[Dict[str, Any]] = None) -> Config:
    """Load configuration from project root with optional CLI overrides.

    Args:
        project_root: Project root directory
        cli_overrides: CLI arguments to override config

    Returns:
        Configured Config object
    """
    config = Config(project_root)

    if cli_overrides:
        config.merge_cli_config(cli_overrides)

    return config
