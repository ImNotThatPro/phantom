import os
import shutil
import subprocess

import pytest


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash is required for this test")
def test_ci_check_with_spaces_in_path():
    env = {
        **os.environ,
        "PHANTOM_PATHS": "tests/fixtures/space path",
        "PYTHONIOENCODING": "utf-8",
        "LC_ALL": "C.UTF-8",
    }
    result = subprocess.run(
        ["bash", "scripts/ci_check.sh"],
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    # Clean UTF-16 null bytes and carriage returns produced by bash on Windows runners
    stdout = result.stdout.replace("\x00", "").replace("\r", "")
    stderr = result.stderr.replace("\x00", "").replace("\r", "")

    assert result.returncode == 0, f"Script failed with stderr:\n{stderr}\nstdout:\n{stdout}"
    assert "checked" in stdout or result.returncode == 0
