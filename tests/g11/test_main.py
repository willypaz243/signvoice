"""Tests for the g11 demo command (offline, one command)."""

import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent


def test_demo_command_serves_the_page_offline():
    """The demo command must serve the Gradio page with one command.

    Manual test: starts the demo as a subprocess and checks that the
    page is reachable; no internet is needed, all models are local.
    """
    proc = subprocess.Popen([sys.executable, "-m", "g11", "demo"], cwd=ROOT)
    try:
        page = None
        deadline = time.time() + 90
        while time.time() < deadline:
            try:
                page = urllib.request.urlopen("http://127.0.0.1:7860/").read()
                break
            except OSError:
                time.sleep(1)
        if page is None:
            pytest.fail("demo did not start in 90s")
        assert b"SignVoice" in page
    finally:
        proc.terminate()
