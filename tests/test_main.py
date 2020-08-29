import os
from pathlib import Path

import pytest
from lintipy import CheckRun

BASE_DIR = Path(os.path.dirname(__file__))


class TestBlackCheckRun:
    @pytest.fixture
    def handler(self):
        return CheckRun("black", "black", "--check", "--diff", "tests")

    def test_run_process(self, handler):
        code, output = handler.run_process(str(BASE_DIR / ".."))
        assert "file would be reformatted" not in output
        assert "Oh no!" not in output
