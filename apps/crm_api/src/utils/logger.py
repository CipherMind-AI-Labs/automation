from __future__ import annotations

import logging
import sys
from typing import Any

# Configure standard logger for CRM API Worker
logger = logging.getLogger("crm_api")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_info(message: str, extra: dict[str, Any] | None = None) -> None:
    """Log an INFO level message.

    Args:
        message: Log message text.
        extra: Additional contextual metadata dictionary.
    """
    if extra:
        logger.info("%s | %s", message, extra)
    else:
        logger.info(message)


def log_warning(message: str, extra: dict[str, Any] | None = None) -> None:
    """Log a WARNING level message.

    Args:
        message: Log message text.
        extra: Additional contextual metadata dictionary.
    """
    if extra:
        logger.warning("%s | %s", message, extra)
    else:
        logger.warning(message)


def log_error(message: str, extra: dict[str, Any] | None = None) -> None:
    """Log an ERROR level message.

    Args:
        message: Log message text.
        extra: Additional contextual metadata dictionary.
    """
    if extra:
        logger.error("%s | %s", message, extra)
    else:
        logger.error(message)
