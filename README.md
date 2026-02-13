# KAYFRAMEWORK

A scaffold-first FastAPI micro-framework for teams that want a repeatable starting architecture, a consistent CLI workflow, and full ownership of generated application code.

PyPI: `https://pypi.org/project/kayframework/`

## Quickstart

```bash
pip install kayframework
kay new app myservice
cd myservice
pip install -e .
uvicorn app.main:app --reload
```

## Why This Framework Exists

KAYFRAMEWORK exists to solve a practical gap:

- FastAPI gives primitives, not a standardized project system.
- Teams often rebuild the same app skeleton and CLI scripts repeatedly.
- Starter templates become unmaintained, inconsistent, or hard to scale across services.

KAYFRAMEWORK provides a stable scaffold workflow while keeping generated projects decoupled from framework internals.

## Who It Is For / Not For

For:

- Teams building multiple FastAPI services with a shared baseline architecture.
- Developers who want opinionated scaffolding but flexible implementation.
- Projects that value CLI-driven consistency (`new`, `module`, `lint`, `doctor`, `build`).

Not for:

- Teams needing a batteries-included monolith like Django admin + ORM conventions.
- Projects expecting runtime plugin magic managed by the framework package itself.
- Users who only need a single minimal script-level API app.

## Key Features

- `src`-layout packaging with clean import boundaries.
- Scaffold template separated from runtime package internals.
- CLI for project/module generation and developer workflow commands.
- Module-oriented generated app structure (`app/modules/...`).
- GitHub-ready repo baseline (CI, contribution docs, issue/PR templates).

## Architecture Overview

```text
src/
  kayframework/
    cli/
      main.py
    core/
      scaffold.py
    modules/
      scaffold.py
    utils/
      process.py
    project_template/
      app/
        ... generated application scaffold ...

docs/
examples/
tests/
```

Design model:

- `kayframework` package: tooling, scaffolding, CLI.
- `project_template`: copied into new projects by `kay new app`.
- Generated apps: independent codebases you fully own and modify.

## CLI

```bash
kay new app <name> [--dir .]
kay new module <name> [--app-dir app]
kay run [--app app.main:app] [--host 127.0.0.1] [--port 8000] [--no-reload]
kay test [path]
kay lint [path]
kay format [path]
kay typecheck [path]
kay build
kay clean [--dir .]
kay init [--dir .]
kay doctor [--dir .]
kay version
```

CLI conventions:

- Non-zero exit codes on failure.
- Deterministic scaffold generation.
- Commands target local project directories explicitly.

## Module System

Generated apps include module loading via `MODULES` in `.env`.

Example:

```env
MODULES=billing,notifications
```

Each module lives under `app/modules/<module_name>/` and exposes `router` in `routes.py`.

## Comparison

| Capability | KAYFRAMEWORK | FastAPI | Flask | Django |
|---|---|---|---|---|
| Opinionated scaffold generation | Yes | No | No | Yes |
| Lightweight micro-framework runtime | Yes | Yes | Yes | No |
| Built-in monolith features (admin, ORM conventions) | No | No | No | Yes |
| CLI-first project/module generation | Yes | Partial | Partial | Yes |
| Generated code ownership model | Full | N/A | N/A | Partial |

## Installation

Framework package:

```bash
pip install kayframework
```

Development setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Development Workflow

```bash
kay lint
kay typecheck
kay test
kay build
```

CI mirrors the same checks in `.github/workflows/ci.yml`.

## Security Notes

For generated projects:

- Replace `SECRET_KEY` before deployment.
- Use `ENV=prod` and `COOKIE_SECURE=true` under HTTPS.
- Do not commit `.env`.
- Add rate limiting, audit logging, and deployment hardening based on your risk model.

## License

See `LICENSE`.
