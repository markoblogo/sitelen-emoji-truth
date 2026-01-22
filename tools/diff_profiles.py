#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Tuple, List

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from tools.profile import load_profile
DEFAULT_OLD = ROOT / "profiles" / "default-stable.v1.json"
DEFAULT_NEW = ROOT / "dist" / "default-stable.json"


def diff_entries(old: Dict[str, str], new: Dict[str, str]) -> Tuple[List[str], List[str], List[Tuple[str, str, str]]]:
    old_keys = set(old.keys())
    new_keys = set(new.keys())

    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)

    changed = []
    for k in sorted(old_keys & new_keys):
        if old[k] != new[k]:
            changed.append((k, old[k], new[k]))

    return added, removed, changed


def main() -> int:
    ap = argparse.ArgumentParser(description="Diff two sitelen-emoji-truth profiles")
    ap.add_argument("--old", type=Path, default=DEFAULT_OLD, help="Old (frozen) profile JSON")
    ap.add_argument("--new", type=Path, default=DEFAULT_NEW, help="New (built) profile JSON")
    args = ap.parse_args()

    old_p = load_profile(args.old)
    new_p = load_profile(args.new)

    added, removed, changed = diff_entries(old_p.entries, new_p.entries)

    print(f"OLD: {args.old}  ({old_p.name} {old_p.version})")
    print(f"NEW: {args.new}  ({new_p.name} {new_p.version})")
    print()

    print(f"Added keys:   {len(added)}")
    print(f"Removed keys: {len(removed)}")
    print(f"Changed keys: {len(changed)}")
    print()

    if added:
        print("## Added")
        for k in added:
            print(f"+ {k}\t{new_p.entries[k]}")
        print()

    if removed:
        print("## Removed")
        for k in removed:
            print(f"- {k}\t{old_p.entries[k]}")
        print()

    if changed:
        print("## Changed")
        for k, a, b in changed:
            print(f"* {k}\t{a}\t=>\t{b}")
        print()

    # exit code: 0 если нет различий, 1 если есть
    return 0 if (not added and not removed and not changed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
