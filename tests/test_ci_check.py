import os
import shutil
import subprocess

import pytest


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash is required for this test")
def test_ci_check_with_spaces_in_path():
    env = {
        **os.environ,
        "PHANTOM_PATHS": "tests/fixtures/space path",
    }
    result = subprocess.run(
        ["bash", "scripts/ci_check.sh"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "checked 1 file(s)" in result.stdout
