# Changelog

All notable changes to LinkGuard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### To Be Added in v0.4.0
- Performance benchmarks and optimization
- Pre-commit hooks template  
- Advanced retry logic with exponential backoff
- Custom headers support for authenticated requests

---

## [0.3.0] - 2025-10-15

### Added
- **Comprehensive Test Suite (91 tests, 71% coverage)**
  - Scanner tests (13 tests): File discovery, ignore patterns, hidden files
  - URL Extractor tests (16 tests): Markdown, HTML, JSON, JS/TS extraction
  - Link Checker tests (10 tests): Async HTTP validation with mocking
  - Configuration tests (23 tests): Config loading, precedence, ignore files
  - Logger tests (5 tests): Rich logging implementation
  - Environment Rules tests (8 tests): Localhost, private IPs, dev domains
  - Exporter tests (9 tests): JSON, CSV, Markdown export validation
  - **CLI Integration tests (10 tests)**: End-to-end CLI command testing

- **GitHub Actions CI/CD Workflow**
  - Multi-OS testing (Ubuntu, Windows, macOS)
  - Multi-Python version testing (3.10, 3.11, 3.12, 3.13)
  - Automated linting (Black, flake8, mypy)
  - Coverage reporting with Codecov integration
  - Package build verification
  - Code quality checks with coverage threshold (70%)

- **Logger Implementation (`utils/logger.py`)**
  - Rich logging with color-coded output
  - Debug/Info/Error levels with proper formatting
  - Verbose mode support via `--verbose` flag
  - Module-specific logger instances

- **Test Infrastructure**
  - pytest configuration with async support
  - pytest-asyncio for async test execution
  - pytest-cov for coverage reporting (HTML, XML, terminal)
  - Comprehensive fixtures and mock utilities
  - AsyncMock for HTTP response mocking

### Changed
- **Fixed CLI Typer compatibility issue**
  - Changed `directory` argument from Path with default to Optional[str]
  - Resolved `TyperArgument.make_metavar()` TypeError
  - CLI now works with Typer 0.19.2+
- Improved async result ordering in link checker tests
- Enhanced path matching for directory detection in file scanner
- Updated hidden file filtering logic

### Fixed
- Missing `assert` statement in link_checker dataclass test
- Async ordering issue in multi-URL test cases
- Path pattern matching for nested directories
- Hidden file filtering (files starting with `.`)
- CLI module import issues (installed package in editable mode)

### Test Coverage by Module
- `file_scanner.py`: 100% (26 statements)
- `url_extractor.py`: 100% (74 statements)
- `rules.py`: 100% (29 statements)
- `exporter.py`: 100% (48 statements)
- `logger.py`: 100% (13 statements)
- `config.py`: 92% (92 statements, 7 missed)
- `link_checker.py`: 82% (67 statements, 12 missed)
- `cli.py`: 0% (115 statements - tested via integration tests)
- **Overall**: 71% coverage (464 statements, 134 missed)

---

## [0.2.0] - 2025-10-12

### Added
- **Configuration System**
  - Support for `linkguard.config.json` configuration file
  - Support for `.linkguardignore` file (gitignore-style patterns)
  - Configuration precedence: CLI args > config file > defaults
  - Config validation with helpful error messages

- **CLI Enhancements**
  - `--concurrency` / `-c` option for controlling parallel requests (default: 50)
  - `--ignore` / `-i` option for runtime exclusion patterns (comma-separated)
  - `--verbose` / `-v` flag for detailed output
  - Exit code 2 for configuration errors
  - Improved help text for all commands

- **Export Formats**
  - JSON export with metadata (timestamp, totals, configuration)
  - CSV export with headers and violation mapping
  - Markdown export with formatted tables and summaries
  - Auto-detection of format based on file extension

- **Rich Console Output**
  - Real-time progress bars with task completion tracking
  - Color-coded results (green for valid, red for broken, yellow for warnings)
  - Summary table with scan statistics
  - Detailed broken link reports with file paths and line numbers
  - Rule violation warnings with context

### Changed
- Moved Rich formatting from `reporter/formatter.py` to `cli.py` (formatter.py now empty)
- Improved error handling and user-friendly error messages
- Enhanced URL extraction to better handle edge cases
- Updated documentation to reflect current implementation status

### Fixed
- URL deduplication to avoid reporting same URL multiple times from same file/line
- Trailing punctuation removal from extracted URLs
- Better handling of HEAD request failures (fallback to GET)

---

## [0.1.0] - 2025-10-09

### Added
- **Core Scanning Pipeline**
  - Recursive file scanner with pattern matching
  - Default exclusions: `.git`, `.venv`, `node_modules`, `__pycache__`, etc.
  - Support for 8 file types: `.md`, `.html`, `.htm`, `.json`, `.txt`, `.js`, `.jsx`, `.ts`, `.tsx`

- **URL Extraction**
  - Markdown link extraction: `[text](url)` patterns
  - Bare URL detection in all text files
  - HTML attribute extraction: `href`, `src` from `<a>`, `<img>`, `<link>`, `<script>` tags
  - JSON recursive search for URL strings
  - Line number and context tracking for each URL

- **Async Link Validation**
  - Asynchronous HTTP checking with `aiohttp`
  - Semaphore-based concurrency control (default: 50 concurrent requests)
  - Configurable timeout (default: 10 seconds)
  - Browser-like User-Agent headers to avoid bot detection
  - Smart HEAD → GET fallback for servers that block HEAD requests
  - Response time tracking
  - Comprehensive error handling (timeout, DNS, connection errors)

- **Environment Rules**
  - Localhost detection: `localhost`, `127.0.0.1`, `0.0.0.0`, `::1`
  - Private network detection: `192.168.*.*`, `10.*.*.*`
  - Development domain detection: `.local`, `.test`
  - Production mode validation with rule violations
  - Violation reporting with severity levels

- **CLI Interface**
  - Main `scan` command with Typer framework
  - `--mode` / `-m` option: dev or prod (default: dev)
  - `--timeout` / `-t` option: request timeout in seconds (default: 10)
  - `--export` / `-e` option: export results to file
  - `--help` comprehensive documentation
  - Exit code 0 for success, 1 for broken links

- **Project Infrastructure**
  - Complete `pyproject.toml` with metadata and dependencies
  - pytest configuration with async support
  - Coverage reporting setup (HTML, XML, terminal)
  - Black, flake8, mypy configurations
  - Development dependencies (`pytest`, `pytest-asyncio`, `pytest-cov`, etc.)

### Known Issues
- `utils/logger.py` is empty (verbose mode doesn't produce detailed logs)
- `reporter/formatter.py` is empty (Rich code integrated in cli.py)
- No unit tests written yet (test files exist but are empty)
- Exit code 3 for dev URLs in prod mode not implemented (uses exit code 1)
- Some websites (Pexels, Medium) return 403 due to bot detection (expected behavior)

---

## [0.0.1] - 2025-10-01

### Added
- Initial project structure
- Basic Python package setup
- Git repository initialization

---

## Version Comparison

**[0.3.0] vs [0.2.0]**
- Added 70 comprehensive tests (7 test modules)
- Added Logger implementation with Rich integration
- Achieved 71% test coverage (100% on 5 core modules)
- Added test infrastructure (pytest-asyncio, fixtures, mocking)
- Fixed hidden file filtering and path matching bugs

**[0.2.0] vs [0.1.0]**
- Added complete configuration system (JSON + ignore file)
- Added 3 export formats (JSON, CSV, Markdown)
- Added Rich console output with progress bars
- Added 3 new CLI options (concurrency, ignore, verbose)
- Improved error handling and user feedback

**Lines of Code:**
- v0.1.0: ~450 lines
- v0.2.0: ~710 lines (+58% growth)
- v0.3.0: ~1,300 lines (+83% growth from v0.2.0)

**Test Coverage:**
- v0.1.0: 0%
- v0.2.0: 0% (infrastructure ready, tests pending)
- v0.3.0: 71% (70 tests, 100% pass rate)

---

[Unreleased]: https://github.com/anubhabx/link-guard/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/anubhabx/link-guard/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/anubhabx/link-guard/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/anubhabx/link-guard/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/anubhabx/link-guard/releases/tag/v0.0.1
