project(
  'contourpy',
  'cpp',
  default_options: [
    # meson-python options are set in pyproject.toml
    'cpp_std=c++17',
    'werror=true',
  ],
  license: 'BSD-3-Clause',
  meson_version: '>= 1.1.0',
  version: '1.0.8.dev1',
)

# Check meson project version is the same as in _version.py
fs = import('fs')
version = fs.read('lib/contourpy/_version.py').strip().split(' ').get(-1).substring(1, -1)
if meson.project_version() != version
  error('ContourPy version mismatch: "@0@" != "@1@"'.format(meson.project_version(), version))
endif

py_mod = import('python')
py3 = py_mod.find_installation(pure: false)

pybind11_dep = dependency('pybind11')

message('----- INFO -----')
message(meson.backend())
message(meson.version())
cpp = meson.get_compiler('cpp')
message(cpp.get_id())
message(cpp.version())
message(cpp.get_linker_id())
message(cpp.cmd_array())
message(host_machine.cpu())
message(host_machine.cpu_family())
message(host_machine.system())
message(meson.project_source_root())
message(py3.get_install_dir())
message(py3.language_version())
message('----------------')
message(pybind11_dep.version())
message(pybind11_dep.type_name())
message('----------------')

subdir('lib/contourpy')
subdir('src')
