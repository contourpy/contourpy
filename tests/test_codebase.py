import contourpy
import pytest
from subprocess import run


def test_cppcheck():
    # Skip test if cppcheck is not installed.
    cmd = ["cppcheck", "--version"]
    try:
        proc = run(cmd)
    except FileNotFoundError:
        pytest.skip()

    # Note excluding mpl2005 code.
    cmd = ["cppcheck", "--quiet", "--enable=all", "--error-exitcode=1", "src", "-isrc/mpl2005.c",
           "--suppress=missingIncludeSystem", "--inline-suppr"]
    proc = run(cmd, capture_output=True)
    assert proc.returncode == 0, f"cppcheck issues:\n{proc.stderr.decode('utf-8')}"


def test_flake8():
    cmd = ["flake8"]
    proc = run(cmd, capture_output=True)
    assert proc.returncode == 0, f"Flake8 issues:\n{proc.stdout.decode('utf-8')}"


def test_version():
    version_python = contourpy.__version__
    version_cxx = contourpy._contourpy.__version__
    assert version_python == version_cxx
