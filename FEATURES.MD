# 🛡️ LinkGuard Features Task List

## ✅ Status Legend
- ⬜ Not Started
- 🔄 In Progress
- ✅ Completed
- 🚫 Blocked
- 💡 Future Enhancement

---

## 🏗️ Phase 1: Core Infrastructure

### Project Setup
- ✅ Configure `pyproject.toml` with project metadata
- ✅ Set up virtual environment and dependency management
- ✅ Create `.gitignore` for Python projects
- ⬜ Initialize pytest configuration
- ⬜ Set up pre-commit hooks

### Utilities & Configuration
- ⬜ Implement `utils/logger.py` with structured logging (DEBUG/INFO/ERROR levels) - **File created but empty**
- ✅ Implement `utils/config.py` for loading `.linkguardignore`
- ✅ Add support for `linkguard.config.json` parsing
- ✅ Implement configuration precedence (CLI → config file → defaults)
- ✅ Add `.linkguardignore` pattern matching (gitignore-style) - **Config parsing complete, need file integration test**

---

## 🔍 Phase 2: File Scanning & URL Extraction

### File Discovery
- ✅ Implement recursive directory traversal in `scanner/file_scanner.py`
- ✅ Add file type detection (.md, .html, .json, .txt, .js, .jsx, .tsx)
- ⬜ Implement `.linkguardignore` filtering
- ✅ Add exclusion patterns for `node_modules`, `.git`, etc.
- ✅ Track file metadata (path, type, size)

### URL Extraction
- ✅ Extract URLs from Markdown files (`[text](url)` and bare URLs)
- ✅ Extract URLs from HTML files using BeautifulSoup (`href`, `src`)
- ✅ Extract URLs from JSON files (string values)
- ✅ Support plain text URL detection with regex
- ⬜ Handle relative vs absolute URL resolution
- ✅ Extract line numbers and context for each URL
- ✅ Deduplicate URLs from same file/line
- ✅ Clean trailing punctuation from URLs

---

## 🌐 Phase 3: Link Validation

### Async HTTP Checking
- ✅ Implement async HTTP client with `aiohttp` in `scanner/link_checker.py`
- ✅ Add concurrent request handling (default: 50 concurrent)
- ✅ Implement timeout handling (default: 10s per request)
- ✅ Handle redirects (follow up to 5 redirects)
- ✅ Categorize responses by status code (2xx, 3xx, 4xx, 5xx)
- ✅ Handle network errors gracefully (DNS, connection timeout)
- ⬜ Add retry logic for transient failures
- ⬜ Support custom headers (User-Agent, etc.)

### Environment Rules
- ✅ Implement environment detection in `scanner/rules.py`
- ✅ Detect localhost URLs (`localhost`, `127.0.0.1`, `0.0.0.0`)
- ✅ Detect development domains (`*.dev`, `*.local`, `*.test`)
- ✅ Implement `--mode prod` flag validation
- ✅ Return non-zero exit code when dev URLs found in prod mode
- ✅ Create rule violation reports

---

## 📊 Phase 4: Reporting & Output

### Console Output
- ✅ Implement Rich console formatter in `cli.py` (integrated, `formatter.py` empty)
- ✅ Add progress bar for scanning files
- ✅ Add progress bar for checking links with real-time updates
- ✅ Display real-time link validation results
- ✅ Show summary statistics (total, valid, broken, warnings)
- ✅ Color-code output (green=valid, red=broken, yellow=warning)
- ✅ Display broken links with file path and line number

### Export Formats
- ✅ Implement JSON export in `reporter/exporter.py`
- ✅ Implement CSV export
- ✅ Implement Markdown export
- ✅ Add structured export schema (file, url, status, line, message)
- ✅ Support custom export file paths (`--export report.json`)
- ✅ Generate timestamped reports with metadata

---

## ⚙️ Phase 5: CLI Interface

### Typer Commands
- ✅ Implement main `linkguard` CLI in `cli.py`
- ✅ Add `scan <directory>` command
- ✅ Add `--mode` option (dev/prod)
- ✅ Add `--export` option for output file
- ✅ Add `--ignore` option for runtime exclusions (comma-separated)
- ✅ Add `--timeout` option for request timeout
- ✅ Add `--concurrency` option for parallel requests
- ✅ Add `--verbose` flag for detailed logging
- ⬜ Add `--version` command
- ✅ Add `--help` documentation for all commands

### Exit Codes
- ✅ Return 0 on success (no broken links)
- ✅ Return 1 on broken links found
- ✅ Return 2 on configuration errors
- ⬜ Return 3 on dev URLs in production mode (currently exits with code 1)

---

## 🧪 Phase 6: Testing

### Unit Tests
- ⬜ Test file scanner with mock file system in `tests/test_scanner.py` - **File exists but empty**
- ⬜ Test URL extraction for each file type
- ⬜ Test `.linkguardignore` pattern matching
- ⬜ Test async link checker with mocked HTTP responses in `tests/test_checker.py` - **File exists but empty**
- ⬜ Test environment rule detection
- ⬜ Test configuration loading and precedence
- ⬜ Test reporter output formatting

### Integration Tests
- ✅ Create test fixtures with sample files (`data/sample.html` exists)
- ⬜ Test end-to-end scan workflow
- ⬜ Test CLI commands with various options
- ⬜ Test export functionality
- ⬜ Achieve 85%+ test coverage

### Test Infrastructure
- ✅ Set up pytest with async support (`pytest-asyncio`) - **Configured in pyproject.toml**
- ⬜ Configure pytest fixtures
- ✅ Add coverage reporting - **Configured in pyproject.toml**
- ⬜ Create GitHub Actions CI workflow

---

## 📦 Phase 7: Packaging & Distribution

### Package Setup
- ⬜ Complete `pyproject.toml` with build configuration
- ⬜ Add package metadata (version, author, license)
- ⬜ Configure entry points for CLI command
- ⬜ Add long description from README
- ⬜ Test local installation with `pip install -e .`

### Documentation
- ⬜ Write comprehensive README.md
- ⬜ Add usage examples with screenshots
- ⬜ Document configuration options
- ⬜ Create `.linkguardignore` example file
- ⬜ Create `linkguard.config.json` example file
- ⬜ Add CONTRIBUTING.md
- ⬜ Add LICENSE file

### Distribution
- ⬜ Build package with `python -m build`
- ⬜ Test installation from built package
- ⬜ Publish to TestPyPI
- ⬜ Publish to PyPI

---

## 🚀 Phase 8: Advanced Features (Future v2.0)

- 💡 **Browser Mode**: Playwright integration for sites with bot protection
- 💡 **Trusted Domains**: Whitelist for known-strict sites (pexels.com, etc.)
- 💡 **Smart Retry**: Exponential backoff for rate-limited sites

---

## 📈 Success Metrics

| Metric                    | Target              | Status |
| ------------------------- | ------------------- | ------ |
| Average scan time         | < 5s for 1000 links | 🔄     |
| Detection accuracy        | > 95%               | ✅     |
| Test coverage             | 85%+                | ⬜     |
| Package installation time | < 30s               | ⬜     |
| CLI startup time          | < 1s                | ✅     |

---

## 🔄 Version Milestones

- **v0.1.0**: Core scanning + basic validation (Phases 1-3) - ✅ **COMPLETED**
- **v0.2.0**: Rich reporting + CLI interface (Phases 4-5) - ✅ **COMPLETED** (Missing: logger.py, test files)
- **v0.3.0**: Testing + CI/CD (Phase 6) - 🔄 **NEXT UP** (Test infrastructure configured, need test implementation)
- **v1.0.0**: Full package release (Phase 7) - ⬜ **NOT STARTED**
- **v2.0.0**: Advanced features (Phase 8) - 💡 **FUTURE**

---

## 🎯 Current Sprint Focus (Updated: October 2025)

### ✅ Recently Completed (v0.2.0)
- [x] Implement `utils/config.py` with full config precedence
- [x] Add configuration file support (`linkguard.config.json`)
- [x] Complete all CLI options (mode, export, timeout, concurrency, ignore, verbose)
- [x] Implement all export formats (JSON, CSV, Markdown)
- [x] Add Rich progress bars and colored output
- [x] Configure pytest infrastructure in pyproject.toml

### 🔄 Current Sprint: Testing Foundation (v0.3.0)
- [ ] Implement `utils/logger.py` with Rich logging
- [ ] Write unit tests for file scanner (`tests/test_scanner.py`)
- [ ] Write unit tests for URL extractor
- [ ] Write async tests for link checker (`tests/test_checker.py`)
- [ ] Write tests for configuration loading
- [ ] Test `.linkguardignore` pattern matching

### 📅 Next Sprint: Test Coverage & CI/CD
- [ ] Complete unit test coverage (target 85%+)
- [ ] Write integration tests
- [ ] Create GitHub Actions CI workflow
- [ ] Add pre-commit hooks template
- [ ] Performance benchmarks

### 🚀 Future: v1.0.0 Release
- [ ] Finalize documentation
- [ ] Create usage examples and tutorials
- [ ] Test package installation
- [ ] Publish to TestPyPI
- [ ] Publish v1.0.0 to PyPI