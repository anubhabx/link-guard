from pathlib import Path
from typing import List, Set, Optional

class FileScanner:
    """Recursively discovers files to scan for links."""
    
    # File extensions we'll scan for URLs
    SUPPORTED_EXTENSIONS = {'.md', '.html', '.htm', '.json', '.txt', '.tsx', '.jsx', '.js'}
    
    DEFAULT_IGNORE_PATTERNS = {
        '.git', '.venv', 'node_modules', '__pychache__',
        '.pytest_cache', '.idea', 'dist', 'build'
    }
    
    def __init__(self, root_dir: Path, ignore_patterns: Optional[Set[str]] = None):
        self.root_dir = root_dir
        self.ignore_patterns = ignore_patterns or self.DEFAULT_IGNORE_PATTERNS
        
    def scan(self) -> List[Path]:
        """
        Recursively scan directory for supported files.
        
        Returns: List of Path objects for files to scan
        """
        
        files_to_scan = []
        
        for file_path in self.root_dir.rglob('*'):
            # Skip Directories
            if file_path.is_dir():
                continue
            
            # Skip in ignored directory
            if self._should_ignore(file_path):
                continue
            
            # Only include supported file types
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                files_to_scan.append(file_path)
                
        return files_to_scan
    
    def _should_ignore(self, file_path: Path) -> bool:
        """Check if file is in an ignored directory."""
        for part in file_path.parts:
            if part in self.ignore_patterns:
                return True
        return False