from pathlib import Path


def create_module(module_name: str, app_dir: Path) -> tuple[int, str]:
    if not module_name.isidentifier():
        return 2, "module name must be a valid Python identifier"

    modules_dir = app_dir / "modules"
    module_dir = modules_dir / module_name
    if module_dir.exists():
        return 2, f"module already exists: {module_dir}"

    module_dir.mkdir(parents=True, exist_ok=False)
    files = {
        "__init__.py": "",
        "routes.py": (
            "from fastapi import APIRouter\n\n"
            "router = APIRouter()\n\n\n"
            "@router.get(\"/\")\n"
            f"def {module_name}_root():\n"
            f"    return {{\"module\": \"{module_name}\", \"status\": \"ok\"}}\n"
        ),
        "schema.py": "# Add module schemas\n",
        "service.py": "# Add module business logic\n",
        "models.py": "# Add module models\n",
    }

    for filename, content in files.items():
        (module_dir / filename).write_text(content, encoding="utf-8")

    return 0, f"Module created: {module_dir}"
