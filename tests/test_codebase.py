import re
from subprocess import run

import pytest

import contourpy


# From PEP440 appendix.
def version_is_canonical(version):
    return re.match(
        r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?"
        r"(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$", version) is not None


def test_cppcheck():
    # Skip test if cppcheck is not installed.
    cmd = ["cppcheck", "--version"]
    try:
        proc = run(cmd)
    except FileNotFoundError:
        pytest.skip()

    # Note excluding mpl2005 code.
    cmd = [
        "cppcheck", "--quiet", "--enable=all", "--error-exitcode=1", "src",
        "-isrc/mpl2005_original.cpp", "--suppress=missingIncludeSystem", "--inline-suppr"]
    proc = run(cmd, capture_output=True)
    assert proc.returncode == 0, f"cppcheck issues:\n{proc.stderr.decode('utf-8')}"


def test_flake8():
    cmd = ["flake8"]
    try:
        proc = run(cmd, capture_output=True)
    except FileNotFoundError:
        pytest.skip()

    assert proc.returncode == 0, f"Flake8 issues:\n{proc.stdout.decode('utf-8')}"


def test_isort():
    cmd = ["isort", ".", "--diff", "--check-only"]
    try:
        proc = run(cmd, capture_output=True)
    except FileNotFoundError:
        pytest.skip()

    assert proc.returncode == 0, f"isort issues:\n{proc.stderr.decode('utf-8')}"


def test_version():
    version_python = contourpy.__version__
    assert version_is_canonical(version_python)
    version_cxx = contourpy._contourpy.__version__
    assert version_python == version_cxx
