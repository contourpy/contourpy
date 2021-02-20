from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext


want_debug = False

__version__ = '0.0.1'


sources = [
    'src/mpl2014.cpp',
    'src/wrap.cpp',
]


define_macros = []
undef_macros = []

if want_debug:
    define_macros.append(('DEBUG',1))
    undef_macros.append('NDEBUG')

_contourpy = Pybind11Extension(
    '_contourpy',
    sources=sources,
    define_macros=define_macros,
    undef_macros=undef_macros,
)


setup(
    name='contourpy',
    version=__version__,
    description='2D contouring',
    long_description='Calculating contours of 2D quadrilateral grids',
    author='Ian Thomas',
    author_email='ianthomas23@gmail.com',
    license='BSD',
    packages=['contourpy'],
    ext_modules=[_contourpy],
    cmdclass={'build_ext': build_ext},
    zip_safe=False
)
