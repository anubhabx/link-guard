# 🚀 LinkGuard Quick Reference

**For developers working on LinkGuard - Updated October 15, 2025**

**Current Version:** v1.0.1 (Production Release)

---

## 📁 Project Structure

```
linkguard/
├── __init__.py                # ✅ Package init with __version__
├── cli.py                     # ✅ Main CLI (224 lines) - Typer commands, Rich output
├── scanner/
│   ├── file_scanner.py        # ✅ File discovery with comprehensive docs
│   ├── url_extractor.py       # ✅ URL extraction with type hints
│   ├── link_checker.py        # ✅ Async HTTP validation with frozen dataclass
│   └── rules.py               # ✅ Environment rules with Final types
├── reporter/
│   ├── formatter.py           # ⬜ EMPTY (Rich code integrated in cli.py)
│   └── exporter.py            # ✅ JSON/CSV/MD export with detailed docs
└── utils/
    ├── config.py              # ✅ Config loader with comprehensive docs
    └── logger.py              # ✅ Rich logging implementation

tests/                         # ✅ 91 tests, 71% coverage
├── test_scanner.py            # ✅ 13 tests (file discovery)
├── test_extractor.py          # ✅ 16 tests (URL extraction)
├── test_checker.py            # ✅ 10 tests (async HTTP)
├── test_config.py             # ✅ 23 tests (configuration)
├── test_exporter.py           # ✅ 9 tests (export formats)
├── test_logger.py             # ✅ 5 tests (logging)
├── test_rules.py              # ✅ 8 tests (environment rules)
└── test_cli_integration.py    # ✅ 10 tests (end-to-end)

.github/workflows/
└── ci.yml                     # ✅ Multi-OS/Python CI/CD

Total: ~1,300 lines of production code + comprehensive tests
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

### ✅ Recently Completed (v1.0)
1. ✅ **Comprehensive Documentation** - All modules have detailed docstrings
2. ✅ **Type Hints** - Final, Pattern, List, Dict throughout codebase
3. ✅ **Example Configs** - .linkguardignore.example and linkguard.config.json.example
4. ✅ **CONTRIBUTING.md** - 300+ lines of contribution guidelines
5. ✅ **Package Distribution** - Built and published to TestPyPI
6. ✅ **RELEASE_NOTES.md** - Comprehensive v1.0 documentation

### High Priority (v1.1.0 Planning)
1. **Publish to PyPI** - v1.0 packages ready
   ```powershell
   # Ready to publish
   python -m twine upload dist/linkguard-1.0*
   ```

2. **Retry Logic** - Exponential backoff for transient failures
   ```python
   # Plan for link_checker.py
   async def _check_with_retry(self, session, url, max_retries=2):
       for attempt in range(max_retries):
           try:
               return await self._check_one_link(session, url)
           except TransientError:
               await asyncio.sleep(2 ** attempt)  # Exponential backoff
   ```

3. **Custom Headers** - Support authenticated requests
   ```bash
   linkguard scan --header "Authorization: Bearer token"
   ```

### Medium Priority
4. **Relative URL Resolution** - Support `../docs/api.md` style links
5. **Installation Video** - Create tutorial for new users
6. **Performance Benchmarks** - Document speed metrics

### Low Priority
7. **Pre-commit Hooks** template configuration
8. **Screenshots/GIFs** for README
9. **GitHub Discussions** setup

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

**Last Updated:** October 15, 2025  
**Current Version:** v1.0.1 (Production Release)  
**Next Milestone:** v1.1.0 (Enhanced Features - Retry Logic, Custom Headers, Relative URLs)
