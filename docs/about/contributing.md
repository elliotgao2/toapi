# Contributing

Thanks for your interest in improving `toapi`! Bug reports, feature ideas,
documentation tweaks, and pull requests are all welcome.

## Reporting an issue

Open an issue on [GitHub](https://github.com/elliotgao2/toapi/issues) with:

- What you tried
- What you expected to happen
- What actually happened (including the full error and traceback)
- Your Python version and `toapi` version

## Setting up a development environment

We use [uv](https://github.com/astral-sh/uv) for packaging and
[ruff](https://github.com/astral-sh/ruff) for lint and format.

```bash
git clone https://github.com/elliotgao2/toapi.git
cd toapi
uv sync
```

Install the pre-commit hooks so ruff runs on every commit:

```bash
uv run pre-commit install
```

## Running the checks

```bash
uv run pytest               # tests
uv run ruff check .         # lint
uv run ruff format --check . # format
```

CI runs the same checks on Python 3.10, 3.11, and 3.12.

## Submitting a pull request

1. Fork the repo and create a topic branch.
2. Make your change. Keep diffs focused — one concern per PR.
3. Add or update tests when the behavior changes.
4. Make sure `pytest` and `ruff check` pass locally.
5. Open the PR with a short description of *what* changed and *why*.

For non-trivial changes, please open an issue first so we can discuss the
approach before you spend time on it.
