"""Central configuration loader for the Automation platform.

This module provides the `LLMConfig` dataclass and `load_llm_config` loader function
to maintain a centralized configuration system for LLM settings across all agents.
"""

from dataclasses import dataclass, field
import logging
from pathlib import Path
import sys
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_CACHED_LLM_CONFIG: Optional["LLMConfig"] = None


@dataclass
class LLMConfig:
    """Central configuration container for LLM settings.

    Parameters
    ----------
    provider : str
        LLM provider name (e.g. 'ollama', 'openai', 'anthropic').
    model : str
        Model identifier string (e.g. 'qwen3:4b').
    base_url : str
        Base service endpoint URL for the LLM provider API.
    temperature : float
        Sampling temperature parameter controlling response randomness.
    max_tokens : int
        Maximum number of output tokens generated per request.
    timeout : int
        Timeout limit in seconds for LLM operations.
    context_window : int
        Maximum context window size supported in tokens.
    """

    provider: str = "ollama"
    model: str = "qwen3:4b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.2
    max_tokens: int = 4096
    timeout: int = 120
    context_window: int = 4096

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMConfig":
        """Create an LLMConfig instance from a raw dictionary mapping.

        Parameters
        ----------
        data : Dict[str, Any]
            Dictionary containing configuration attributes under 'llm' or top-level keys.

        Returns
        -------
        LLMConfig
            Configured LLMConfig object.
        """
        llm_data = data.get("llm", data)
        if not isinstance(llm_data, dict):
            llm_data = {}

        return cls(
            provider=str(llm_data.get("provider", "ollama")),
            model=str(llm_data.get("model", "qwen3:4b")),
            base_url=str(llm_data.get("base_url", "http://localhost:11434")),
            temperature=float(llm_data.get("temperature", 0.2)),
            max_tokens=int(llm_data.get("max_tokens", 4096)),
            timeout=int(llm_data.get("timeout", 120)),
            context_window=int(llm_data.get("context_window", 4096)),
        )


def _parse_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Parse a YAML file using PyYAML if available or fallback line parser."""
    content = file_path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        parsed = yaml.safe_load(content)
        if isinstance(parsed, dict):
            return parsed
    except ImportError:
        logger.debug("PyYAML not installed. Fallback to lightweight parser.")

    # Lightweight YAML parser fallback for key-value structures
    result: Dict[str, Any] = {}
    current_section: Optional[str] = None

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.endswith(":") and not ":" in line[:-1]:
            current_section = line[:-1].strip()
            if current_section not in result:
                result[current_section] = {}
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip("\"'")

            # Cast primitives if possible
            typed_val: Any = val
            if val.lower() == "true":
                typed_val = True
            elif val.lower() == "false":
                typed_val = False
            else:
                try:
                    if "." in val:
                        typed_val = float(val)
                    else:
                        typed_val = int(val)
                except ValueError:
                    typed_val = val

            if current_section:
                result[current_section][key] = typed_val
            else:
                result[key] = typed_val

    return result


def _parse_toml_file(file_path: Path) -> Dict[str, Any]:
    """Parse a TOML file using tomllib standard library (Python 3.11+)."""
    if sys.version_info >= (3, 11):
        import tomllib  # type: ignore

        with file_path.open("rb") as f:
            return tomllib.load(f)
    else:
        try:
            import toml  # type: ignore

            return toml.loads(file_path.read_text(encoding="utf-8"))
        except ImportError:
            logger.warning("TOML library unavailable for parsing TOML config file.")
            return {}


def load_llm_config(
    config_path: Optional[str] = None, reload: bool = False
) -> LLMConfig:
    """Load platform LLM settings from configuration file.

    Checks specified path, `config/config.yaml`, `config.yaml`, or `config.toml`.
    Returns default `LLMConfig` if no file is found.

    Parameters
    ----------
    config_path : Optional[str], optional
        Explicit path to configuration file.
    reload : bool, optional
        Flag to force re-reading configuration file and bypassing cache.

    Returns
    -------
    LLMConfig
        Loaded or default LLM configuration object.
    """
    global _CACHED_LLM_CONFIG

    if _CACHED_LLM_CONFIG is not None and not reload and config_path is None:
        return _CACHED_LLM_CONFIG

    search_paths = []
    if config_path:
        search_paths.append(Path(config_path))
    else:
        root_dir = Path(__file__).resolve().parent.parent
        search_paths.extend(
            [
                root_dir / "config" / "config.yaml",
                root_dir / "config.yaml",
                root_dir / "config" / "config.toml",
                root_dir / "config.toml",
            ]
        )

    config_data: Dict[str, Any] = {}
    loaded_file: Optional[Path] = None

    for path in search_paths:
        if path.is_file():
            logger.info(f"Loading platform configuration from: {path}")
            if path.suffix.lower() in [".yaml", ".yml"]:
                config_data = _parse_yaml_file(path)
                loaded_file = path
                break
            elif path.suffix.lower() == ".toml":
                config_data = _parse_toml_file(path)
                loaded_file = path
                break

    if not loaded_file:
        logger.info("No configuration file found. Using default LLMConfig settings.")

    llm_config = LLMConfig.from_dict(config_data)

    if config_path is None and not reload:
        _CACHED_LLM_CONFIG = llm_config

    return llm_config


def reset_config_cache() -> None:
    """Clear cached LLMConfig object (primarily for unit testing)."""
    global _CACHED_LLM_CONFIG
    _CACHED_LLM_CONFIG = None
