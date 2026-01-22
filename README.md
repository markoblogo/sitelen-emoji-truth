# sitelen-emoji-truth

Canonical frozen mapping for toki pona -> sitelen emoji.

## Dev setup


```
python3 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements-dev.txt

python -m pytest -q
```

## **Build**

```
python tools/build_default_stable.py
```

## Visual build (for books / Kindle)

1) Fetch Twemoji assets (once):
```bash
python3 -m tools.fetch_twemoji_assets
````

2. Build visual HTML (and copy only used PNGs):

```
./scripts/visual_build.sh input.txt out/visual
open out/visual/index.html
```

Optional PDF:

```
./scripts/visual_build.sh --fetch --pdf input.txt out/visual
```

Twemoji graphics are CC BY 4.0 — include attribution in published works.
