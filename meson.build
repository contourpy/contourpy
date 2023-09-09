project(
  'contourpy',
  'cpp',
  default_options: [
    # meson-python options are set in pyproject.toml
    'cpp_std=c++17',
    'werror=true',
  ],
  license: 'BSD-3-Clause',
  meson_version: '>= 1.2.0',
  version: '1.1.1rc1',
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

subdir('lib/contourpy')
subdir('src')
