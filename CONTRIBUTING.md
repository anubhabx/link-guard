# Contributing to LinkGuard

Thank you for considering contributing to LinkGuard! This document provides guidelines and instructions for contributing to the project.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- pip and virtualenv

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/link-guard.git
   cd link-guard
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify Installation**
   ```bash
   pytest tests/ -v
   linkguard --help
   ```

## 🌿 Git Workflow

We follow a **feature branch workflow**. Never commit directly to `master`.

### Creating a Feature Branch

```bash
# Create and switch to a new feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### Branch Naming Conventions
- **Features**: `feature/descriptive-name`
- **Bug Fixes**: `fix/issue-description`
- **Documentation**: `docs/what-changed`
- **Tests**: `test/what-tested`
- **Refactoring**: `refactor/what-refactored`

### Making Changes

1. **Make your changes** in the feature branch
2. **Write or update tests** for your changes
3. **Run tests** to ensure everything passes:
   ```bash
   pytest tests/ -v --cov=linkguard
   ```
4. **Format your code**:
   ```bash
   black linkguard/ tests/
   ```
5. **Check code quality**:
   ```bash
   flake8 linkguard/ tests/ --max-line-length=100 --extend-ignore=E203,W503
   ```

### Committing Changes

Use clear, descriptive commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) format:

```bash
# Format: <type>(<scope>): <description>

git add .
git commit -m "feat(scanner): add support for .rst files"
git commit -m "fix(checker): handle SSL certificate errors gracefully"
git commit -m "docs(readme): add installation instructions"
git commit -m "test(extractor): add tests for JSON URL extraction"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### Merging to Master

1. **Ensure all tests pass**:
   ```bash
   pytest tests/ -v --cov=linkguard --cov-fail-under=70
   ```

2. **Merge to master**:
   ```bash
   git checkout master
   git merge feature/your-feature-name
   ```

3. **Delete the feature branch**:
   ```bash
   git branch -d feature/your-feature-name
   ```

4. **Push to remote** (if applicable):
   ```bash
   git push origin master
   git push origin --delete feature/your-feature-name
   ```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=linkguard --cov-report=html

# Run specific test file
pytest tests/test_scanner.py -v

# Run specific test
pytest tests/test_scanner.py::test_scan_discovers_markdown_files -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_<module>.py`
- Name test functions as `test_<description>`
- Use pytest fixtures for common setup
- Mock external dependencies (HTTP requests, file I/O)
- Aim for at least 70% code coverage

**Example Test:**
```python
import pytest
from pathlib import Path

def test_url_extraction_from_markdown(tmp_path):
    """Test that URLs are correctly extracted from Markdown files."""
    # Arrange
    md_file = tmp_path / "test.md"
    md_file.write_text("[Link](https://example.com)")
    
    # Act
    extractor = URLExtractor()
    urls = extractor.extract_from_file(md_file)
    
    # Assert
    assert len(urls) == 1
    assert urls[0]["url"] == "https://example.com"
```

### Async Tests

For async code, use `pytest-asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_link_checking():
    """Test asynchronous link validation."""
    # Your async test code here
    pass
```

## 📝 Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings (enforced by Black)
- **Imports**: Organized (standard lib → third-party → local)

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Optional, Dict, Any
from pathlib import Path

def process_files(
    file_paths: List[Path],
    config: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Process a list of files.
    
    Args:
        file_paths: List of file paths to process
        config: Optional configuration dictionary
        
    Returns:
        List of processed file contents
    """
    # Implementation here
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of function.
    
    Longer description if needed, explaining what the function does,
    any important details, edge cases, etc.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        
    Example:
        >>> example_function("test", 5)
        True
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
    return True
```

### Code Formatting

Use **Black** for automatic formatting:

```bash
# Format all code
black linkguard/ tests/

# Check without modifying
black --check linkguard/ tests/
```

### Linting

Use **flake8** for linting:

```bash
flake8 linkguard/ tests/ --max-line-length=100 --extend-ignore=E203,W503
```

### Type Checking (Optional)

Use **mypy** for static type checking:

```bash
mypy linkguard/ --ignore-missing-imports
```

## 🏗️ Architecture Guidelines

### Code Organization

```
linkguard/
├── scanner/          # Core scanning logic
│   ├── file_scanner.py     # File discovery
│   ├── url_extractor.py    # URL extraction
│   ├── link_checker.py     # Link validation
│   └── rules.py            # Environment rules
├── reporter/         # Result reporting
│   ├── exporter.py         # JSON/CSV/Markdown export
│   └── formatter.py        # Console formatting (currently empty)
├── utils/            # Utilities
│   ├── config.py           # Configuration management
│   └── logger.py           # Logging utilities
└── cli.py            # CLI interface
```

### Design Principles

1. **Single Responsibility**: Each module should have one clear purpose
2. **Async-First**: All I/O operations should be asynchronous
3. **Type Safety**: Use type hints for better code clarity
4. **Error Handling**: Gracefully handle errors, don't crash
5. **Testability**: Write code that's easy to test

### Pipeline Pattern

LinkGuard follows a pipeline pattern:

```
Scanner → Extractor → Checker → Rules → Reporter
```

When adding features, consider which part of the pipeline they belong to.

## 🐛 Reporting Issues

### Before Submitting an Issue

1. Check if the issue already exists
2. Verify you're using the latest version
3. Collect relevant information (OS, Python version, error messages)

### Issue Template

```markdown
**Description**
Clear description of the issue

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Windows 11, Ubuntu 22.04]
- Python Version: [e.g., 3.11.5]
- LinkGuard Version: [e.g., 0.3.0]

**Additional Context**
Any other relevant information
```

## 📦 Pull Request Process

1. **Create a feature branch** from `master`
2. **Make your changes** with clear commits
3. **Update tests** and ensure they pass
4. **Update documentation** if needed
5. **Run code quality checks**
6. **Create a Pull Request** with a clear description

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] New tests added for changes
- [ ] Code coverage maintained or improved

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Improve test coverage (target: 85%+)
- [ ] Add retry logic for transient failures
- [ ] Support custom headers for authenticated requests
- [ ] Relative URL resolution

### Medium Priority
- [ ] Link caching with TTL
- [ ] Performance benchmarks
- [ ] Pre-commit hooks template
- [ ] Additional export formats

### Low Priority
- [ ] Browser mode (Playwright integration)
- [ ] VS Code extension
- [ ] GitHub Action
- [ ] Web dashboard

## 💬 Communication

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## 📄 License

By contributing to LinkGuard, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Thank you for contributing to LinkGuard! Your efforts help make this project better for everyone.

---

**Questions?** Feel free to ask in GitHub Discussions or open an issue.
