"""Run the intentional type-error example and verify mypy catches all mistakes."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "examples" / "intentional_type_errors.py"
result = subprocess.run(
    [sys.executable, "-m", "mypy", str(TARGET)],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
output = result.stdout + result.stderr
(ROOT / "artifacts").mkdir(exist_ok=True)
(ROOT / "artifacts" / "mypy_intentional_errors.txt").write_text(output, encoding="utf-8")
expected = ["Incompatible types", "Argument 2"]
if result.returncode == 0:
    print("mypy unexpectedly accepted the intentional errors")
    raise SystemExit(1)
if "error:" not in output:
    print(output)
    raise SystemExit(1)
print(output, end="")
print("mypy detected the intentional type errors as expected")
