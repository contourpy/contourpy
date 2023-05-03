cpp_args = [
  '-DCONTOURPY_VERSION=' + version
]

ext = py3.extension_module(
  '_contourpy',
  [
    'chunk_local.cpp',
    'converter.cpp',
    'fill_type.cpp',
    'line_type.cpp',
    'mpl2005_original.cpp',
    'mpl2005.cpp',
    'mpl2014.cpp',
    'outer_or_hole.cpp',
    'serial.cpp',
    'threaded.cpp',
    'util.cpp',
    'wrap.cpp',
    'z_interp.cpp',
  ],
  cpp_args: cpp_args,
  dependencies: [pybind11_dep],
  gnu_symbol_visibility: 'hidden',
  install: true,
  subdir: 'contourpy',
)
