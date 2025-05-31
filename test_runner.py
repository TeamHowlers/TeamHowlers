# test_runner.py
import subprocess, importlib.util, sys, shutil

def run_pytest():
    """Run pytest with coverage; return (ok: bool, coverage: float, output: str)."""
    # 1. Make sure pytest is available
    if importlib.util.find_spec("pytest") is None:
        return False, 0.0, "pytest not installed. Run: pip install pytest pytest-cov."

    cmd = ["pytest", "--cov=.", "--cov-report=term-missing", "-q"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    ok = result.returncode == 0

    # Parse coverage line, e.g. "TOTAL ... 85%"
    cov = 0.0
    for line in result.stdout.splitlines():
        if "TOTAL" in line and "%" in line:
            cov = float(line.strip().split()[-1].strip("%"))
            break

    return ok, cov, result.stdout + result.stderr


def run_jest_tests():
    """Run Jest only if `npx` and `jest` exist; otherwise skip."""
    if shutil.which("npx") is None:
        return True, 0.0, "Node/NPM not installed – skipping Jest."

    # (optional extra check that a __tests__ folder exists)
    # ...

    result = subprocess.run(
        ["npx", "jest", "--coverage"],
        capture_output=True,
        text=True,
    )
    ok = result.returncode == 0
    cov = 0.0  # parse from result.stdout if you really need it
    return ok, cov, result.stdout + result.stderr
