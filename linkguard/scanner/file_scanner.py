from pathlib import Path
from typing import List, Set, Optional
import fnmatch


class FileScanner:
    """Recursively discovers files to scan for links."""

    # File extensions we'll scan for URLs
    SUPPORTED_EXTENSIONS = {
        ".md",
        ".html",
        ".htm",
        ".json",
        ".txt",
        ".tsx",
        ".jsx",
        ".js",
    }

    DEFAULT_IGNORE_PATTERNS = {
        ".git",
        ".venv",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".idea",
        "dist",
        "build",
    }

    def __init__(self, root_dir: Path, ignore_patterns: Optional[Set[str]] = None):
        self.root_dir = Path(root_dir)
        self.ignore_patterns = ignore_patterns or set()
        # Merge with default patterns
        self.ignore_patterns.update(self.DEFAULT_IGNORE_PATTERNS)

    def scan(self) -> List[Path]:
        """
        Recursively scan the root directory for supported files.

        Returns:
            List[Path]: List of file paths to check for URLs
        """
        discovered_files = []

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file():
                # Check if file has supported extension
                if file_path.suffix in self.SUPPORTED_EXTENSIONS:
                    # Skip if matches ignore patterns
                    if not self._should_ignore(file_path):
                        # Skip hidden files (starting with .)
                        if not file_path.name.startswith("."):
                            discovered_files.append(file_path)

        return discovered_files

    def _should_ignore(self, file_path: Path) -> bool:
        """Check if file is in an ignored directory."""
        parts = file_path.parts

        for pattern in self.ignore_patterns:
            # Check if any part of the path matches the ignore pattern
            for part in parts:
                if fnmatch.fnmatch(part, pattern):
                    return True

        return False
