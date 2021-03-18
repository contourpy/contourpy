from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext


# Set want_debug to True if want to enable asserts in C++ code.
want_debug = False

want_mpl2005 = True


__version__ = '0.0.1'


define_macros = []
undef_macros = []

if want_debug:
    define_macros.append(('DEBUG',1))
    undef_macros.append('NDEBUG')

_contourpy = Pybind11Extension(
    'contourpy._contourpy',
    sources=[
        'src/chunk_local.cpp',
        'src/fill_type.cpp',
        'src/line_type.cpp',
        'src/mpl2014.cpp',
        'src/outer_or_hole.cpp',
        'src/serial.cpp',
        'src/wrap.cpp',
    ],
    define_macros=define_macros,
    undef_macros=undef_macros,
)

ext_modules=[_contourpy]


if want_mpl2005:
    # Using original C code and Python/C API wrapper.
    # numpy is in pyproject.toml rather than requirements/install.txt for this.
    import numpy as np
    from setuptools import Extension

    _mpl2005 = Extension(
        'contourpy._mpl2005',
        sources=['src/mpl2005.c'],
        undef_macros=undef_macros,
        include_dirs=[np.get_include()],
        define_macros=define_macros + [
            ('PY_ARRAY_UNIQUE_SYMBOL', 'CNTR_ARRAY_API'),
            ('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),
            ('__STDC_FORMAT_MACROS', 1),
        ],
    )
    ext_modules.append(_mpl2005)



def read_requirements(filename):
    return open(filename).read().strip().split('\n')


setup(
    name='contourpy',
    version=__version__,
    description='2D contouring',
    long_description='Calculating contours of 2D quadrilateral grids',
    author='Ian Thomas',
    author_email='ianthomas23@gmail.com',
    license='BSD',
    package_dir={'': 'lib'},
    packages=['contourpy'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=read_requirements('requirements/install.txt'),
)
