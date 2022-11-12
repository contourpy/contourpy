project(
  'contourpy',
  'cpp',
  default_options: [
    'b_ndebug=true',   # true disables asserts, false keeps them.
    'buildtype=debugoptimized',
    'cpp_std=c++11',   # none, c++14, c++17 are other options.
    'werror=true',
  ],
  license: 'BSD-3-Clause',
  #meson_version: '>= 0.63.0',
  version: '1.0.7.dev1',
)

# Check meson project version is the same as in _version.py
fs = import('fs')
version = fs.read('lib/contourpy/_version.py').strip().split(' ').get(-1).substring(1, -1)
if meson.project_version() != version
  error('ContourPy version mismatch: "@0@" != "@1@"'.format(meson.project_version(), version))
endif

py_mod = import('python')
py3 = py_mod.find_installation()

message('----- INFO -----')
message(meson.backend())
message(meson.version())
cpp = meson.get_compiler('cpp')
message(cpp.get_id())
message(cpp.version())
message(host_machine.cpu())
message(host_machine.cpu_family())
message(host_machine.system())
message('----------------')

subdir('lib/contourpy')
subdir('src')
