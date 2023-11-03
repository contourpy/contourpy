# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.append(os.path.abspath("./sphinxext"))


# -- Project information -----------------------------------------------------

project = "ContourPy"
copyright = "2021-2023, ContourPy Contributors"
author = "ContourPy Contributors"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "name_supports",
    "name_supports_type",
    "plot_directive",
]

autodoc_typehints = "none"

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

html_theme_path = ["_themes"]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_favicon = "_static/contourpy_favicon.ico"

html_theme_options = {
    "dark_logo": "contourpy_logo_horiz_white.svg",
    "light_logo": "contourpy_logo_horiz.svg",
    "sidebar_hide_name": True,
}

rst_epilog = """
.. _Bokeh: https://bokeh.org/
.. _Clang: https://clang.llvm.org/
.. _GCC: https://gcc.gnu.org/
.. _HoloViews: https://holoviews.org/
.. _Matplotlib: https://matplotlib.org/
.. _MSVC: https://visualstudio.microsoft.com/
.. _NumPy: https://numpy.org/
.. _PyPI: https://pypi.org/project/contourpy/
.. _Shapely: https://shapely.readthedocs.io/
.. _conda: https://conda.io/
.. _conda-forge: https://anaconda.org/conda-forge/contourpy/
.. _default: https://anaconda.org/anaconda/contourpy/
.. _github: https://www.github.com/contourpy/contourpy/
.. _meson: https://mesonbuild.com/
.. _meson-python: https://meson-python.readthedocs.io/
.. _ninja: https://ninja-build.org/
.. _pre-commit: https://pre-commit.com/
.. _pybind11: https://pybind11.readthedocs.io/
.. _pyenv: https://github.com/pyenv/pyenv/
.. _virtualenv: https://virtualenv.pypa.io/en/latest/
"""

extlinks = {
    "pr": ("https://github.com/contourpy/contourpy/pull/%s", "#%s"),
    "user": ("https://github.com/%s", "@%s"),
}
