import pytest
import json
from pathlib import Path
from linkguard.utils.config import Config, load_config


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure."""
    return tmp_path


def test_default_config(temp_project):
    """Test that default config is loaded when no config file exists."""
    config = Config(temp_project)
    
    assert config.get("mode") == "dev"
    assert config.get("timeout") == 10
    assert config.get("concurrency") == 50
    assert config.get("strict_ssl") is False


def test_load_config_from_json(temp_project):
    """Test loading config from linkguard.config.json."""
    config_data = {
        "mode": "prod",
        "timeout": 20,
        "concurrency": 100,
    }
    
    config_file = temp_project / "linkguard.config.json"
    config_file.write_text(json.dumps(config_data))
    
    config = Config(temp_project)
    
    assert config.get("mode") == "prod"
    assert config.get("timeout") == 20
    assert config.get("concurrency") == 100


def test_parse_linkguardignore_file(temp_project):
    """Test parsing .linkguardignore file."""
    ignore_file = temp_project / ".linkguardignore"
    ignore_file.write_text("node_modules\n*.draft.md\n# Comment\n\ndist/")
    
    config = Config(temp_project)
    patterns = config.get_ignore_patterns()
    
    assert "node_modules" in patterns
    assert "*.draft.md" in patterns
    assert "dist" in patterns  # Trailing slash removed
    assert "# Comment" not in patterns  # Comments excluded


def test_fallback_to_gitignore(temp_project):
    """Test that .gitignore is used when .linkguardignore doesn't exist."""
    gitignore_file = temp_project / ".gitignore"
    gitignore_file.write_text(".venv\n__pycache__\n*.pyc")
    
    config = Config(temp_project)
    patterns = config.get_ignore_patterns()
    
    assert ".venv" in patterns
    assert "__pycache__" in patterns
    assert "*.pyc" in patterns


def test_linkguardignore_takes_priority(temp_project):
    """Test that .linkguardignore takes priority over .gitignore."""
    gitignore_file = temp_project / ".gitignore"
    gitignore_file.write_text(".venv\nnode_modules")
    
    linkguardignore_file = temp_project / ".linkguardignore"
    linkguardignore_file.write_text("*.draft.md")
    
    config = Config(temp_project)
    patterns = config.get_ignore_patterns()
    
    # Should use .linkguardignore, not .gitignore
    assert "*.draft.md" in patterns
    assert ".venv" not in patterns
    assert "node_modules" not in patterns


def test_recursive_gitignore_collection(temp_project):
    """Test that all .gitignore files in subdirectories are collected."""
    # Root .gitignore
    (temp_project / ".gitignore").write_text("node_modules\n*.log")
    
    # Frontend .gitignore
    frontend = temp_project / "frontend"
    frontend.mkdir()
    (frontend / ".gitignore").write_text("dist/\n.cache/")
    
    # Backend .gitignore
    backend = temp_project / "backend"
    backend.mkdir()
    (backend / ".gitignore").write_text("__pycache__\n*.pyc")
    
    config = Config(temp_project)
    patterns = config.get_ignore_patterns()
    
    # Should merge all patterns
    assert "node_modules" in patterns
    assert "dist" in patterns
    assert "__pycache__" in patterns
    assert "*.log" in patterns


def test_cli_overrides_merge_with_config(temp_project):
    """Test that CLI overrides are merged with config file."""
    config_file = temp_project / "linkguard.config.json"
    config_file.write_text(json.dumps({"mode": "dev", "timeout": 10}))
    
    cli_overrides = {"mode": "prod", "concurrency": 100}
    config = load_config(temp_project, cli_overrides)
    
    assert config.get("mode") == "prod"  # CLI override
    assert config.get("timeout") == 10  # From config file
    assert config.get("concurrency") == 100  # CLI override


def test_cli_ignore_patterns_merge(temp_project):
    """Test that CLI ignore patterns are merged with file patterns."""
    ignore_file = temp_project / ".linkguardignore"
    ignore_file.write_text("node_modules\n*.log")
    
    cli_overrides = {"ignore_patterns": ["*.draft.md", "temp/"]}
    config = load_config(temp_project, cli_overrides)
    
    patterns = config.get_ignore_patterns()
    
    # Should have both file and CLI patterns
    assert "node_modules" in patterns
    assert "*.log" in patterns
    assert "*.draft.md" in patterns
    assert "temp/" in patterns


def test_invalid_json_raises_error(temp_project):
    """Test that invalid JSON in config file raises ValueError."""
    config_file = temp_project / "linkguard.config.json"
    config_file.write_text("{invalid json")
    
    with pytest.raises(ValueError, match="Error parsing config file"):
        Config(temp_project)


def test_should_ignore_path(temp_project):
    """Test path matching against ignore patterns."""
    config = Config(temp_project)
    config.config["ignore_patterns"] = ["node_modules", "*.draft.md", "dist"]
    
    assert config.should_ignore_path(Path("node_modules/package.json"))
    assert config.should_ignore_path(Path("docs/test.draft.md"))
    assert config.should_ignore_path(Path("dist/bundle.js"))
    assert not config.should_ignore_path(Path("docs/readme.md"))


def test_should_exclude_url():
    """Test URL exclusion patterns."""
    config = Config(Path("."))
    config.config["exclude_urls"] = ["https://example.com/*", "http://localhost*"]
    
    assert config.should_exclude_url("https://example.com/page")
    assert config.should_exclude_url("http://localhost:3000")
    assert not config.should_exclude_url("https://github.com")


def test_get_ignore_patterns_returns_list(temp_project):
    """Test that get_ignore_patterns returns a list."""
    config = Config(temp_project)
    patterns = config.get_ignore_patterns()
    
    assert isinstance(patterns, list)


def test_config_handles_empty_ignore_file(temp_project):
    """Test that empty .linkguardignore is handled gracefully."""
    ignore_file = temp_project / ".linkguardignore"
    ignore_file.write_text("\n\n# Only comments\n\n")
    
    config = Config(temp_project)
    patterns = config.get_ignore_patterns()
    
    # Should have no patterns (only comments/whitespace)
    assert len(patterns) == 0


def test_config_repr(temp_project):
    """Test Config __repr__ method."""
    config = Config(temp_project)
    repr_str = repr(config)
    
    assert "Config(" in repr_str
    assert "mode" in repr_str