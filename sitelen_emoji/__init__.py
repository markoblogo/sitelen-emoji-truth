from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_PATH = ROOT / "profiles" / "default-stable.v1.json"
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*|[.:]")


def load_profile(path: str | Path = DEFAULT_PROFILE_PATH) -> dict[str, Any]:
    """Load a sitelen-emoji profile JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def default_profile() -> dict[str, Any]:
    return load_profile(DEFAULT_PROFILE_PATH)


def lookup(word: str, profile: dict[str, Any] | None = None) -> str | None:
    """Return the sitelen emoji for a word, alias, or utility token."""
    data = profile or default_profile()
    entries = data.get("entries") or {}
    aliases = data.get("aliases") or {}
    key = word.strip().lower()
    base = aliases.get(key, key)
    return entries.get(key) or entries.get(base)


def translate(text: str, profile: dict[str, Any] | None = None) -> str:
    """Translate known toki pona tokens to sitelen emoji, preserving other text."""
    data = profile or default_profile()
    punct = {".": "_punct_period", ":": "_punct_colon"}

    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        key = punct.get(token, token)
        return lookup(key, data) or token

    return TOKEN_RE.sub(replace, text)


defaultProfile = default_profile()

__all__ = ["defaultProfile", "default_profile", "load_profile", "lookup", "translate"]
