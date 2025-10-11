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
- ⬜ Implement `utils/logger.py` with structured logging (DEBUG/INFO/ERROR levels)
- ⬜ Implement `utils/config.py` for loading `.linkguardignore`
- ⬜ Add support for `linkguard.config.json` parsing
- ⬜ Implement configuration precedence (CLI → config file → defaults)
- ⬜ Add `.linkguardignore` pattern matching (gitignore-style)

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
- ✅ Implement Rich console formatter in `reporter/formatter.py`
- ✅ Add progress bar for scanning files
- ✅ Add progress bar for checking links
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
- ✅ Generate timestamped reports

---

## ⚙️ Phase 5: CLI Interface

### Typer Commands
- ✅ Implement main `linkguard` CLI in `cli.py`
- ✅ Add `scan <directory>` command
- ✅ Add `--mode` option (dev/prod)
- ✅ Add `--export` option for output file
- ⬜ Add `--ignore` option for runtime exclusions
- ✅ Add `--timeout` option for request timeout
- ⬜ Add `--concurrency` option for parallel requests
- ⬜ Add `--verbose` flag for detailed logging
- ⬜ Add `--version` command
- ✅ Add `--help` documentation for all commands

### Exit Codes
- ✅ Return 0 on success (no broken links)
- ✅ Return 1 on broken links found
- ⬜ Return 2 on configuration errors
- ⬜ Return 3 on dev URLs in production mode

---

## 🧪 Phase 6: Testing

### Unit Tests
- ⬜ Test file scanner with mock file system in `tests/test_scanner.py`
- ⬜ Test URL extraction for each file type
- ⬜ Test `.linkguardignore` pattern matching
- ⬜ Test async link checker with mocked HTTP responses in `tests/test_checker.py`
- ⬜ Test environment rule detection
- ⬜ Test configuration loading and precedence
- ⬜ Test reporter output formatting

### Integration Tests
- ⬜ Create test fixtures with sample files (`data/` directory)
- ⬜ Test end-to-end scan workflow
- ⬜ Test CLI commands with various options
- ⬜ Test export functionality
- ⬜ Achieve 85%+ test coverage

### Test Infrastructure
- ⬜ Set up pytest with async support (`pytest-asyncio`)
- ⬜ Configure pytest fixtures
- ⬜ Add coverage reporting
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

## 🚀 Phase 8: Advanced Features (Future)

### Performance Optimization
- 💡 Implement local cache for verified links (`cache.py`)
- 💡 Add cache expiration policies (TTL-based)
- 💡 Support cache clearing command
- 💡 Add benchmark tests for performance

### Enhanced Validation
- 💡 Check for HTTPS vs HTTP security issues
- 💡 Detect redirect chains and loops
- 💡 Validate anchor links (#fragments)
- 💡 Check for robots.txt restrictions
- 💡 Implement rate limiting per domain

### Smart Features
- 💡 Suggest link replacements for broken URLs
- 💡 Integrate with sitemap.xml for validation
- 💡 AI-powered content validation mode
- 💡 Historical link tracking and analytics

### Integration & Automation
- 💡 Git hook integration (pre-commit/pre-push)
- 💡 GitHub Actions workflow template
- 💡 VS Code extension
- 💡 Web dashboard for link health visualization
- 💡 API mode for programmatic access
- 💡 Webhook notifications for broken links

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

- **v0.1.0**: Core scanning + basic validation (Phases 1-3) - 🔄 **IN PROGRESS**
- **v0.2.0**: Rich reporting + CLI interface (Phases 4-5) - ✅ **COMPLETED**
- **v0.3.0**: Testing + CI/CD (Phase 6) - ⬜ **NOT STARTED**
- **v1.0.0**: Full package release (Phase 7) - ⬜ **NOT STARTED**
- **v2.0.0**: Advanced features (Phase 8) - 💡 **FUTURE**

---

## 🎯 Current Sprint Focus

### Week 1-2: Core Infrastructure Completion
- [ ] Implement `utils/logger.py` with Rich logging
- [ ] Implement `utils/config.py` for `.linkguardignore`
- [ ] Add configuration file support (`linkguard.config.json`)
- [ ] Write unit tests for file scanner
- [ ] Write unit tests for URL extractor

### Week 3-4: Testing & Documentation
- [ ] Complete unit test coverage
- [ ] Write integration tests
- [ ] Set up pytest configuration
- [ ] Create comprehensive README
- [ ] Add usage examples

### Week 5-6: Packaging & Release
- [ ] Finalize `pyproject.toml`
- [ ] Test package installation
- [ ] Publish to TestPyPI
- [ ] Publish v1.0.0 to PyPI