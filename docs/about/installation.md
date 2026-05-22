# Installation

## Requirements

- Python 3.10 or newer
- pip (or [uv](https://github.com/astral-sh/uv),
  [pipx](https://pipx.pypa.io/), [Poetry](https://python-poetry.org/) — any
  modern installer)

Check your Python version:

```bash
python --version
```

## Install from PyPI

```bash
pip install toapi
```

Or with uv:

```bash
uv add toapi
```

## Verify

```bash
python -c "import toapi; print(toapi.__version__)"
```

## Upgrade

```bash
pip install -U toapi
```

## Install from source

```bash
git clone https://github.com/elliotgao2/toapi.git
cd toapi
uv sync
```

This drops you in a working development environment with all dependencies
and dev tools.
