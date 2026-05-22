# Release Notes

## Upgrading

```bash
pip install -U toapi
```

Or with uv:

```bash
uv add toapi@latest
```

## Changelog

### 2.2.0 (2026-05-22)

- Switched packaging from Poetry to [uv](https://github.com/astral-sh/uv)
  (PEP 621 + hatchling).
- Raised the minimum Python version to 3.10.
- Replaced the abandoned `cchardet` dependency with `charset-normalizer`.
- Bumped Flask 2 → 3, plus `requests`, `click`, `colorama`, and `cssselect`
  to current majors.
- Replaced black + isort + flake8 + `pytest-pep8` with a single
  [ruff](https://github.com/astral-sh/ruff) toolchain.
- Replaced Travis CI with GitHub Actions on a 3.10 / 3.11 / 3.12 matrix.
- Replaced the `ItemType` metaclass with `__init_subclass__` — same
  behavior, half the code.
- `__version__` is now sourced from package metadata, fixing an import
  error in `toapi.cli`.

### 2.1.x

- Maintenance releases on the old Poetry / Python 3.8 stack.

### 1.0.0 (2017-12-26)

- Initial release.
