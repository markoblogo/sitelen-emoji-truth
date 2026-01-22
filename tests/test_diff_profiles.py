from pathlib import Path
from tools.profile import load_profile
from tools.diff_profiles import diff_entries

ROOT = Path(__file__).resolve().parents[1]
P1 = ROOT / "profiles" / "default-stable.v1.json"

def test_diff_same_profile_is_empty():
    p = load_profile(P1)
    added, removed, changed = diff_entries(p.entries, p.entries)
    assert added == []
    assert removed == []
    assert changed == []
