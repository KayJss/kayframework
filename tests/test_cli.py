from pathlib import Path

from kayframework.core.scaffold import create_project
from kayframework.modules.scaffold import create_module


def test_create_project(tmp_path: Path) -> None:
    result, _ = create_project("demo", tmp_path)
    assert result == 0

    target = tmp_path / "demo"
    assert (target / "app" / "main.py").exists()
    assert (target / "pyproject.toml").exists()
    assert (target / ".env.example").exists()


def test_create_module(tmp_path: Path) -> None:
    app_dir = tmp_path / "app"
    (app_dir / "modules").mkdir(parents=True)

    result, _ = create_module("billing", app_dir)
    assert result == 0

    module_dir = app_dir / "modules" / "billing"
    assert (module_dir / "routes.py").exists()
    assert (module_dir / "schema.py").exists()
