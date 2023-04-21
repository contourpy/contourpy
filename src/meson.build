cpp_args = [
  # CONTOURPY_DEBUG derived from NDEBUG in wrap.cpp
  '-DCONTOURPY_CXX11=0',  # only for information purposes.
  '-DCONTOURPY_VERSION=@0@'.format(version),
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
  cpp_args: [cpp_args],
  #link_args: version_link_args,
  dependencies : [pybind11_dep],
  gnu_symbol_visibility: 'hidden',
  install: true,
  #override_options: [],   # Can override options from project
  subdir: 'contourpy',
)
