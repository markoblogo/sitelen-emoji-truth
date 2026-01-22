# sitelen-emoji-truth
A pinned, versioned “source of truth” profile for toki pona → sitelen emoji, with reproducible book-ready visuals.

[![build](https://github.com/markoblogo/sitelen-emoji-truth/actions/workflows/build.yml/badge.svg)](https://github.com/markoblogo/sitelen-emoji-truth/actions/workflows/build.yml)
[![release](https://img.shields.io/github/v/release/markoblogo/sitelen-emoji-truth?sort=semver)](https://github.com/markoblogo/sitelen-emoji-truth/releases)
[![tag](https://img.shields.io/github/v/tag/markoblogo/sitelen-emoji-truth?sort=semver)](https://github.com/markoblogo/sitelen-emoji-truth/tags)
[![license](https://img.shields.io/github/license/markoblogo/sitelen-emoji-truth)](https://github.com/markoblogo/sitelen-emoji-truth/blob/main/LICENSE)

<p align="center">
  <img src="docs/cover.png" alt="sitelen-emoji-truth cover" width="980" />
</p>

Canonical **frozen** mapping for **toki pona → sitelen emoji**.

> Goal: one stable “source of truth” for production (translator, books), with reproducible visuals.

---

## What is frozen vs generated

- **Frozen (source of truth):**
  - `profiles/default-stable.v1.json` — pinned mapping intended for integrations and publishing.

- **Generated (for comparison / upstream tracking):**
  - `dist/default-stable.json` — produced by `tools/build_default_stable.py` from upstream sources.
  - Use `tools/diff_profiles.py` to see what changed vs frozen.

---

## Pinned profile URL (recommended for integrations)

Pin to a **git tag** (recommended) and fetch the frozen profile via `raw.githubusercontent.com`.

Example:

```text
https://raw.githubusercontent.com/markoblogo/sitelen-emoji-truth/v1.0.0/profiles/default-stable.v1.json
````

Replace v1.0.0 with the tag you want to pin to.
  

Why pin: your translator/book pipeline should not change output unless **you** intentionally update the pinned version.

---

## **Translator integration (runtime behavior)**


**Recommended approach:**

1. Fetch the pinned frozen JSON on startup (by tag URL above).
2. Parse JSON and keep it in memory (optionally cache to disk/redis).
3. Resolve aliases (e.g. ali → ale) and map word → entries[word].


Do **not** auto-update from main or “latest” without a version bump/tag change.

---

## **Dev setup**

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

---

## **Build (generate dist)**

```
python tools/build_default_stable.py
```

---

## **Books pipeline**

### **1) Convert toki pona text → sitelen emoji tokens**


Input: .txt or .md with toki pona text

Output: a text file where tokens are mapped to emoji (spaces preserved, newlines preserved)

```
python3 -m tools.convert_tp_text --in book_tp.txt --out book_se.txt
```

Options:

- --no-dot to keep . as text (otherwise mapped to _punct_period)
- --no-colon to keep : as text (otherwise mapped to _punct_colon)


### **2) Visual-stable build (HTML + optional PDF)**

This renders emoji as **Twemoji PNG** so visuals are consistent across Kindle/apps/devices.

Fetch Twemoji assets (once per machine/version):

```
python3 -m tools.fetch_twemoji_assets
```

Build visual HTML (copies only used PNGs into the output folder):

```
./scripts/visual_build.sh book_se.txt out/visual
open out/visual/index.html
```

Optional PDF (requires Google Chrome installed):

```
./scripts/visual_build.sh --fetch --pdf book_se.txt out/visual
open out/visual/book.pdf
```

---

## **Updating upstream safely (without breaking published output)**

1. Regenerate dist/ from upstream:

```
python tools/build_default_stable.py
```

2. Compare frozen vs new generated:

```
python3 -m tools.diff_profiles
```

3. If you intentionally want a new frozen version, create a new file under profiles/
    
    (e.g. profiles/default-stable.v2.json), update tests if needed, then tag a new release.
    

---

## **Releasing a pinned version**

```
git tag -a v1.0.0 -m "Pinned frozen profile"
git push origin v1.0.0
```

Then consumers can pin to:

```
https://raw.githubusercontent.com/markoblogo/sitelen-emoji-truth/v1.0.0/profiles/default-stable.v1.json
```

---

## License & attribution

- Repository code and profiles: MIT License (see `LICENSE`).
- Twemoji graphics are **not included** in this repository and are fetched separately.
  If you publish outputs that embed Twemoji PNG, include attribution (Twemoji is CC BY 4.0).
