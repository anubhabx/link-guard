# Changelog

All notable changes to LinkGuard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### To Be Added in v0.3.0
- Unit tests for all scanner modules
- Integration tests with real fixtures
- Logger implementation in `utils/logger.py`
- GitHub Actions CI/CD workflow
- Pre-commit hooks template

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

**[0.2.0] vs [0.1.0]**
- Added complete configuration system (JSON + ignore file)
- Added 3 export formats (JSON, CSV, Markdown)
- Added Rich console output with progress bars
- Added 3 new CLI options (concurrency, ignore, verbose)
- Improved error handling and user feedback

**Lines of Code:**
- v0.1.0: ~450 lines
- v0.2.0: ~710 lines (+58% growth)

**Test Coverage:**
- v0.1.0: 0%
- v0.2.0: 0% (infrastructure ready, tests pending)

---

[Unreleased]: https://github.com/anubhabx/link-guard/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/anubhabx/link-guard/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/anubhabx/link-guard/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/anubhabx/link-guard/releases/tag/v0.0.1
