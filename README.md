# KAYFRAMEWORK

A scaffold-first FastAPI micro-framework for teams that want a repeatable starting architecture, a consistent CLI workflow, installable project extensions, and full ownership of generated application code.

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

## Key Features

- `src`-layout packaging with clean import boundaries.
- Scaffold template separated from runtime package internals.
- CLI for project/module generation and developer workflow commands.
- Module-oriented generated app structure (`app/modules/...`).
- Installable plugin system for reusable project extensions.
- GitHub-ready repo baseline with tests and project documentation.

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
    plugins/
      scaffold.py
    utils/
      process.py
    project_template/
      app/
        core/plugins.py
        ... generated application scaffold ...

docs/
examples/
tests/
```

Design model:

- `kayframework` package: tooling, scaffolding, CLI and built-in plugin installers.
- `project_template`: copied into new projects by `kay new app`.
- Generated apps: independent codebases you fully own and modify.

## CLI

```bash
kay new app <name> [--dir .]
kay new module <name> [--app-dir app]
kay add plugin <name> [--app-dir app]
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

## Plugin System

Generated applications load plugins listed in the `PLUGINS` environment variable. Plugins live inside the generated project, so application code remains under your control.

Install the built-in CORS plugin:

```bash
kay add plugin cors
```

This creates:

```text
app/plugins/__init__.py
app/plugins/cors.py
```

and updates the project environment configuration:

```env
PLUGINS=cors
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

At runtime, KAYFRAMEWORK imports each configured plugin and calls:

```python
register(app, settings)
```

That small contract makes the system easy to extend with future plugins such as rate limiting, structured logging, authentication helpers or observability integrations.

## Module System

Generated apps include module loading via `MODULES` in `.env`.

Example:

```env
MODULES=billing,notifications
```

Each module lives under `app/modules/<module_name>/` and exposes `router` in `routes.py`.

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

## Security Notes

For generated projects:

- Replace `SECRET_KEY` before deployment.
- Use `ENV=prod` and `COOKIE_SECURE=true` under HTTPS.
- Do not commit `.env`.
- Keep CORS origins explicit in production instead of allowing arbitrary domains.
- Add rate limiting, audit logging, and deployment hardening based on your risk model.

## License

See `LICENSE`.
