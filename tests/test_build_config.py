from __future__ import annotations

import pytest

from contourpy.util import build_config


@pytest.fixture
def all_keys() -> list[str]:
    return [
        "b_ndebug",
        "b_vscrt",
        "build_cpu_endian",
        "build_cpu_family",
        "build_cpu_system",
        "build_cpu",
        "build_dir",
        "build_options",
        "buildtype",
        "compile_command",
        "compiler_name",
        "compiler_version",
        "contourpy_version",
        "cpp_std",
        "cross_build",
        "debug",
        "host_cpu_endian",
        "host_cpu_family",
        "host_cpu_system",
        "host_cpu",
        "linker_id",
        "meson_backend",
        "meson_version",
        "mesonpy_version",
        "optimization",
        "pybind11_version",
        "python_install_dir",
        "python_path",
        "python_version",
        "source_dir",
        "vsenv",
    ]


def test_build_config(all_keys: list[str]) -> None:
    config = build_config()

    for key in all_keys:
        # key exists and its value is a non-empty string
        value = config.pop(key)
        assert isinstance(value, str) and len(value) > 0

    # assert no keys left
    assert len(config) == 0
