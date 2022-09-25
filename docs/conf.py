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

import sphinx_rtd_theme

sys.path.append(os.path.abspath("./sphinxext"))


# -- Project information -----------------------------------------------------

project = 'ContourPy'
copyright = '2021-2022, ContourPy Contributors'
author = 'ContourPy Contributors'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "name_supports",
    "name_supports_type",
    "plot_directive",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_path = ["_themes", ]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_favicon = '_static/contourpy_favicon.ico'

html_logo = '_static/contourpy_logo_horiz_white.svg'

html_theme_options = {
    'logo_only': True,
    'prev_next_buttons_location': 'bottom',
}

rst_epilog = """
.. _Bokeh: https://bokeh.org/
.. _Matplotlib: https://matplotlib.org/
.. _NumPy: https://numpy.org/
.. _PyPI: https://pypi.org/project/contourpy/
.. _conda-forge: https://anaconda.org/conda-forge/contourpy/
.. _default: https://anaconda.org/anaconda/contourpy/
.. _github: https://www.github.com/contourpy/contourpy/
.. _pybind11: https://pybind11.readthedocs.io/
"""
