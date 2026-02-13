# Architecture

KAYFRAMEWORK is built as a scaffold-first framework:

1. `src/kayframework` provides the framework package and CLI.
2. `src/kayframework/project_template` stores the project scaffold copied by `kay new app`.
3. Generated projects run independently from the framework package.

## Runtime Model

- The framework package itself focuses on developer workflow (CLI, scaffolding, quality commands).
- The generated project owns API runtime concerns (routing, auth, DB, templates).

## Core Components

- `kayframework.core.scaffold`: project generation primitives.
- `kayframework.modules.scaffold`: module scaffold generation.
- `kayframework.cli.main`: command parser and command dispatch.
- `kayframework.utils.process`: subprocess execution helper.

## Design Constraints

- Keep scaffold assets out of import paths.
- Keep CLI deterministic with explicit exit codes.
- Keep generated projects editable and framework-agnostic after generation.
