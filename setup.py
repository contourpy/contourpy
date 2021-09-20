import os
import re
from setuptools import setup
from pybind11.setup_helpers import build_ext, naive_recompile, ParallelCompile, Pybind11Extension


def get_version():
    # Full compliance with PEP440 is tested in test_codebase.py
    version_filename = "lib/contourpy/_version.py"
    pattern = re.compile(r'__version__\s*=\s*"([\d\w\.]+)"')

    with open(version_filename) as f:
        for line in f:
            match = pattern.match(line)
            if match:
                return match.group(1)

    raise RuntimeError(f"Unable to read version from {version_filename}")


__version__ = get_version()

# Set environment variable CONTOURPY_DEBUG=1 if you want to enable asserts in C++ code.
CONTOURPY_DEBUG = int(os.environ.get("CONTOURPY_DEBUG", 0))

# Set environment variable CONTOURPY_CXX11=1 if you want to use C++11 standard rather than the
# highest supported standard.
CONTOURPY_CXX11 = int(os.environ.get("CONTOURPY_CXX11", 0))


define_macros = [
    ("CONTOURPY_VERSION", __version__),
]
undef_macros = []

if CONTOURPY_DEBUG:
    define_macros.append(("DEBUG", 1))
    undef_macros.append("NDEBUG")

if CONTOURPY_CXX11:
    cxx_std = 11
    cmdclass = {}
else:
    cxx_std = 0
    cmdclass = {"build_ext": build_ext}

ParallelCompile(default=0, needs_recompile=naive_recompile).install()

_contourpy = Pybind11Extension(
    "contourpy._contourpy",
    sources=[
        "src/chunk_local.cpp",
        "src/converter.cpp",
        "src/fill_type.cpp",
        "src/line_type.cpp",
        "src/mpl2005_original.cpp",
        "src/mpl2005.cpp",
        "src/mpl2014.cpp",
        "src/outer_or_hole.cpp",
        "src/serial.cpp",
        "src/threaded.cpp",
        "src/util.cpp",
        "src/wrap.cpp",
        "src/z_interp.cpp",
    ],
    cxx_std=cxx_std,
    define_macros=define_macros + [
        ("CONTOURPY_DEBUG", CONTOURPY_DEBUG),
        ("CONTOURPY_CXX11", CONTOURPY_CXX11),
    ],
    undef_macros=undef_macros,
)

setup(
    version=__version__,
    ext_modules=[_contourpy],
    cmdclass=cmdclass,
)
