"""Central configuration package for the Automation platform."""

from config.config_loader import LLMConfig, load_llm_config

__all__ = ["LLMConfig", "load_llm_config"]
