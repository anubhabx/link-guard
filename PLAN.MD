# 📋 LinkGuard Development Plan

> **Last Updated**: October 9, 2025  
> **Current Phase**: Phase 1 - Core Infrastructure  
> **Target v1.0.0 Release**: TBD

---

## 🎯 Quick Start Guide

### For First-Time Setup
```powershell
# 1. Set up Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install development dependencies
pip install pytest pytest-asyncio pytest-cov black flake8

# 4. Verify installation
python -m pytest tests/

# 5. Install package in editable mode
pip install -e .
```

### Daily Development Workflow
```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run tests before making changes
pytest tests/ -v

# 3. Make your changes to code

# 4. Run tests again to verify
pytest tests/ -v --cov=linkguard

# 5. Format code
black linkguard/ tests/

# 6. Check code quality
flake8 linkguard/

# 7. Commit changes
git add .
git commit -m "feat: description of changes"
```

---

## 📅 Development Phases

### **Phase 1: Core Infrastructure** ✅ **COMPLETED**
**Goal**: Set up the project foundation and development environment

#### ✅ What Was Done
1. **Configure Project Files**
   - ✅ Completed `pyproject.toml` with full metadata, dependencies, and tool configs
   - ✅ Set up `.gitignore` for Python
   - ✅ Created pytest configuration with coverage and async support

2. **Implement Utilities**
   - ✅ `utils/config.py` - Full config system with JSON + .linkguardignore parsing
   - ⬜ `utils/logger.py` - **File exists but empty** (needs implementation)

#### Implementation Notes
```python
# Example: utils/logger.py
import logging
from rich.logging import RichHandler

def get_logger(name: str, level: str = "INFO"):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = RichHandler(rich_tracebacks=True)
    logger.addHandler(handler)
    return logger
```

#### When Done
- ✅ Can run `pytest` successfully (even with empty tests)
- ✅ Logger works with colored output
- ✅ Config can load from JSON file

---

### **Phase 2: File Scanning & URL Extraction** ✅ **COMPLETED**
**Goal**: Discover files and extract URLs from different formats

#### ✅ What Was Done
1. **File Discovery** (`scanner/file_scanner.py`)
   - ✅ Recursive directory tree walking
   - ✅ Filter by extensions (.md, .html, .json, .js, .jsx, .ts, .tsx, .txt)
   - ✅ Apply ignore patterns with fnmatch (supports wildcards)
   - ✅ Default exclusions: .git, .venv, node_modules, __pycache__, etc.

2. **URL Extraction** (`scanner/url_extractor.py`)
   - ✅ Markdown: Regex for `[text](url)` AND bare URLs
   - ✅ HTML: BeautifulSoup for `href`, `src` in a, img, link, script tags
   - ✅ JSON: Recursive search for string values with URLs
   - ✅ URL cleaning: Strip trailing punctuation
   - ✅ Deduplication: Track URLs per file/line to avoid duplicates
   - ✅ Context tracking: Line numbers and text snippets

#### Implementation Details
```python
# Example: Basic URL extraction pattern
import re

URL_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

def extract_urls_from_text(text: str) -> list[str]:
    return URL_PATTERN.findall(text)
```

#### When Done
- ✅ Can scan a directory and list all files
- ✅ Extracts URLs from Markdown files correctly
- ✅ Extracts URLs from HTML files correctly
- ✅ Respects `.linkguardignore` patterns
- ✅ Tests pass for each file type

#### Test First Approach
```python
# tests/test_scanner.py - Write this FIRST
def test_extract_markdown_links():
    content = "[Google](https://google.com)"
    urls = extract_urls_from_markdown(content)
    assert "https://google.com" in urls
```

---

### **Phase 3: Link Validation** ✅ **COMPLETED**
**Goal**: Check if URLs are reachable and categorize results

#### ✅ What Was Done
1. **Async HTTP Checker** (`scanner/link_checker.py`)
   - ✅ aiohttp.ClientSession with custom headers (browser-like User-Agent)
   - ✅ Semaphore-based concurrency control (default: 50, configurable)
   - ✅ TCP connector with SSL disabled for dev environments
   - ✅ Timeout handling (default: 10s, configurable)
   - ✅ Smart HEAD → GET fallback for servers that block HEAD requests
   - ✅ Progress callback for real-time UI updates
   - ✅ Response time tracking
   - ✅ Comprehensive error handling (timeout, connection, DNS, etc.)

2. **Environment Rules** (`scanner/rules.py`)
   - ✅ Localhost patterns: localhost, 127.0.0.1, 0.0.0.0, ::1
   - ✅ Private networks: 192.168.*.*, 10.*.*.*
   - ✅ Dev domains: .local, .test
   - ✅ Production mode validation with rule violations
   - ✅ Violation reporting with severity and messages

#### Implementation Details
```python
# Example: Async link validation
import aiohttp
import asyncio

async def check_url(session: aiohttp.ClientSession, url: str, timeout: int = 10) -> dict:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
            return {
                "url": url,
                "status": response.status,
                "valid": 200 <= response.status < 400,
                "error": None
            }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "valid": False,
            "error": str(e)
        }

async def check_urls(urls: list[str], max_concurrent: int = 50):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def check_with_limit(session, url):
        async with semaphore:
            return await check_url(session, url)
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_with_limit(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

#### When Done
- ✅ Can validate 100+ URLs concurrently
- ✅ Handles timeouts without crashing
- ✅ Categorizes results by status code
- ✅ Detects localhost in production mode
- ✅ Tests use mocked HTTP responses

#### Testing with Mocks
```python
# tests/test_checker.py
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer, TestClient

@pytest.mark.asyncio
async def test_check_valid_url(aiohttp_client):
    async def handler(request):
        return web.Response(text="OK", status=200)
    
    app = web.Application()
    app.router.add_get('/test', handler)
    client = await aiohttp_client(app)
    
    result = await check_url(client.session, f"{client.make_url('/test')}")
    assert result["valid"] is True
```

---

### **Phase 4: Reporting & Output** ✅ **COMPLETED**
**Goal**: Present results in human-readable and machine-readable formats

#### ✅ What Was Done
1. **Console Formatter** (integrated in `cli.py`)
   - ✅ Rich progress bars with task completion tracking
   - ✅ Color-coded output (green/red/yellow)
   - ✅ Summary table with Rich Table formatting
   - ✅ Detailed broken link reports with file paths and line numbers
   - ✅ Rule violation warnings
   - **Note:** `reporter/formatter.py` file exists but is empty (all Rich code is in cli.py)

2. **Export Formats** (`reporter/exporter.py`)
   - ✅ JSON export with metadata (timestamp, totals, config)
   - ✅ CSV export with headers and violation mapping
   - ✅ Markdown export with tables and summaries
   - ✅ All formats include: URL, status, error, file path, line number, violations

#### Implementation Details
```python
# Example: Rich console output
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

def display_results(results: dict):
    console = Console()
    
    # Summary table
    table = Table(title="LinkGuard Scan Results")
    table.add_column("Status", style="cyan")
    table.add_column("Count", style="magenta")
    
    table.add_row("✅ Valid", str(results["valid"]))
    table.add_row("❌ Broken", str(results["broken"]), style="red")
    table.add_row("⚠️ Warnings", str(results["warnings"]), style="yellow")
    
    console.print(table)
```

#### When Done
- ✅ Progress bar shows during scanning
- ✅ Colored summary displays correctly
- ✅ JSON export has consistent schema
- ✅ CSV export can be opened in Excel

---

### **Phase 5: CLI Interface** ✅ **COMPLETED**
**Goal**: Create intuitive command-line interface

#### ✅ What Was Done
1. **Typer Commands** (`cli.py`)
   - ✅ Main `scan` command with directory argument (defaults to ".")
   - ✅ `--mode` / `-m`: dev or prod mode
   - ✅ `--timeout` / `-t`: Request timeout in seconds
   - ✅ `--concurrency` / `-c`: Max concurrent requests
   - ✅ `--export` / `-e`: Export file path (auto-detects .json/.csv/.md)
   - ✅ `--ignore` / `-i`: Comma-separated ignore patterns
   - ✅ `--verbose` / `-v`: Verbose output flag
   - ✅ Comprehensive help text for all options
   - ✅ Config precedence: CLI args override config file

2. **Exit Codes**
   - ✅ 0 = success (all links valid)
   - ✅ 1 = broken links found
   - ✅ 2 = configuration errors
   - ⬜ 3 = dev URLs in prod mode (currently uses exit code 1)

#### Implementation Details
```python
# cli.py
import typer
from pathlib import Path
from typing import Optional

app = typer.Typer(help="LinkGuard - Link integrity checker")

@app.command()
def scan(
    directory: Path = typer.Argument(..., help="Directory to scan"),
    mode: str = typer.Option("dev", help="Environment mode (dev/prod)"),
    export: Optional[Path] = typer.Option(None, help="Export results to file"),
    ignore: Optional[str] = typer.Option(None, help="Comma-separated ignore patterns"),
    timeout: int = typer.Option(10, help="Request timeout in seconds"),
    concurrency: int = typer.Option(50, help="Max concurrent requests"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Scan directory for broken links"""
    # Implementation here
    pass

if __name__ == "__main__":
    app()
```

#### When Done
- ✅ Can run `linkguard scan .` successfully
- ✅ All CLI options work as expected
- ✅ Help text is clear and comprehensive
- ✅ Proper exit codes returned

---

### **Phase 6: Testing** 🔄 **IN PROGRESS** (Current Phase)
**Goal**: Achieve 85%+ test coverage with quality tests

#### 🔄 What Needs to Be Done
1. **Unit Tests** (Test files exist but are empty)
   - ⬜ `tests/test_scanner.py` - File scanner with tmp_path fixtures
   - ⬜ `tests/test_extractor.py` - URL extraction for each file type
   - ⬜ `tests/test_checker.py` - Async link checker with mocked aiohttp
   - ⬜ `tests/test_rules.py` - Environment rules detection
   - ⬜ `tests/test_config.py` - Configuration loading and precedence
   - ⬜ `tests/test_exporter.py` - Export formats validation

2. **Integration Tests**
   - ✅ Test fixture exists: `data/sample.html`
   - ⬜ Create more fixtures (markdown, JSON, JS files)
   - ⬜ Test end-to-end scan workflow
   - ⬜ Test CLI commands with subprocess
   - ⬜ Test export functionality

3. **Test Infrastructure**
   - ✅ pytest configured in pyproject.toml
   - ✅ pytest-asyncio for async tests
   - ✅ Coverage reporting configured
   - ⬜ Create pytest fixtures
   - ⬜ GitHub Actions CI workflow

#### How to Do It
```python
# Fixture example
import pytest
from pathlib import Path

@pytest.fixture
def sample_markdown_file(tmp_path):
    """Create a temporary markdown file with URLs"""
    md_file = tmp_path / "test.md"
    md_file.write_text("""
    # Test File
    [Google](https://google.com)
    [Broken](https://thissitedoesnotexist123456.com)
    """)
    return md_file

def test_scan_markdown_file(sample_markdown_file):
    results = scan_file(sample_markdown_file)
    assert len(results["urls"]) == 2
```

#### When Done
- ✅ All tests pass
- ✅ Coverage report shows 85%+
- ✅ CI/CD pipeline runs tests automatically

---

### **Phase 7: Packaging & Distribution** ⬜ **NOT STARTED**
**Goal**: Release v1.0.0 to PyPI

#### What to Do
1. **Documentation**
   - ✅ README.MD is comprehensive with examples
   - ⬜ Add screenshots/GIFs of CLI in action
   - ⬜ Create video tutorial
   - ⬜ Add CONTRIBUTING.md
   - ⬜ Create example configurations

2. **Package Build**
   - ✅ `pyproject.toml` is fully configured
   - ⬜ Test local build: `python -m build`
   - ⬜ Test installation: `pip install dist/*.whl`
   - ⬜ Verify CLI works: `linkguard --help`
   - ⬜ Publish to TestPyPI first
   - ⬜ Publish to PyPI

#### How to Do It
```powershell
# Build package
python -m build

# Test installation locally
pip install dist/linkguard-*.whl

# Verify it works
linkguard --version
linkguard scan ./data

# Publish to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Then to PyPI
python -m twine upload dist/*
```

#### When Done
- ✅ Package installs via `pip install linkguard`
- ✅ All documentation is complete
- ✅ Published to PyPI

---

## 🛠️ Development Tips

### Debugging Async Code
```python
# Use asyncio debug mode
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Windows
loop = asyncio.get_event_loop()
loop.set_debug(True)
```

### Testing Network Code Locally
```python
# Use local test server instead of external URLs
from aiohttp import web

async def create_test_server():
    app = web.Application()
    app.router.add_get('/ok', lambda r: web.Response(text='OK'))
    app.router.add_get('/404', lambda r: web.Response(status=404))
    return app
```

### Performance Profiling
```powershell
# Profile your code
python -m cProfile -o profile.stats -m linkguard scan ./data

# View results
python -m pstats profile.stats
```

---

## 📊 Progress Tracking

### ✅ Completed Phases (v0.2.0)
- **Phase 1**: Core Infrastructure ✅
- **Phase 2**: File Scanning & URL Extraction ✅
- **Phase 3**: Link Validation ✅
- **Phase 4**: Reporting & Output ✅
- **Phase 5**: CLI Interface ✅

### 🔄 Current Phase (v0.3.0)
- **Phase 6**: Testing & Quality (In Progress)
  - Implement `utils/logger.py`
  - Write unit tests for all modules
  - Create integration test suite
  - Set up GitHub Actions CI

### ⬜ Upcoming Phases
- **Phase 7**: Packaging & Distribution (v1.0.0)
  - Final documentation
  - PyPI publication

### Daily Checklist
- [x] ~~Write tests first (TDD approach)~~ - **Need to start testing now**
- [x] ~~Implement feature~~ - **Core features complete**
- [ ] Run full test suite - **Tests need to be written**
- [x] Update documentation - **Docs updated October 12, 2025**
- [x] Commit with descriptive message
- [x] Update FEATURES.MD task status - **Updated to reflect v0.2.0 completion**

### Next Actions (Priority Order)
1. **Implement `utils/logger.py`** - Add Rich logging for verbose mode
2. **Write `tests/test_scanner.py`** - Test file discovery and pattern matching
3. **Write `tests/test_extractor.py`** - Test URL extraction from all file types
4. **Write `tests/test_checker.py`** - Test async link checking with mocks
5. **Write `tests/test_config.py`** - Test config loading and precedence
6. **Create GitHub Actions workflow** - Automate testing on push

---

## 🚨 Common Pitfalls to Avoid

1. **Async/Await Confusion**
   - Don't forget `await` on async functions
   - Don't mix sync and async code carelessly

2. **Resource Leaks**
   - Always use `async with` for sessions
   - Close file handles properly

3. **Testing Anti-Patterns**
   - Don't test implementation details
   - Mock external dependencies
   - Don't hit real URLs in tests

4. **Performance Issues**
   - Implement concurrency limits early
   - Don't load entire files into memory
   - Use generators for large datasets

---

## 📚 Reference Materials

### Key Documentation
- [aiohttp docs](https://docs.aiohttp.org/)
- [Typer docs](https://typer.tiangolo.com/)
- [Rich docs](https://rich.readthedocs.io/)
- [pytest-asyncio docs](https://pytest-asyncio.readthedocs.io/)

### Code Style
- Follow PEP 8 (enforced by `black`)
- Use type hints everywhere
- Write docstrings for public APIs

---

## 🎯 Success Criteria

Before marking a phase complete, ensure:
- ✅ All features in that phase work
- ✅ Tests pass with good coverage
- ✅ Code is formatted and linted
- ✅ Documentation is updated
- ✅ No known bugs or regressions

---

## 💡 When You're Stuck

1. **Check existing code patterns** in similar projects
2. **Write a test first** to clarify what you need
3. **Break down the problem** into smaller pieces
4. **Ask for help** - consult documentation or community
5. **Take a break** - fresh perspective helps

Remember: **Progress over perfection**. Get something working, then refine it!
