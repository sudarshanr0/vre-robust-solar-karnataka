"""Shared setup for the toy scripts: import path, figure directory, banner."""

from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
FIG_DIR = BASE_DIR / "reports" / "figures"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def figure_path(name: str) -> Path:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    return FIG_DIR / name


def banner(title: str, question: str) -> None:
    print("=" * 78)
    print(title)
    print("-" * 78)
    print(question)
    print("=" * 78)
    print()
