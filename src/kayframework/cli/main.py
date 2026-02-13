import argparse
import shutil
import sys
from pathlib import Path

from kayframework import __version__
from kayframework.core.scaffold import create_project
from kayframework.modules.scaffold import create_module
from kayframework.utils.process import run_command


def _cmd_new_app(args: argparse.Namespace) -> int:
    code, message = create_project(args.name, Path(args.dir))
    stream = sys.stderr if code else sys.stdout
    print(message, file=stream)
    return code


def _cmd_new_module(args: argparse.Namespace) -> int:
    code, message = create_module(args.name, Path(args.app_dir))
    stream = sys.stderr if code else sys.stdout
    print(message, file=stream)
    return code


def _cmd_run(args: argparse.Namespace) -> int:
    cmd = ["uvicorn", args.app, "--host", args.host, "--port", str(args.port)]
    if args.reload:
        cmd.append("--reload")
    return run_command(cmd)


def _cmd_test(args: argparse.Namespace) -> int:
    return run_command(["pytest", args.path])


def _cmd_lint(args: argparse.Namespace) -> int:
    first = run_command(["ruff", "check", args.path])
    second = run_command(["black", "--check", args.path])
    return first or second


def _cmd_format(args: argparse.Namespace) -> int:
    return run_command(["black", args.path])


def _cmd_typecheck(args: argparse.Namespace) -> int:
    return run_command(["mypy", args.path])


def _cmd_build(_: argparse.Namespace) -> int:
    return run_command([sys.executable, "-m", "build"])


def _cmd_clean(args: argparse.Namespace) -> int:
    target = Path(args.dir)
    clean_dirs = ["build", "dist", ".mypy_cache", ".ruff_cache", ".pytest_cache"]
    for name in clean_dirs:
        path = target / name
        if path.exists() and path.is_dir():
            shutil.rmtree(path, ignore_errors=True)

    for cache_dir in target.rglob("__pycache__"):
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir, ignore_errors=True)

    print(f"Cleaned artifacts in: {target}")
    return 0


def _cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.dir)
    env_example = target / ".env.example"
    env_file = target / ".env"

    if not env_example.exists():
        env_example.write_text("ENV=local\nLOG_LEVEL=INFO\nMODULES=\n", encoding="utf-8")
    if not env_file.exists():
        env_file.write_text("ENV=local\nLOG_LEVEL=INFO\nMODULES=\n", encoding="utf-8")

    print(f"Initialized env files in: {target}")
    return 0


def _cmd_doctor(args: argparse.Namespace) -> int:
    target = Path(args.dir)
    ok = True

    binaries = ["python", "uvicorn", "pytest", "ruff", "black", "mypy"]
    for binary in binaries:
        if shutil.which(binary) is None:
            print(f"missing binary: {binary}")
            ok = False

    is_generated_app = (target / "app" / "main.py").exists()
    if is_generated_app:
        required_paths = ["pyproject.toml", "app/main.py", ".env.example"]
    else:
        required_paths = ["pyproject.toml", "src/kayframework", "README.md"]
    for rel_path in required_paths:
        if not (target / rel_path).exists():
            print(f"missing file: {rel_path}")
            ok = False

    if ok:
        print("doctor: ok")
        return 0
    return 1


def _cmd_version(_: argparse.Namespace) -> int:
    print(__version__)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kay", description="KAYFRAMEWORK CLI")
    sub = parser.add_subparsers(dest="command")

    new_parser = sub.add_parser("new", help="Create scaffolds")
    new_sub = new_parser.add_subparsers(dest="new_command")

    new_app = new_sub.add_parser("app", help="Create a new project from the framework scaffold")
    new_app.add_argument("name", help="Project directory name")
    new_app.add_argument("--dir", default=".", help="Parent directory (default: current)")
    new_app.set_defaults(handler=_cmd_new_app)

    new_module = new_sub.add_parser("module", help="Create a module inside an existing app")
    new_module.add_argument("name", help="Module name (Python identifier)")
    new_module.add_argument("--app-dir", default="app", help="App directory (default: app)")
    new_module.set_defaults(handler=_cmd_new_module)

    run = sub.add_parser("run", help="Run app with uvicorn")
    run.add_argument("--app", default="app.main:app", help="ASGI app path")
    run.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    run.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    run.add_argument("--no-reload", dest="reload", action="store_false", help="Disable reload")
    run.set_defaults(reload=True, handler=_cmd_run)

    test = sub.add_parser("test", help="Run pytest")
    test.add_argument("path", nargs="?", default="tests", help="Test path")
    test.set_defaults(handler=_cmd_test)

    lint = sub.add_parser("lint", help="Run ruff + black --check")
    lint.add_argument("path", nargs="?", default=".", help="Target path")
    lint.set_defaults(handler=_cmd_lint)

    fmt = sub.add_parser("format", help="Format code with black")
    fmt.add_argument("path", nargs="?", default=".", help="Target path")
    fmt.set_defaults(handler=_cmd_format)

    tc = sub.add_parser("typecheck", help="Run mypy")
    tc.add_argument("path", nargs="?", default="src", help="Target path")
    tc.set_defaults(handler=_cmd_typecheck)

    build = sub.add_parser("build", help="Build package artifacts")
    build.set_defaults(handler=_cmd_build)

    clean = sub.add_parser("clean", help="Remove build/test cache artifacts")
    clean.add_argument("--dir", default=".", help="Target directory")
    clean.set_defaults(handler=_cmd_clean)

    init = sub.add_parser("init", help="Create .env and .env.example if missing")
    init.add_argument("--dir", default=".", help="Target directory")
    init.set_defaults(handler=_cmd_init)

    doctor = sub.add_parser("doctor", help="Validate local framework setup")
    doctor.add_argument("--dir", default=".", help="Target directory")
    doctor.set_defaults(handler=_cmd_doctor)

    version = sub.add_parser("version", help="Print CLI version")
    version.set_defaults(handler=_cmd_version)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    handler = getattr(args, "handler", None)

    if handler is None:
        parser.print_help()
        raise SystemExit(2)

    raise SystemExit(handler(args))
