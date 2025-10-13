# 🛡️ LinkGuard

> **Automated link validation for developers who care about quality documentation.**

LinkGuard is a fast, async Python CLI tool that scans your project files for broken links and development URLs. Catch 404s before your users do, and ensure localhost references don't leak into production.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-91%20passing-brightgreen.svg)](tests/)
[![Test Coverage](https://img.shields.io/badge/coverage-71%25-yellow.svg)](htmlcov/index.html)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## ✨ Features

- 🚀 **Blazing Fast**: Async HTTP validation checks hundreds of links in seconds
- 🎯 **Environment-Aware**: Detect localhost/dev URLs that shouldn't be in production
- 🎨 **Beautiful CLI**: Rich progress bars, color-coded results, and detailed reporting
- 📊 **Multiple Export Formats**: JSON, CSV, and Markdown reports for CI/CD integration
- 🔍 **Smart URL Extraction**: Supports Markdown, HTML, JSON, and plain text files
- ⚙️ **Zero Config**: Works out of the box with sensible defaults
- 🛠️ **Highly Configurable**: `.linkguardignore` and `linkguard.config.json` support
- ✅ **Well-Tested**: 91 comprehensive tests with 71% code coverage (100% pass rate)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/anubhabx/link-guard.git
cd link-guard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# Install in development mode (includes all dependencies)
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Scan current directory
linkguard

# Scan specific directory
linkguard ./docs

# Production mode (flags localhost URLs as errors)
linkguard --mode prod

# Export results to JSON
linkguard --export report.json

# Custom timeout
linkguard --timeout 15
```

> **💡 Tip**: After installation with `pip install -e ".[dev]"`, you can use `linkguard` directly instead of `python -m linkguard.cli`

---

## 📖 Usage Examples

### Basic Scanning

```bash
# Scan current directory for broken links
linkguard
```

**Output:**
```
🔍 Scanning directory: C:\dev\my-project
Mode: dev | Timeout: 10s

✓ Found 42 files to scan
✓ Extracted 156 URLs

🌐 Checking links...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 156/156

╭─ Scan Summary ─────────────╮
│ Files scanned       42     │
│ URLs found          156    │
│ Working links       152    │
│ Broken links        4      │
│ Rule violations     0      │
╰────────────────────────────╯

❌ Broken Links:
 ✗ https://example.com/old-page
    Status: 404 | Error: HTTP error
    in docs/api.md:23
```

### Scan Specific Directory

```bash
# Scan documentation folder
linkguard ./docs

# Scan multiple levels up
linkguard ../other-project

# Scan with absolute path
linkguard C:\projects\my-app
```

### Production Mode

```bash
# Check for localhost URLs (fails if found)
linkguard --mode prod
```

**Detects and flags:**
- `http://localhost:3000`
- `http://127.0.0.1:8080`
- `https://api.dev.internal`
- `https://staging.local`
- `http://192.168.1.100`

**Example Output:**
```
⚠ Found 2 environment rule violations:

 ⚠ http://localhost:3000
   Localhost URLs not allowed in production mode
   in src/config.js:12

 ⚠ https://api.dev.internal
   Development domain found in production mode
   in docs/api-reference.md:45
```

### Export Results

```bash
# Export to JSON (great for CI/CD)
linkguard --export report.json

# Export to CSV (Excel-friendly)
linkguard --export report.csv

# Export to Markdown (human-readable)
linkguard --export report.md

# Combine options
linkguard ./docs --mode prod --export prod-scan.json --timeout 20
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Check for broken links
  run: |
    pip install -e ".[dev]"
    linkguard --mode prod --export link-report.json
  continue-on-error: false  # Fail build if broken links found
```

```bash
# Exit codes:
# 0 - All links valid
# 1 - Broken links or rule violations found
```

---

## ⚙️ Configuration

### Command-Line Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `[DIRECTORY]` | - | Path | `.` (current) | Directory to scan |
| `--mode` | `-m` | `dev`\|`prod` | `dev` | Scanning mode |
| `--timeout` | `-t` | Integer | `10` | Request timeout (seconds) |
| `--export` | `-e` | Path | None | Export file (`.json`, `.csv`, `.md`) |
| `--help` | | Flag | - | Show help message |

### Configuration File

Create a `linkguard.config.json` in your project root:

```json
{
  "mode": "prod",
  "timeout": 15,
  "concurrency": 100,
  "ignore_patterns": [
    "node_modules/**",
    "*.min.js",
    "temp-*.md"
  ],
  "exclude_urls": [
    "https://example.local"
  ]
}
```

### Ignore File

Create a `.linkguardignore` file (gitignore-style):

```
# Ignore file patterns
*.draft.md
/archive/*
/vendor/*

# Ignore specific domains
example.local
*.internal.company.com
```

---

## 🏗️ Supported File Types

LinkGuard automatically detects and extracts URLs from:

| File Type | Extensions | Extraction Method |
|-----------|-----------|-------------------|
| **Markdown** | `.md`, `.markdown` | `[text](url)` patterns + bare URLs |
| **HTML** | `.html`, `.htm` | `href`, `src` attributes |
| **JSON** | `.json` | String values containing URLs |
| **Plain Text** | `.txt` | HTTP/HTTPS patterns |
| **JavaScript/TypeScript** | `.js`, `.jsx`, `.ts`, `.tsx` | Bare URL patterns |

**Default Exclusions:**
- `.git`, `.venv`, `node_modules`, `__pycache__`
- `.pytest_cache`, `.idea`, `dist`, `build`

---

## 🔧 Development

### Project Structure

```
linkguard/
├── cli.py                    # CLI entry point & main command
├── scanner/
│   ├── file_scanner.py       # Recursive file discovery
│   ├── url_extractor.py      # URL extraction from files
│   ├── link_checker.py       # Async HTTP link validation
│   └── rules.py              # Environment-specific rules
├── reporter/
│   ├── formatter.py          # Rich console output formatting
│   └── exporter.py           # JSON/CSV/Markdown export
└── utils/
    ├── config.py             # Configuration file loader
    └── logger.py             # Structured logging utilities
```

### Local Development Setup

```bash
# Clone and navigate
git clone https://github.com/anubhabx/link-guard.git
cd link-guard

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
linkguard --help
```

### Running Tests

LinkGuard has a comprehensive test suite with **91 passing tests** and **71% code coverage**.

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=linkguard --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_scanner.py -v

# Run async tests
pytest tests/test_checker.py --asyncio-mode=auto

# View coverage report
# Open htmlcov/index.html in your browser
```

**Test Results Summary:**
- ✅ **91 tests passing** (100% pass rate)
- 📊 **71% overall coverage**
  - Scanner module: 94% coverage
  - Reporter module: 100% coverage
  - Utils module: 93% coverage
  - CLI module: 0% coverage (see note below)

> **Note on CLI Coverage:** The CLI integration tests all pass successfully, but coverage tracking shows 0% due to a technical limitation with subprocess-based testing. The CLI is tested via `subprocess.run()` which spawns a new Python process where the parent process's coverage tracking doesn't transfer. The CLI functionality is fully verified through 10 integration tests that validate all command-line options, export formats, and error handling.

### Code Quality

```bash
# Format code with black
black linkguard/ tests/

# Lint with flake8
flake8 linkguard/

# Type checking with mypy
mypy linkguard/

# Run all quality checks
black linkguard/ && flake8 linkguard/ && mypy linkguard/
```

---

## 🤝 Contributing

We welcome contributions! Whether it's:

- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🔧 Code contributions

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/anubhabx/link-guard.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clean, documented code
   - Add tests for new features
   - Update documentation
   - Follow PEP 8 style guide

4. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
   
   Use [conventional commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation updates
   - `test:` Test additions/changes
   - `refactor:` Code refactoring
   - `chore:` Maintenance tasks

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Wait for code review

### Development Guidelines

- **Code Style**: Follow PEP 8, enforced by Black (100 char line length)
- **Type Hints**: Use type hints for all function signatures
- **Documentation**: Add docstrings to all public functions/classes
- **Testing**: Write tests for new features (targeting 85%+ coverage)
- **Commits**: Use conventional commit format

---

## 🗺️ Roadmap

### Current Version: v0.2.0 ✅ **COMPLETED**

- [x] Core async link validation
- [x] Environment rules (localhost detection)
- [x] Rich CLI output with progress bars
- [x] Export to JSON/CSV/Markdown
- [x] Beautiful summary tables
- [x] Configuration file support (`linkguard.config.json`)
- [x] `.linkguardignore` implementation
- [x] All CLI options (mode, export, timeout, concurrency, ignore, verbose)
- [x] Comprehensive test suite (91 tests, 71% coverage)
- [x] Logger implementation with Rich formatting

### Upcoming Releases

**v1.0.0 - Production Release** (Target: 4-6 weeks)
- [ ] PyPI package publication
- [ ] Comprehensive documentation improvements
- [ ] Usage video tutorials
- [ ] Example configurations repository
- [ ] GitHub Actions CI/CD workflow
- [ ] Pre-commit hooks template
- [ ] 85%+ test coverage target
- [ ] Community Discord server
- [ ] 100+ GitHub stars

**v1.1.0 - Enhanced Features** (Future)
- [ ] Retry logic with exponential backoff
- [ ] Custom HTTP headers support
- [ ] Relative URL resolution
- [ ] Link caching with TTL
- [ ] Exit code 3 for dev URLs in prod mode (currently uses exit code 1)

**v2.0.0 - Advanced Features** (Future)
- [ ] Anchor link validation (`#section`)
- [ ] Browser automation with Playwright (bypass bot detection)
- [ ] AI-powered link suggestions
- [ ] Web dashboard for analytics
- [ ] Slack/Discord webhook notifications

See [FEATURES.MD](FEATURES.MD) for detailed feature tracking.

---

## 📊 Performance

LinkGuard is designed for speed and efficiency:

- ⚡ **Async I/O**: Non-blocking HTTP requests using aiohttp
- 🔄 **Concurrent Scanning**: Check 50+ links simultaneously (configurable)
- 💾 **Memory Efficient**: Stream file reads, no full-file loading
- 🎯 **Smart Defaults**: Optimized timeout (10s) and concurrency (50) settings

**Benchmarks** (Tested on typical projects):
- ✅ 100 links validated in < 2 seconds
- ✅ 1000 links validated in ~5 seconds
- ✅ 10,000 files scanned in < 30 seconds

---

## 🐛 Troubleshooting

### Common Issues

**Q: Why are some valid links marked as broken?**
- Some servers block automated requests or have aggressive rate limiting
- **Solution**: Increase timeout: `linkguard --timeout 20`

**Q: Getting "Connection timeout" errors**
- Network latency or slow servers
- **Solution**: Increase timeout: `linkguard --timeout 30`

**Q: How do I ignore specific files or URLs?**
- Use `.linkguardignore` file (gitignore-style patterns)
- Or add `ignore_patterns` and `exclude_urls` to `linkguard.config.json`
- Or use CLI flag: `linkguard --ignore "*.draft.md,temp/*"`

**Q: Can I validate relative links (`./page.html`)?**
- Not yet. Only absolute URLs (`https://...`) are supported
- **Planned for v1.1.0**: Relative link resolution

**Q: SSL certificate errors?**
- LinkGuard skips SSL verification by default to support dev environments
- **Coming in v1.0.0**: `--strict-ssl` flag for strict SSL checking

**Q: Command not found: `linkguard`**
- Install package first: `pip install -e ".[dev]"`
- Or use: `python -m linkguard.cli` instead

**Q: How do I use this in CI/CD?**
```yaml
steps:
  - uses: actions/checkout@v2
  - uses: actions/setup-python@v2
    with:
      python-version: '3.10'
  - run: |
      cd link-guard
      pip install -e ".[dev]"
      linkguard --mode prod --export report.json
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with amazing open-source tools:

- [aiohttp](https://docs.aiohttp.org/) - Async HTTP client for concurrent requests
- [typer](https://typer.tiangolo.com/) - Modern CLI framework with type hints
- [rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing made easy

Special thanks to all [contributors](https://github.com/anubhabx/link-guard/graphs/contributors)! 🎉

---

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/anubhabx/link-guard/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/anubhabx/link-guard/discussions)
- 💡 **Feature Requests**: [Open an Issue](https://github.com/anubhabx/link-guard/issues/new)
- 📧 **Email**: anubhabxdev@gmail.com

---

## ⭐ Star History

If you find LinkGuard useful, please consider giving it a star! ⭐

It helps others discover the project and motivates continued development.

[![Star History Chart](https://api.star-history.com/svg?repos=anubhabx/link-guard&type=Date)](https://star-history.com/#anubhabx/link-guard&Date)

---

**Made with ❤️ by the open-source community**

*Contributions, issues, and feature requests are welcome!*

### Known Limitations

**Sites with Aggressive Bot Protection**
Some sites (Pexels, Medium, etc.) may return `403 Forbidden` even for valid links due to bot detection. This is expected behavior - these sites intentionally block automated tools.

**Workarounds:**
- Use `--exclude-urls` in config to skip specific domains
- Manually verify these links in a browser
- Coming in v2.0: Browser automation mode (Playwright)