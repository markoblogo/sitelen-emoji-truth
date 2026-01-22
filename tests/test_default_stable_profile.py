import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "profiles" / "default-stable.v1.json"


def load_profile():
    """Helper to load the default-stable profile JSON."""
    with PROFILE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_profile_loads_and_has_expected_top_level_shape():
    profile = load_profile()

    # Basic JSON shape
    assert isinstance(profile, dict)

    # Required top-level keys
    for key in ("name", "version", "generated_at", "sources", "aliases", "entries"):
        assert key in profile, f"missing top-level key: {key}"

    # Specific expected metadata
    assert profile["name"] == "sitelen-emoji default-stable"
    assert profile["version"] == "0.1.0"

    # Sources structure
    sources = profile["sources"]
    assert isinstance(sources, list) and sources, "sources should be a non-empty list"
    first_src = sources[0]
    assert first_src.get("type") == "upstream_json"
    assert isinstance(first_src.get("url"), str) and first_src["url"], "url should be a non-empty string"


def test_aliases_are_present_and_resolved_in_entries():
    profile = load_profile()
    aliases = profile["aliases"]
    entries = profile["entries"]

    # Example alias from words/aliases.json
    assert aliases.get("ali") == "ale"

    # The alias and its canonical form should both exist in entries
    assert "ali" in entries
    assert "ale" in entries

    # They should map to the same emoji glyph
    assert entries["ali"] == entries["ale"]


def test_selected_entries_map_to_expected_emojis():
    profile = load_profile()
    entries = profile["entries"]

    expected_pairs = {
        "a": "❗",
        "ala": "❌",
        "ale": "♾️",
        "ali": "♾️",
        "pona": "👍",
        "toki": "🗣️",
        "_punct_period": "➖️",
        "_punct_colon": "➗️",
    }

    for word, expected_emoji in expected_pairs.items():
        assert word in entries, f"{word!r} should be present in entries"
        assert (
            entries[word] == expected_emoji
        ), f"entry for {word!r} should be {expected_emoji!r}, got {entries[word]!r}"
