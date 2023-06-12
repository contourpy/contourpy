python_sources = [
  '__init__.py',
  'bokeh_renderer.py',
  'bokeh_util.py',
  'data.py',
  'mpl_renderer.py',
  'mpl_util.py',
  'renderer.py',
]

py3.install_sources(
  python_sources,
  subdir: 'contourpy/util',
)


# Build config data
conf_data = configuration_data()

# Python settings
conf_data.set('python_version', py3.language_version())
conf_data.set('python_install_dir', py3.get_install_dir().replace('\\', '/'))
conf_data.set('python_path', py3.full_path().replace('\\', '/'))

# package versions
conf_data.set('contourpy_version', meson.project_version())
conf_data.set('meson_version', meson.version())
conf_data.set('mesonpy_version',
  run_command(
    py3,
    ['-c', 'import mesonpy; print(mesonpy.__version__)'],
    check: true
  ).stdout().strip()
)
conf_data.set('pybind11_version', pybind11_dep.version())

# Misc meson settings
conf_data.set('meson_backend', meson.backend())
conf_data.set('build_dir', meson.current_build_dir().replace('\\', '/'))
conf_data.set('source_dir', meson.current_source_dir().replace('\\', '/'))
conf_data.set('cross_build', meson.is_cross_build())

# Build options
conf_data.set('build_options', meson.build_options().replace('\\', '/'))
options = [
  'b_ndebug',
  'b_vscrt',
  'buildtype',
  'cpp_std',
  'debug',
  'optimization',
  'vsenv',
]
foreach option : options
  conf_data.set(option, get_option(option))
endforeach

# C++ compiler
cpp = meson.get_compiler('cpp')
conf_data.set('compiler_name', cpp.get_id())
conf_data.set('compiler_version', cpp.version())
conf_data.set('linker_id', cpp.get_linker_id())
conf_data.set('compile_command', ' '.join(cpp.cmd_array()))

# Host and build machines
machines = {
  'host': host_machine,
  'build': build_machine,
}
foreach name, machine : machines
  conf_data.set(name + '_cpu', machine.cpu())
  conf_data.set(name + '_cpu_family', machine.cpu_family())
  conf_data.set(name + '_cpu_endian', machine.endian())
  conf_data.set(name + '_cpu_system', machine.system())
endforeach

# Write build config to python file
configure_file(
  input: '_build_config.py.in',
  output: '_build_config.py',
  configuration: conf_data,
  install_dir: py3.get_install_dir() / 'contourpy' / 'util',
)

# Print summary of important build config
foreach key : ['host_cpu', 'build_cpu', 'cross_build', 'optimization']
  summary({key: conf_data.get(key)}, section: 'Build config')
endforeach
