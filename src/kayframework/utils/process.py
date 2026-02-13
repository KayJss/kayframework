import subprocess


def run_command(cmd: list[str]) -> int:
    result = subprocess.run(cmd, check=False)
    return result.returncode
