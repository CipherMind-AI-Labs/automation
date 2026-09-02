"""Unit tests for centralized configuration system (LLMConfig and config loader)."""

from pathlib import Path
import tempfile
import pytest

from config.config_loader import LLMConfig, load_llm_config, reset_config_cache


def setup_function() -> None:
    """Reset configuration cache before each test."""
    reset_config_cache()


def teardown_function() -> None:
    """Reset configuration cache after each test."""
    reset_config_cache()


def test_load_default_config_yaml() -> None:
    """Test loading LLM settings from default config/config.yaml."""
    cfg = load_llm_config()
    assert isinstance(cfg, LLMConfig)
    assert cfg.provider == "ollama"
    assert cfg.model == "qwen3:4b"
    assert cfg.base_url == "http://localhost:11434"
    assert cfg.temperature == 0.2
    assert cfg.max_tokens == 4096
    assert cfg.timeout == 120
    assert cfg.context_window == 4096


def test_load_custom_yaml_config() -> None:
    """Test loading configuration from a custom YAML file."""
    yaml_content = """
llm:
  provider: openai
  model: gpt-4o
  base_url: https://api.openai.com/v1
  temperature: 0.7
  max_tokens: 8192
  timeout: 60
  context_window: 128000
"""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        cfg = load_llm_config(config_path=temp_path, reload=True)
        assert cfg.provider == "openai"
        assert cfg.model == "gpt-4o"
        assert cfg.base_url == "https://api.openai.com/v1"
        assert cfg.temperature == 0.7
        assert cfg.max_tokens == 8192
        assert cfg.timeout == 60
        assert cfg.context_window == 128000
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_load_custom_toml_config() -> None:
    """Test loading configuration from a custom TOML file."""
    toml_content = """
[llm]
provider = "anthropic"
model = "claude-3-5-sonnet"
base_url = "https://api.anthropic.com"
temperature = 0.3
max_tokens = 4096
timeout = 90
context_window = 200000
"""
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as f:
        f.write(toml_content)
        temp_path = f.name

    try:
        cfg = load_llm_config(config_path=temp_path, reload=True)
        assert cfg.provider == "anthropic"
        assert cfg.model == "claude-3-5-sonnet"
        assert cfg.base_url == "https://api.anthropic.com"
        assert cfg.temperature == 0.3
        assert cfg.max_tokens == 4096
        assert cfg.timeout == 90
        assert cfg.context_window == 200000
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_llm_config_from_dict() -> None:
    """Test instantiating LLMConfig directly from a dictionary."""
    data = {
        "llm": {
            "provider": "ollama",
            "model": "llama3:8b",
            "temperature": "0.5",
            "max_tokens": "2048",
            "timeout": "45",
        }
    }
    cfg = LLMConfig.from_dict(data)
    assert cfg.provider == "ollama"
    assert cfg.model == "llama3:8b"
    assert cfg.temperature == 0.5
    assert cfg.max_tokens == 2048
    assert cfg.timeout == 45
