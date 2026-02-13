# Contributing

## Scope

Contributions are welcome for:

- CLI reliability improvements
- Scaffold quality improvements
- Documentation and developer workflow
- Tests and CI hardening

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Local Quality Checks

```bash
kay lint
kay typecheck
kay test
```

## Pull Request Rules

- Keep changes focused and atomic.
- Include tests for behavior changes.
- Update docs for user-facing changes.
- Avoid breaking CLI contracts without migration notes.

## Commit Guidance

Prefer clear commit subjects:

- `cli: add <feature>`
- `scaffold: fix <behavior>`
- `docs: update <section>`
- `ci: adjust <pipeline>`
