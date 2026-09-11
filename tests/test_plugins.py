from pathlib import Path

from kayframework.core.scaffold import create_project
from kayframework.plugins.scaffold import install_plugin


def test_install_cors_plugin(tmp_path: Path) -> None:
    code, _ = create_project("demo", tmp_path)
    assert code == 0

    app_dir = tmp_path / "demo" / "app"
    code, message = install_plugin("cors", app_dir)

    assert code == 0
    assert "cors" in message
    assert (app_dir / "plugins" / "cors.py").exists()
    assert "PLUGINS=cors" in (tmp_path / "demo" / ".env.example").read_text(encoding="utf-8")


def test_reject_unknown_plugin(tmp_path: Path) -> None:
    code, _ = create_project("demo", tmp_path)
    assert code == 0

    code, message = install_plugin("does-not-exist", tmp_path / "demo" / "app")

    assert code == 2
    assert "unknown plugin" in message
