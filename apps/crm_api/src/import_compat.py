"""Import compatibility for local Python and Cloudflare Workers runtimes."""

from __future__ import annotations

import sys
import types
from pathlib import Path


def configure_src_namespace() -> None:
    """Make the source directory available as the ``src`` package.

    Wrangler executes ``src/app.py`` with ``src`` as the Python import root.
    In that environment, ``src`` itself is therefore not importable.

    Local development and tests normally execute from the project root,
    where ``src`` is importable naturally. This function bridges the two
    environments without changing existing ``src.*`` imports.
    """
    source_dir = Path(__file__).resolve().parent

    if "src" in sys.modules:
        return

    src_package = types.ModuleType("src")
    src_package.__path__ = [str(source_dir)]
    src_package.__package__ = "src"

    sys.modules["src"] = src_package