# Publishing

Package publishing is prepared but disabled by default.

## Current package names

- npm: `sitelen-emoji`
- PyPI: `sitelen-emoji`

Both names were unregistered when checked on 2026-06-08.

## GitHub settings

- Repository variable: `ENABLE_PACKAGE_PUBLISH=false`
- PyPI environment: `pypi`

Keep publishing disabled until both registries have trusted publishers configured.

## npm trusted publisher

Create the package on npm and configure a trusted publisher:

- Repository: `markoblogo/sitelen-emoji-truth`
- Workflow: `publish-npm.yml`
- Allowed action: `npm publish`

Workflow file: `.github/workflows/publish-npm.yml`

Docs: https://docs.npmjs.com/trusted-publishers/

## PyPI trusted publisher

Create the project on PyPI and configure a GitHub trusted publisher:

- Owner: `markoblogo`
- Repository: `sitelen-emoji-truth`
- Workflow name: `publish-pypi.yml`
- Environment name: `pypi`

Workflow file: `.github/workflows/publish-pypi.yml`

Docs: https://docs.pypi.org/trusted-publishers/

## Enable publishing

After trusted publishers are configured:

```bash
gh variable set ENABLE_PACKAGE_PUBLISH --repo markoblogo/sitelen-emoji-truth --body true
```

Publishing runs on GitHub Release publish events and can also be started manually with `workflow_dispatch`.
