import shutil
from importlib import resources
from pathlib import Path


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
    package_name = project_name.lower().replace(" ", "-")

    (target_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {project_name}",
                "",
                "Generated with KAYFRAMEWORK.",
                "",
                "## Quickstart",
                "```bash",
                "pip install -e .",
                "uvicorn app.main:app --reload",
                "```",
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
        "\n".join(["ENV=local", "LOG_LEVEL=INFO", "MODULES="]) + "\n",
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
    target_dir = base_dir / project_name
    if target_dir.exists():
        return 2, f"target directory already exists: {target_dir}"

    target_dir.mkdir(parents=True, exist_ok=False)
    copy_project_template(target_dir)
    write_generated_files(project_name, target_dir)
    return 0, f"Project created: {target_dir}"
