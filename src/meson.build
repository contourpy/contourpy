message('----- CPP -----')
cpp = meson.get_compiler('cpp')
message(cpp.get_id())
message(cpp.version())
message(meson.project_source_root())
message(py3.get_install_dir())
message(py3.language_version())
message('---------------')

incdir_pybind11 = run_command(py3,
  ['-c', 'import pybind11; print(pybind11.get_include())'],
  check: true
).stdout().strip()

inc_pybind11 = include_directories(incdir_pybind11)

pybind11_config = find_program('pybind11-config')
pybind11_config_ret = run_command(pybind11_config, ['--includes'], check: true)
pybind11_dep = declare_dependency(
  include_directories: [pybind11_config_ret.stdout().split('-I')[-1].strip()],
)

cpp_args = [
  '-DCONTOURPY_DEBUG=0',
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
