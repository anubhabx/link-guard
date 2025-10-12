# 🚀 LinkGuard Quick Reference

**For developers working on LinkGuard - Updated October 12, 2025**

---

## 📁 Project Structure

```
linkguard/
├── cli.py                     # ✅ Main CLI (180 lines) - Typer commands, Rich output
├── scanner/
│   ├── file_scanner.py        # ✅ File discovery (60 lines)
│   ├── url_extractor.py       # ✅ URL extraction (150 lines)
│   ├── link_checker.py        # ✅ Async HTTP validation (180 lines)
│   └── rules.py               # ✅ Environment rules (60 lines)
├── reporter/
│   ├── formatter.py           # ⬜ EMPTY - Rich code in cli.py
│   └── exporter.py            # ✅ JSON/CSV/MD export (150 lines)
└── utils/
    ├── config.py              # ✅ Config loader (120 lines)
    └── logger.py              # ⬜ EMPTY - Needs implementation

tests/
├── test_scanner.py            # ⬜ EMPTY - Needs tests
└── test_checker.py            # ⬜ EMPTY - Needs tests

Total: ~900 lines of production code
```

---

## 🔧 Development Setup (Windows PowerShell)

```powershell
# 1. Clone and navigate
git clone https://github.com/anubhabx/link-guard.git
cd link-guard

# 2. Create virtual environment
python -m venv venv

# 3. Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# 4. Install in editable mode with dev dependencies
pip install -e ".[dev]"

# 5. Verify installation
linkguard --help
```

---

## 🧪 Testing Commands

```powershell
# Run all tests (when written)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=linkguard --cov-report=html

# Run specific test file
pytest tests/test_scanner.py -v

# Run async tests
pytest tests/test_checker.py --asyncio-mode=auto

# View coverage report
start htmlcov/index.html
```

---

## 📊 Code Quality Commands

```powershell
# Format code with Black
black linkguard/ tests/

# Lint with flake8
flake8 linkguard/

# Type check with mypy
mypy linkguard/

# Run all quality checks
black linkguard/ && flake8 linkguard/ && mypy linkguard/
```

---

## 🏃 Running LinkGuard

```powershell
# Basic usage
linkguard scan

# Production mode
linkguard scan --mode prod

# Custom options
linkguard scan ./docs --timeout 20 --concurrency 100

# Export results
linkguard scan --export report.json

# Ignore patterns
linkguard scan --ignore "*.draft.md,temp/*"

# Verbose output
linkguard scan --verbose

# All options combined
linkguard scan ./docs `
  --mode prod `
  --timeout 15 `
  --concurrency 75 `
  --export results.json `
  --ignore "node_modules,*.pyc" `
  --verbose
```

---

## 📝 Configuration Files

### linkguard.config.json
```json
{
  "mode": "dev",
  "timeout": 10,
  "concurrency": 50,
  "ignore_patterns": [
    "node_modules",
    ".git",
    "*.pyc"
  ],
  "exclude_urls": [
    "http://example.com/*",
    "https://private-api.internal/*"
  ],
  "strict_ssl": false
}
```

### .linkguardignore
```
# Ignore directories
node_modules
.git
dist
build

# Ignore file patterns
*.draft.md
*.temp.html
temp-*

# Ignore paths
/archive/*
/vendor/*
```

---

## 🐛 Common Issues & Solutions

### Issue: `linkguard: command not found`
**Solution:**
```powershell
pip install -e ".[dev]"
# OR use full path
python -m linkguard.cli scan
```

### Issue: `ModuleNotFoundError: No module named 'linkguard'`
**Solution:**
```powershell
# Make sure you're in the project root
cd c:\dev\link-guard
pip install -e ".[dev]"
```

### Issue: Tests not running
**Solution:**
```powershell
# Install dev dependencies
pip install -e ".[dev]"

# Check pytest is installed
pytest --version
```

### Issue: Virtual environment not activating
**Solution:**
```powershell
# PowerShell execution policy issue
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\venv\Scripts\Activate.ps1
```

---

## 🎯 What to Work On Next

### High Priority (v0.3.0)
1. **Implement Logger** - `utils/logger.py`
   ```python
   # Template
   from rich.logging import RichHandler
   import logging

   def get_logger(name: str, verbose: bool = False):
       level = logging.DEBUG if verbose else logging.INFO
       # ... implement Rich logging
   ```

2. **Write Unit Tests** - `tests/test_scanner.py`
   ```python
   # Template
   import pytest
   from pathlib import Path
   
   @pytest.fixture
   def temp_markdown_file(tmp_path):
       md_file = tmp_path / "test.md"
       md_file.write_text("[Google](https://google.com)")
       return md_file
   
   def test_scan_markdown_file(temp_markdown_file):
       # ... test file scanning
   ```

3. **Create CI Workflow** - `.github/workflows/test.yml`
   ```yaml
   name: Tests
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - uses: actions/setup-python@v2
         - run: pip install -e ".[dev]"
         - run: pytest tests/ --cov=linkguard
   ```

### Medium Priority
4. **Add Screenshots** to README
5. **Create Example Configs** in `examples/`
6. **Fix Exit Code 3** for dev URLs in prod mode

### Low Priority
7. **Pre-commit Hooks** configuration
8. **Performance Benchmarks**
9. **Video Tutorial**

---

## 📚 Key Files to Understand

### 1. `cli.py` - Entry Point
- **What it does:** Parses CLI args, orchestrates scan, displays results
- **Key functions:** `scan()`, config loading, progress bar handling
- **Dependencies:** typer, rich, asyncio

### 2. `scanner/file_scanner.py` - File Discovery
- **What it does:** Recursively finds files to scan
- **Key functions:** `scan()`, `_should_ignore()`
- **Config:** Uses `SUPPORTED_EXTENSIONS` and `DEFAULT_IGNORE_PATTERNS`

### 3. `scanner/url_extractor.py` - URL Extraction
- **What it does:** Extracts URLs from different file types
- **Key functions:** `extract_from_file()`, `_extract_from_text()`, `_extract_from_html()`
- **Patterns:** `URL_PATTERN`, `MD_LINK_PATTERN`

### 4. `scanner/link_checker.py` - Link Validation
- **What it does:** Async HTTP checking with HEAD→GET fallback
- **Key functions:** `check_links()`, `_check_one_link()`, `_check_with_get()`
- **Features:** Semaphore concurrency, timeout handling, progress callbacks

### 5. `utils/config.py` - Configuration
- **What it does:** Loads and merges config from multiple sources
- **Key functions:** `load_config()`, `_parse_ignore_file()`
- **Precedence:** CLI > config file > defaults

---

## 🔍 Code Patterns Used

### Async Pattern (link_checker.py)
```python
async def check_links(self, url_data, progress_callback=None):
    semaphore = asyncio.Semaphore(self.max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        tasks = [self._check_one_link(session, semaphore, ...) 
                 for file_path, url_info in url_data]
        
        for coro in asyncio.as_completed(tasks):
            result = await coro
            if progress_callback:
                progress_callback(completed)
```

### Config Precedence (config.py)
```python
config = Config(project_root)  # Load from file
config.merge_cli_config(cli_overrides)  # Override with CLI
final_timeout = config.get("timeout", 10)  # Get with default
```

### Rich Progress (cli.py)
```python
with Progress(...) as progress:
    task = progress.add_task("Checking links...", total=len(urls))
    
    def update_progress(completed):
        progress.update(task, completed=completed)
    
    results = asyncio.run(checker.check_links(urls, update_progress))
```

---

## 📊 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Scan 1000 links | < 5s | ~3s ✅ |
| Startup time | < 1s | ~0.5s ✅ |
| Memory usage | < 100MB | ~40MB ✅ |
| Test coverage | 85%+ | 0% ❌ |

---

## 🔗 Useful Links

- **GitHub Repo:** https://github.com/anubhabx/link-guard
- **Documentation:** See `README.MD`, `FEATURES.MD`, `PLAN.MD`
- **Status Report:** See `STATUS.MD`
- **Changelog:** See `CHANGELOG.MD`

---

**Last Updated:** October 12, 2025  
**Current Version:** v0.2.0  
**Next Milestone:** v0.3.0 (Testing & Quality)
