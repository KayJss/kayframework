from pathlib import Path

BUILTIN_PLUGINS = {"cors"}


def _append_env_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    found = False
    output: list[str] = []

    for line in lines:
        if line.startswith(f"{key}="):
            found = True
            current = [item.strip() for item in line.split("=", 1)[1].split(",") if item.strip()]
            if value not in current:
                current.append(value)
            output.append(f"{key}={','.join(current)}")
        else:
            output.append(line)

    if not found:
        output.append(f"{key}={value}")

    path.write_text("\n".join(output) + "\n", encoding="utf-8")


def install_plugin(name: str, app_dir: Path) -> tuple[int, str]:
    plugin_name = name.strip().lower().replace("-", "_")
    if plugin_name not in BUILTIN_PLUGINS:
        return 2, f"unknown plugin: {name}. Available: {', '.join(sorted(BUILTIN_PLUGINS))}"

    if not (app_dir / "main.py").exists():
        return 2, f"not a KAYFRAMEWORK app directory: {app_dir}"

    plugins_dir = app_dir / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    init_file = plugins_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")

    target = plugins_dir / f"{plugin_name}.py"
    if target.exists():
        return 2, f"plugin already installed: {plugin_name}"

    if plugin_name == "cors":
        target.write_text(
            "from fastapi import FastAPI\n"
            "from fastapi.middleware.cors import CORSMiddleware\n\n"
            "def register(app: FastAPI, settings) -> None:\n"
            "    origins = [item.strip() for item in settings.CORS_ORIGINS.split(',') if item.strip()]\n"
            "    app.add_middleware(\n"
            "        CORSMiddleware,\n"
            "        allow_origins=origins or ['http://localhost:3000', 'http://localhost:5173'],\n"
            "        allow_credentials=True,\n"
            "        allow_methods=['*'],\n"
            "        allow_headers=['*'],\n"
            "    )\n",
            encoding="utf-8",
        )

    project_root = app_dir.parent
    for env_name in (".env", ".env.example"):
        _append_env_value(project_root / env_name, "PLUGINS", plugin_name)

    return 0, f"Plugin installed: {plugin_name}"
