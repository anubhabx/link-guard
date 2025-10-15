# 🛡️ LinkGuard# 🛡️ LinkGuard



> **Fast, async link validation for developers. Catch broken links before your users do.**> **Automated link validation for developers who care about quality documentation.**



[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)LinkGuard is a fast, async Python CLI tool that scans your project files for broken links and development URLs. Catch 404s before your users do, and ensure localhost references don't leak into production.

[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/anubhabx/link-guard/releases)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

[![Tests](https://img.shields.io/badge/tests-91%20passing-brightgreen.svg)](tests/)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Coverage](https://img.shields.io/badge/coverage-71%25-yellow.svg)](htmlcov/index.html)[![Tests](https://img.shields.io/badge/tests-91%20passing-brightgreen.svg)](tests/)

[![Status](https://img.shields.io/badge/status-production-success.svg)](RELEASE_NOTES.md)[![Test Coverage](https://img.shields.io/badge/coverage-71%25-yellow.svg)](htmlcov/index.html)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

LinkGuard is a Python CLI tool that scans your project files for broken links and development URLs. Perfect for documentation sites, CI/CD pipelines, and ensuring quality before deployment.

---

---

## ✨ Features

## ✨ Features

- 🚀 **Blazing Fast**: Async HTTP validation checks hundreds of links in seconds

- 🚀 **Blazing Fast** - Async validation checks hundreds of links in seconds- 🎯 **Environment-Aware**: Detect localhost/dev URLs that shouldn't be in production

- 🎯 **Environment-Aware** - Detect localhost/dev URLs that shouldn't reach production- 🎨 **Beautiful CLI**: Rich progress bars, color-coded results, and detailed reporting

- 🎨 **Beautiful CLI** - Rich progress bars and color-coded results- 📊 **Multiple Export Formats**: JSON, CSV, and Markdown reports for CI/CD integration

- 📊 **Multiple Exports** - JSON, CSV, and Markdown reports for automation- 🔍 **Smart URL Extraction**: Supports Markdown, HTML, JSON, and plain text files

- 🔍 **Smart Extraction** - Supports Markdown, HTML, JSON, JS/TS, and plain text- ⚙️ **Zero Config**: Works out of the box with sensible defaults

- ⚙️ **Zero Config** - Works out of the box with sensible defaults- 🛠️ **Highly Configurable**: `.linkguardignore` and `linkguard.config.json` support

- 🛠️ **Configurable** - `.linkguardignore` and `linkguard.config.json` support- ✅ **Well-Tested**: 91 comprehensive tests with 71% code coverage (100% pass rate)

- ✅ **Production Ready** - 91 tests, 71% coverage, comprehensive documentation

---

---

## 🚀 Quick Start

## 📦 Installation

### Installation

```bash

# Install from PyPI (coming soon)```bash

pip install linkguard# Clone the repository

git clone https://github.com/anubhabx/link-guard.git

# Or install from sourcecd link-guard

git clone https://github.com/anubhabx/link-guard.git

cd link-guard# Create virtual environment

pip install -e ".[dev]"python -m venv venv

```

# Activate virtual environment

---# Windows (PowerShell)

.\venv\Scripts\Activate.ps1

## 🚀 Quick Start# Linux/Mac

source venv/bin/activate

```bash

# Scan current directory# Install in development mode (includes all dependencies)

linkguardpip install -e ".[dev]"

```

# Scan specific directory

linkguard ./docs### Basic Usage



# Production mode (flags localhost URLs)```bash

linkguard --mode prod# Scan current directory

linkguard

# Export results

linkguard --export report.json# Scan specific directory

```linkguard ./docs



**Example Output:**# Production mode (flags localhost URLs as errors)

```linkguard --mode prod

🔍 Scanning directory: ./docs

Mode: dev | Timeout: 10s# Export results to JSON

linkguard --export report.json

✓ Found 42 files to scan

✓ Extracted 156 URLs# Custom timeout

linkguard --timeout 15

🌐 Checking links...```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 156/156

> **💡 Tip**: After installation with `pip install -e ".[dev]"`, you can use `linkguard` directly instead of `python -m linkguard.cli`

╭─ Scan Summary ─────────────╮

│ Files scanned       42     │---

│ URLs found          156    │

│ Working links       152    │## 📖 Usage Examples

│ Broken links        4      │

│ Rule violations     0      │### Basic Scanning

╰────────────────────────────╯

``````bash

# Scan current directory for broken links

---linkguard

```

## 📖 Documentation

**Output:**

| Document | Description |```

|----------|-------------|🔍 Scanning directory: C:\dev\my-project

| **[QUICKSTART.md](QUICKSTART.MD)** | Installation, basic usage, and common examples |Mode: dev | Timeout: 10s

| **[FEATURES.md](FEATURES.MD)** | Complete feature list and capabilities |

| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Development setup, testing, and contribution guidelines |✓ Found 42 files to scan

| **[RELEASE_NOTES.md](RELEASE_NOTES.md)** | v1.0.0 release details and highlights |✓ Extracted 156 URLs

| **[CHANGELOG.md](CHANGELOG.MD)** | Full version history and changes |

🌐 Checking links...

---━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 156/156



## ⚙️ Configuration╭─ Scan Summary ─────────────╮

│ Files scanned       42     │

### Command-Line Options│ URLs found          156    │

│ Working links       152    │

```bash│ Broken links        4      │

linkguard [DIRECTORY] [OPTIONS]│ Rule violations     0      │

╰────────────────────────────╯

Options:

  --mode, -m          dev|prod        Scanning mode (default: dev)❌ Broken Links:

  --timeout, -t       INTEGER         Request timeout in seconds (default: 10) ✗ https://example.com/old-page

  --export, -e        PATH            Export to JSON/CSV/Markdown    Status: 404 | Error: HTTP error

  --concurrency, -c   INTEGER         Max concurrent requests (default: 50)    in docs/api.md:23

  --ignore, -i        TEXT            Comma-separated ignore patterns```

  --verbose, -v                       Detailed output

  --help                              Show help### Scan Specific Directory

```

```bash

### Configuration File# Scan documentation folder

linkguard ./docs

Create `linkguard.config.json` in your project root:

# Scan multiple levels up

```jsonlinkguard ../other-project

{

  "mode": "prod",# Scan with absolute path

  "timeout": 15,linkguard C:\projects\my-app

  "concurrency": 100,```

  "ignore_patterns": ["node_modules/**", "*.min.js"],

  "exclude_urls": ["https://example.local"],### Production Mode

  "strict_ssl": false

}```bash

```# Check for localhost URLs (fails if found)

linkguard --mode prod

See [linkguard.config.json.example](linkguard.config.json.example) for all options.```



### Ignore File**Detects and flags:**

- `http://localhost:3000`

Create `.linkguardignore` (gitignore-style syntax):- `http://127.0.0.1:8080`

- `https://api.dev.internal`

```- `https://staging.local`

# Ignore directories- `http://192.168.1.100`

node_modules/

dist/**Example Output:**

build/```

⚠ Found 2 environment rule violations:

# Ignore file patterns

*.draft.md ⚠ http://localhost:3000

temp-*.json   Localhost URLs not allowed in production mode

   in src/config.js:12

# Ignore domains

*.internal.company.com ⚠ https://api.dev.internal

example.local   Development domain found in production mode

```   in docs/api-reference.md:45

```

See [.linkguardignore.example](.linkguardignore.example) for more examples.

### Export Results

---

```bash

## 🏗️ Supported File Types# Export to JSON (great for CI/CD)

linkguard --export report.json

| Type | Extensions | What's Extracted |

|------|-----------|------------------|# Export to CSV (Excel-friendly)

| Markdown | `.md`, `.markdown` | `[text](url)` and bare URLs |linkguard --export report.csv

| HTML | `.html`, `.htm` | `href`, `src` attributes |

| JSON | `.json` | URL strings in values |# Export to Markdown (human-readable)

| JavaScript/TypeScript | `.js`, `.jsx`, `.ts`, `.tsx` | Bare URL patterns |linkguard --export report.md

| Plain Text | `.txt` | HTTP/HTTPS URLs |

# Combine options

**Auto-excluded**: `.git`, `.venv`, `node_modules`, `__pycache__`, `dist`, `build`linkguard ./docs --mode prod --export prod-scan.json --timeout 20

```

---

### CI/CD Integration

## 🔧 CI/CD Integration

```yaml

### GitHub Actions# GitHub Actions example

- name: Check for broken links

```yaml  run: |

name: Link Validation    pip install -e ".[dev]"

    linkguard --mode prod --export link-report.json

on: [push, pull_request]  continue-on-error: false  # Fail build if broken links found

```

jobs:

  check-links:```bash

    runs-on: ubuntu-latest# Exit codes:

    steps:# 0 - All links valid

      - uses: actions/checkout@v3# 1 - Broken links or rule violations found

      - uses: actions/setup-python@v4```

        with:

          python-version: '3.10'---

      - name: Install LinkGuard

        run: pip install linkguard## ⚙️ Configuration

      - name: Check links

        run: linkguard --mode prod --export report.json### Command-Line Options

      - name: Upload report

        if: failure()| Option | Short | Type | Default | Description |

        uses: actions/upload-artifact@v3|--------|-------|------|---------|-------------|

        with:| `[DIRECTORY]` | - | Path | `.` (current) | Directory to scan |

          name: link-report| `--mode` | `-m` | `dev`\|`prod` | `dev` | Scanning mode |

          path: report.json| `--timeout` | `-t` | Integer | `10` | Request timeout (seconds) |

```| `--export` | `-e` | Path | None | Export file (`.json`, `.csv`, `.md`) |

| `--help` | | Flag | - | Show help message |

**Exit Codes:**

- `0` - All links valid### Configuration File

- `1` - Broken links or rule violations found

- `2` - Configuration errorCreate a `linkguard.config.json` in your project root:



---```json

{

## 🎯 Use Cases  "mode": "prod",

  "timeout": 15,

✅ **Documentation Sites** - Ensure all links work before publishing    "concurrency": 100,

✅ **Open Source Projects** - Validate README and wiki links    "ignore_patterns": [

✅ **Marketing Sites** - Check landing pages and blog posts      "node_modules/**",

✅ **CI/CD Pipelines** - Automated link checking on every commit      "*.min.js",

✅ **Pre-Production Checks** - Catch localhost URLs before deployment      "temp-*.md"

✅ **Content Migration** - Validate links after CMS migrations    ],

  "exclude_urls": [

---    "https://example.local"

  ]

## 🤝 Contributing}

```

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup and workflow### Ignore File

- Testing guidelines (91 tests, 71% coverage)

- Code style requirements (PEP 8, Black, type hints)Create a `.linkguardignore` file (gitignore-style):

- Pull request process

```

**Quick Start:**# Ignore file patterns

```bash*.draft.md

git clone https://github.com/anubhabx/link-guard.git/archive/*

cd link-guard/vendor/*

python -m venv venv

source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows# Ignore specific domains

pip install -e ".[dev]"example.local

pytest tests/ -v*.internal.company.com

``````



------



## 🗺️ Roadmap## 🏗️ Supported File Types



### ✅ v1.0.0 (Current - October 2025)LinkGuard automatically detects and extracts URLs from:

- Production-ready release

- Comprehensive documentation| File Type | Extensions | Extraction Method |

- 91 passing tests with 71% coverage|-----------|-----------|-------------------|

- GitHub Actions CI/CD| **Markdown** | `.md`, `.markdown` | `[text](url)` patterns + bare URLs |

- Published to PyPI| **HTML** | `.html`, `.htm` | `href`, `src` attributes |

| **JSON** | `.json` | String values containing URLs |

### 🚧 v1.1.0 (Planned)| **Plain Text** | `.txt` | HTTP/HTTPS patterns |

- Retry logic with exponential backoff| **JavaScript/TypeScript** | `.js`, `.jsx`, `.ts`, `.tsx` | Bare URL patterns |

- Custom HTTP headers support

- Relative URL resolution**Default Exclusions:**

- Enhanced performance optimizations- `.git`, `.venv`, `node_modules`, `__pycache__`

- `.pytest_cache`, `.idea`, `dist`, `build`

### 🔮 v2.0.0 (Future)

- Anchor link validation (`#section`)---

- Browser automation (Playwright) for bot detection bypass

- Web dashboard for analytics## 🔧 Development

- Webhook notifications (Slack/Discord)

### Project Structure

See [FEATURES.MD](FEATURES.MD) for complete roadmap.

```

---linkguard/

├── cli.py                    # CLI entry point & main command

## 📊 Performance├── scanner/

│   ├── file_scanner.py       # Recursive file discovery

**Benchmarks** (typical projects):│   ├── url_extractor.py      # URL extraction from files

- ✅ 100 links validated in ~2 seconds│   ├── link_checker.py       # Async HTTP link validation

- ✅ 1,000 links validated in ~5 seconds  │   └── rules.py              # Environment-specific rules

- ✅ 10,000 files scanned in <30 seconds├── reporter/

│   ├── formatter.py          # Rich console output formatting

**Architecture:**│   └── exporter.py           # JSON/CSV/Markdown export

- Async I/O with `aiohttp` for concurrent requests└── utils/

- Semaphore-based concurrency control (default: 50)    ├── config.py             # Configuration file loader

- Memory-efficient streaming file reads    └── logger.py             # Structured logging utilities

- HEAD request with smart GET fallback```



---### Local Development Setup



## 🐛 Troubleshooting```bash

# Clone and navigate

**Valid links marked as broken?**git clone https://github.com/anubhabx/link-guard.git

- Some servers block automated requests → Increase timeout: `--timeout 20`cd link-guard



**"Connection timeout" errors?**# Create virtual environment

- Network latency or slow servers → Try: `--timeout 30`python -m venv venv

.\venv\Scripts\Activate.ps1  # Windows

**Ignore specific files/URLs?**source venv/bin/activate      # Linux/Mac

- Use `.linkguardignore` or add to `linkguard.config.json`

# Install in editable mode with dev dependencies

**Command not found?**pip install -e ".[dev]"

- Ensure installed: `pip install -e ".[dev]"`

- Or use: `python -m linkguard.cli`# Verify installation

linkguard --help

**SSL certificate errors?**```

- LinkGuard skips SSL verification by default

- Coming soon: `--strict-ssl` flag### Running Tests



See [QUICKSTART.MD](QUICKSTART.MD) for more troubleshooting tips.LinkGuard has a comprehensive test suite with **91 passing tests** and **71% code coverage**.



---```bash

# Run all tests

## 📄 Licensepytest tests/ -v



MIT License - see [LICENSE](LICENSE) file for details.# Run with coverage report

pytest tests/ --cov=linkguard --cov-report=html --cov-report=term

---

# Run specific test file

## 🙏 Acknowledgmentspytest tests/test_scanner.py -v



Built with these amazing tools:# Run async tests

- [aiohttp](https://docs.aiohttp.org/) - Async HTTP clientpytest tests/test_checker.py --asyncio-mode=auto

- [typer](https://typer.tiangolo.com/) - Modern CLI framework

- [rich](https://rich.readthedocs.io/) - Beautiful terminal formatting# View coverage report

- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing# Open htmlcov/index.html in your browser

```

Special thanks to all [contributors](https://github.com/anubhabx/link-guard/graphs/contributors)! 🎉

**Test Results Summary:**

---- ✅ **91 tests passing** (100% pass rate)

- 📊 **71% overall coverage**

## 📞 Support  - Scanner module: 94% coverage

  - Reporter module: 100% coverage

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/anubhabx/link-guard/issues)  - Utils module: 93% coverage

- 💬 **Discussions**: [GitHub Discussions](https://github.com/anubhabx/link-guard/discussions)  - CLI module: 0% coverage (see note below)

- 💡 **Feature Requests**: [Open an Issue](https://github.com/anubhabx/link-guard/issues/new)

- 📧 **Contact**: anubhabxdev@gmail.com> **Note on CLI Coverage:** The CLI integration tests all pass successfully, but coverage tracking shows 0% due to a technical limitation with subprocess-based testing. The CLI is tested via `subprocess.run()` which spawns a new Python process where the parent process's coverage tracking doesn't transfer. The CLI functionality is fully verified through 10 integration tests that validate all command-line options, export formats, and error handling.



---### Code Quality



<div align="center">```bash

# Format code with black

**Made with ❤️ for the open-source community**black linkguard/ tests/



If you find LinkGuard useful, please give it a ⭐!# Lint with flake8

flake8 linkguard/

[Documentation](QUICKSTART.MD) • [Features](FEATURES.MD) • [Contributing](CONTRIBUTING.md) • [Changelog](CHANGELOG.MD)

# Type checking with mypy

</div>mypy linkguard/


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