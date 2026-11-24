"""Shared pytest fixtures for the test suite."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


@pytest.fixture
def make_file(tmp_path: Path) -> Callable[[str, str], Path]:
    """Return a factory creating a temporary file with the given name and content.

    Args
    ----
        tmp_path (Path): temporary path automatically filled by `pytest`.

    Returns
    -------
        Callable[[str, str], Path]
            function `(name, content) -> Path` writing the file in `tmp_path`.
    """
    def _make(name: str, content: str) -> Path:
        path = tmp_path / name
        path.write_text(content)
        return path

    return _make
