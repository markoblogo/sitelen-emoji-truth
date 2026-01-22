#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "profiles" / "default-stable.v1.json"

def load_profile(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def resolve(word: str, profile: dict) -> str | None:
    word = word.strip().lower()
    aliases = profile.get("aliases", {})
    entries = profile.get("entries", {})
    base = aliases.get(word, word)
    return entries.get(word) or entries.get(base)

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/lookup.py <word> [<word> ...] [--profile path]")
        sys.exit(2)

    args = sys.argv[1:]
    profile_path = DEFAULT_PROFILE

    if "--profile" in args:
        i = args.index("--profile")
        try:
            profile_path = Path(args[i + 1])
        except IndexError:
            print("Error: --profile requires a path")
            sys.exit(2)
        del args[i:i+2]

    profile = load_profile(profile_path)

    exit_code = 0
    for w in args:
        e = resolve(w, profile)
        if e is None:
            print(f"{w}\t<missing>")
            exit_code = 1
        else:
            print(f"{w}\t{e}")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
