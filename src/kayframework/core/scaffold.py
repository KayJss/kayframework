import re
import shutil
from importlib import resources
from pathlib import Path


_PROJECT_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def _normalize_package_name(project_name: str) -> str:
    return project_name.strip().lower().replace("_", "-").replace(" ", "-")


def _validate_project_name(project_name: str) -> str | None:
    value = project_name.strip()
    if not value:
        return "project name cannot be empty"
    if value in {".", ".."} or not _PROJECT_NAME_RE.fullmatch(value):
        return "project name may contain only letters, numbers, dots, underscores and hyphens"
    return None


def copy_project_template(target_dir: Path) -> None:
    template_root = resources.files("kayframework").joinpath("project_template")
    with resources.as_file(template_root) as source_path:
        for item in source_path.iterdir():
            destination = target_dir / item.name
            if item.is_dir():
                shutil.copytree(item, destination, dirs_exist_ok=False)
            else:
                shutil.copy2(item, destination)


def write_generated_files(project_name: str, target_dir: Path) -> None:
    package_name = _normalize_package_name(project_name)

    (target_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {project_name}",
                "",
                "Generated with KAYFRAMEWORK.",
                "",
                "## Quickstart",
                "```bash",
                "python -m venv .venv",
                "pip install -e .",
                "uvicorn app.main:app --reload",
                "```",
                "",
                "## Plugins",
                "Install built-in extensions with `kay add plugin <name>`.",
                "Example: `kay add plugin cors`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (target_dir / "pyproject.toml").write_text(
        "\n".join(
            [
                "[project]",
                f'name = "{package_name}"',
                'version = "0.1.0"',
                'requires-python = ">=3.10"',
                "dependencies = [",
                '  "fastapi",',
                '  "uvicorn[standard]",',
                '  "pydantic-settings",',
                "]",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (target_dir / ".env.example").write_text(
        "\n".join(
            [
                "ENV=local",
                "LOG_LEVEL=INFO",
                "MODULES=",
                "PLUGINS=",
                "CORS_ORIGINS=http://localhost:3000,http://localhost:5173",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (target_dir / ".gitignore").write_text(
        "\n".join(
            [
                ".venv/",
                "__pycache__/",
                "*.pyc",
                ".pytest_cache/",
                ".mypy_cache/",
                ".ruff_cache/",
                ".env",
                "*.db",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def create_project(project_name: str, base_dir: Path) -> tuple[int, str]:
    validation_error = _validate_project_name(project_name)
    if validation_error:
        return 2, validation_error

    clean_name = project_name.strip()
    target_dir = base_dir / clean_name
    if target_dir.exists():
        return 2, f"target directory already exists: {target_dir}"

    target_dir.mkdir(parents=True, exist_ok=False)
    try:
        copy_project_template(target_dir)
        write_generated_files(clean_name, target_dir)
    except Exception:
        shutil.rmtree(target_dir, ignore_errors=True)
        raise

    return 0, f"Project created: {target_dir}"
