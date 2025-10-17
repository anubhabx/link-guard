# 🛡️ LinkGuard - Product Requirements Document

**Version:** 1.0.1  
**Last Updated:** 2025-10-15  
**Status:** Production Release (v1.0)  
**Owner:** Development Team

---

## 📋 Executive Summary

LinkGuard is a Python-based CLI tool designed to automatically detect and report broken links, localhost URLs, and development references in project documentation and source files. The tool helps development teams maintain high-quality documentation, prevent broken external references in production, and ensure clean deployments by catching development URLs before they reach production environments.

### Key Value Propositions
- **Automated Link Validation**: Asynchronously check hundreds of URLs in seconds
- **Environment-Aware Scanning**: Detect localhost/dev URLs that shouldn't exist in production
- **Developer-Friendly**: Rich CLI output with progress bars, color-coded results, and detailed reports
- **CI/CD Integration**: Export results in JSON/CSV/Markdown for automated pipelines
- **Zero Configuration**: Works out of the box with sensible defaults

---

## 🎯 Product Vision & Goals

### Vision Statement
*"Make link validation effortless and automated for every development workflow, ensuring documentation and code references remain reliable and production-ready."*

### Primary Goals
1. **Reduce Documentation Debt**: Catch broken links before they frustrate users
2. **Prevent Production Issues**: Flag localhost/dev URLs in pre-deployment checks
3. **Save Developer Time**: Automate manual link checking in large codebases
4. **Enable CI/CD Integration**: Provide machine-readable outputs for automated workflows

### Success Metrics
- **Performance**: Scan 1000 links in < 5 seconds
- **Accuracy**: 95%+ detection rate for broken links
- **Adoption**: 100+ GitHub stars in first 6 months
- **Usage**: 1000+ PyPI downloads in first quarter

---

## 👥 Target Users & Personas

### Primary Personas

#### 1. **Documentation Maintainer (Dana)**
- **Role**: Technical Writer / DevRel Engineer
- **Pain Points**: 
  - Manually checking links in large documentation sites
  - Links break when external sites change
  - No automated way to validate Markdown files
- **Goals**: 
  - Automate link validation in CI/CD
  - Get notified when links break
  - Export reports for stakeholders

#### 2. **DevOps Engineer (Derek)**
- **Role**: Release Manager / Platform Engineer
- **Pain Points**: 
  - Localhost URLs accidentally deployed to production
  - No pre-deployment validation for external references
  - Manual PR reviews for link changes
- **Goals**: 
  - Block deployments with broken links
  - Detect dev URLs in production mode
  - Integrate with GitHub Actions

#### 3. **Open Source Maintainer (Olivia)**
- **Role**: OSS Project Owner
- **Pain Points**: 
  - Contributors add broken links in PRs
  - README files accumulate outdated references
  - No automated checks in contribution workflow
- **Goals**: 
  - Add pre-commit hooks for link validation
  - Maintain high-quality documentation
  - Reduce manual review burden

---

## 🚀 Core Features & Requirements

### 1. File Discovery & Scanning

#### 1.1 Supported File Types
- **Must Have:**
  - Markdown (`.md`, `.markdown`)
  - HTML (`.html`, `.htm`)
  - JSON (`.json`)
  - Plain text (`.txt`)
  - JavaScript/TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`)

- **Nice to Have (v2.0):**
  - Python files (`.py`) - docstrings
  - YAML/TOML config files
  - ReStructuredText (`.rst`)
  - AsciiDoc (`.adoc`)

#### 1.2 Ignore Patterns
- **Default Exclusions:**
  - `.git`, `.venv`, `node_modules`, `__pycache__`
  - `.pytest_cache`, `.idea`, `dist`, `build`

- **Custom Ignore File (`.linkguardignore`):**
  ```
  # Gitignore-style pattern matching
  *.min.js
  /vendor/*
  temp-*.md
  ```

#### 1.3 Configuration File (`linkguard.config.json`)
```json
{
  "mode": "prod",
  "timeout": 15,
  "concurrency": 100,
  "ignore_patterns": ["docs/archive/*"],
  "exclude_urls": ["https://example.local"],
  "retry_attempts": 2
}
```

**Configuration Precedence:**
1. CLI arguments (highest priority)
2. `linkguard.config.json`
3. Default values (lowest priority)

---

### 2. URL Extraction Engine

#### 2.1 Markdown Link Detection
- **Inline Links**: `[text](https://example.com)`
- **Bare URLs**: `https://example.com`
- **Reference Links**: `[text][ref]` → `[ref]: https://example.com`

#### 2.2 HTML Attribute Extraction
- **Anchor tags**: `<a href="...">`
- **Images**: `<img src="...">`
- **Scripts**: `<script src="...">`
- **Stylesheets**: `<link href="...">`
- **Iframes**: `<iframe src="...">`

#### 2.3 JSON Value Extraction
- Recursively search for string values starting with `http://` or `https://`
- Track JSON path for context (e.g., `.config.apiUrl`)

#### 2.4 URL Normalization
- Strip trailing punctuation (`,`, `.`, `)`, `;`)
- Deduplicate URLs within same file
- Preserve fragment identifiers (`#section`)
- Handle encoded characters (`%20`)

---

### 3. Asynchronous Link Validation

#### 3.1 HTTP Request Strategy
- **Concurrency**: Default 50 parallel requests (configurable up to 200)
- **Timeout**: 10 seconds per request (configurable)
- **Redirects**: Follow up to 5 redirects automatically
- **SSL Verification**: Disabled by default (enable with `--strict-ssl`)

#### 3.2 Status Code Categorization
- **2xx (Success)**: Green ✅ Working
- **3xx (Redirect)**: Yellow ⚠️ Warning (follow and report final destination)
- **4xx (Client Error)**: Red ❌ Broken (404, 403, etc.)
- **5xx (Server Error)**: Red ❌ Broken (500, 503, etc.)
- **Connection Errors**: Red ❌ Broken (DNS, timeout, etc.)

#### 3.3 Retry Logic (v1.1)
- Retry transient failures (5xx, timeouts) up to 2 times
- Exponential backoff: 1s, 2s, 4s
- Skip retry for 4xx errors (permanent failures)

#### 3.4 Custom Headers (v1.1)
```bash
linkguard scan --header "User-Agent: LinkGuard/1.0" --header "Authorization: Bearer token"
```

---

### 4. Environment Rules Engine

#### 4.1 Development URL Detection
**Localhost Patterns:**
- `localhost`, `127.0.0.1`, `0.0.0.0`, `::1`
- `192.168.*.*`, `10.*.*.*` (private networks)
- `*.local`, `*.dev`, `*.test`, `*.localhost`

**Rule Violations:**
```python
RuleViolation(
    url="http://localhost:8000",
    rule="no-localhost-in-prod",
    severity="error",
    message="Localhost URLs not allowed in production mode",
    file_path="docs/api.md",
    line_number=42
)
```

#### 4.2 Security Rules (v1.2)
- **HTTP in Production**: Flag non-HTTPS URLs in `--mode prod`
- **Insecure Redirects**: Detect HTTPS → HTTP redirect chains
- **Mixed Content**: Warn about HTTP resources in HTTPS pages

#### 4.3 Custom Rules (v2.0)
```json
{
  "rules": [
    {
      "pattern": "*.internal.company.com",
      "severity": "error",
      "message": "Internal domains not allowed in public docs"
    }
  ]
}
```

---

### 5. Reporting & Export

#### 5.1 Console Output (Rich UI)
```
🛡️ Scanning directory: /project
📁 Found 142 files to scan
🔗 Extracted 387 URLs

🌐 Checking links...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 387/387

╭─ Scan Summary ─────────────╮
│ Files Scanned       142    │
│ URLs Found          387    │
│ Working Links       381    │
│ Broken Links        6      │
│ Rule Violations     2      │
╰────────────────────────────╯

❌ Found 6 broken links:
 - https://oldsite.com (404) in docs/api.md:23
 - https://timeout.example.com (Timeout) in README.md:45
 ...

⚠️ Found 2 rule violations:
 - http://localhost:3000 in src/config.js:12 (no-localhost-in-prod)
```

#### 5.2 JSON Export
```json
{
  "metadata": {
    "timestamp": "2025-01-11T10:30:00Z",
    "total_links": 387,
    "broken_links": 6,
    "violations": 2
  },
  "results": [...],
  "violations": [...]
}
```

#### 5.3 CSV Export
```csv
URL,Status,Error,File,Line,Violation
https://example.com,200,None,docs/api.md,23,None
http://localhost:3000,N/A,Connection,config.js,12,no-localhost-in-prod
```

#### 5.4 Markdown Report
```markdown
# LinkGuard Scan Report

**Generated:** 2025-01-11 10:30:00

## Summary
- Total: 387 links
- Broken: 6 links
- Violations: 2 rules

## Broken Links
| URL | Status | File | Line |
|-----|--------|------|------|
| ... | ... | ... | ... |
```

---

### 6. CLI Interface & Commands

#### 6.1 Primary Command
```bash
linkguard scan [DIRECTORY] [OPTIONS]
```

#### 6.2 Options Reference
| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--mode` | `-m` | `dev`\|`prod` | `dev` | Scanning mode |
| `--timeout` | `-t` | `int` | `10` | Request timeout (seconds) |
| `--export` | `-e` | `path` | `None` | Export file (.json/.csv/.md) |
| `--ignore` | `-i` | `pattern` | `None` | Additional ignore patterns |
| `--concurrency` | `-c` | `int` | `50` | Max parallel requests |
| `--verbose` | `-v` | `flag` | `False` | Detailed logging |
| `--strict-ssl` | | `flag` | `False` | Verify SSL certificates |
| `--no-color` | | `flag` | `False` | Disable colored output |

#### 6.3 Exit Codes
| Code | Meaning |
|------|---------|
| `0` | Success (all links valid) |
| `1` | Broken links found |
| `2` | Configuration error |
| `3` | Dev URLs in production mode |

#### 6.4 Usage Examples
```bash
# Basic scan (current directory)
linkguard scan

# Production mode with export
linkguard scan ./docs --mode prod --export report.json

# Custom timeout and concurrency
linkguard scan --timeout 20 --concurrency 100

# Ignore specific patterns
linkguard scan --ignore "*.temp.md" --ignore "draft/*"

# Verbose logging for debugging
linkguard scan --verbose
```

---

## 🔧 Technical Architecture

### System Components

```
┌─────────────────────────────────────────────┐
│            CLI Interface (Typer)            │
│  - Argument parsing                         │
│  - Rich console output                      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Scanner Pipeline                    │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ FileScanner  │→ │ URLExtractor │        │
│  └──────────────┘  └──────────────┘        │
│         │                  │                │
│         ▼                  ▼                │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ LinkChecker  │  │    Rules     │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Reporter Module                     │
│  - Formatter (console)                      │
│  - Exporter (JSON/CSV/MD)                   │
└─────────────────────────────────────────────┘
```

### Key Dependencies
- **aiohttp**: Async HTTP client for concurrent requests
- **typer**: Modern CLI framework with type hints
- **rich**: Terminal formatting and progress bars
- **beautifulsoup4**: HTML parsing and attribute extraction
- **pytest** + **pytest-asyncio**: Testing framework

### Performance Considerations
- **Async I/O**: All HTTP requests non-blocking
- **Semaphore Limits**: Prevent overwhelming servers
- **Connection Pooling**: Reuse TCP connections
- **Lazy Loading**: Stream file reads, don't load all in memory

---

## 📅 Development Roadmap

### Phase 1: MVP (v0.1.0) - **COMPLETED** ✅
- [x] Core file scanning
- [x] URL extraction (Markdown, HTML, JSON)
- [x] Async link validation
- [x] Basic console output
- [x] Environment rules (localhost detection)

### Phase 2: Enhanced UX (v0.2.0) - **COMPLETED** ✅
- [x] Rich console formatting
- [x] Export to JSON/CSV/Markdown
- [x] Progress bars and spinners
- [x] Configuration file support
- [x] `.linkguardignore` implementation

### Phase 3: Testing & Quality (v0.3.0) - **COMPLETED** ✅
- [x] Unit test coverage (71% - 91 tests)
- [x] Integration tests (10 CLI tests)
- [x] GitHub Actions CI
- [x] Logger implementation
- [x] Test infrastructure

### Phase 4: Production Release (v1.0) - **COMPLETED** ✅ (October 15, 2025)
- [x] Package on PyPI (TestPyPI published, PyPI ready)
- [x] Comprehensive documentation (README, CONTRIBUTING, examples)
- [x] Example configurations (.linkguardignore.example, config.json.example)
- [x] Type hints and docstrings (all modules enhanced)
- [x] RELEASE_NOTES.md
- [ ] Video tutorials (planned for v1.1)
- [ ] Community Discord server (planned)

### Phase 5: Enhanced Features (v1.1.0) - **NEXT** 🔄
- [ ] Retry logic with exponential backoff
- [ ] Custom headers support
- [ ] Relative URL resolution
- [ ] Performance benchmarks
- [ ] Pre-commit hooks template

### Phase 6: Advanced Features (v2.0.0) - **FUTURE** 💡
- [ ] Link caching with TTL
- [ ] Anchor link validation (#section)
- [ ] Browser automation (Playwright)
- [ ] Web dashboard
- [ ] Webhook notifications

---

## 🎨 User Experience Principles

### 1. **Progressive Disclosure**
- Simple defaults work for 80% of use cases
- Advanced options available but not required
- Help text guides users to correct usage

### 2. **Immediate Feedback**
- Real-time progress indicators
- Color-coded results (green/yellow/red)
- Clear error messages with actionable fixes

### 3. **Graceful Degradation**
- Continue scanning on individual failures
- Aggregate errors in final report
- Never crash on malformed input

### 4. **Developer Empathy**
- Fast execution (< 5s for typical projects)
- Machine-readable outputs for CI/CD
- Verbose mode for debugging

---

## 🔒 Security & Privacy

### Data Handling
- **No Data Collection**: LinkGuard never sends data to external servers
- **Local Execution**: All scanning happens on user's machine
- **SSL Handling**: SSL verification optional (some dev servers use self-signed certs)

### Responsible Scanning
- **Rate Limiting**: Respect server resources with configurable concurrency
- **User-Agent**: Identify as LinkGuard in HTTP headers
- **Robots.txt** (v1.2): Respect crawl restrictions

---

## 📊 Competitive Analysis

| Feature | LinkGuard | linkchecker | markdown-link-check | lychee |
|---------|-----------|-------------|---------------------|--------|
| Async Scanning | ✅ | ❌ | ✅ | ✅ |
| Environment Rules | ✅ | ❌ | ❌ | ❌ |
| Rich CLI Output | ✅ | ❌ | ❌ | ✅ |
| JSON/CSV Export | ✅ | ✅ | ✅ | ✅ |
| Python-based | ✅ | ✅ | ❌ (Node) | ❌ (Rust) |
| Config File | 🔄 | ✅ | ✅ | ✅ |
| Link Caching | 🔄 | ✅ | ❌ | ✅ |

**Differentiators:**
- Environment-aware scanning (localhost detection)
- Beautiful Rich UI with progress bars
- Python ecosystem integration
- Simple configuration with sensible defaults

---

## 📝 Open Questions & Future Considerations

### Questions to Resolve
1. Should we support relative URL resolution? (e.g., `../docs/api.md`)
2. How to handle rate limiting for external APIs?
3. Should we validate anchor links (`#section-name`)?
4. Support for authenticated requests (OAuth, API keys)?

### Future Exploration
- [ ] Web dashboard for link health tracking
- [ ] GitHub App integration (auto-comment on PRs)
- [ ] Slack/Discord notifications for broken links
- [ ] VS Code extension for inline validation
- [ ] SaaS version with scheduled scans

---

## 🤝 Contributing & Community

### Contribution Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use conventional commits

### Community Channels
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Q&A and ideas
- **Discord** (v1.0): Real-time community support
- **Twitter**: @LinkGuardDev (coming soon)

---

## 📄 License & Legal

- **License**: MIT License
- **Copyright**: 2025 LinkGuard Contributors
- **Trademarks**: "LinkGuard" name and logo

---

## 📞 Contact & Support

- **Email**: support@linkguard.dev
- **GitHub**: https://github.com/linkguard/linkguard
- **Documentation**: https://linkguard.dev/docs

---

*This PRD is a living document and will be updated as the product evolves.*

