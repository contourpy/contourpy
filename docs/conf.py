from datetime import date
import os
import sys

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./sphinxext"))

from process_changelog import process_changelog

project = "ContourPy"
author = "ContourPy Contributors"
copyright = f"2021-{date.today().year}, {author}"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "name_supports",
    "name_supports_type",
    "plot_directive",
]

autodoc_typehints = "none"

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_favicon = "_static/contourpy_favicon.ico"
html_static_path = ["_static"]
html_theme = "sphinx_book_theme"
html_theme_options = {
    "logo": {
        "alt_text": "ContourPy documentation - Home",
        "image_dark": "_static/contourpy_logo_horiz_white.svg",
        "image_light": "_static/contourpy_logo_horiz.svg",
    },
    "repository_url": "https://github.com/contourpy/contourpy",
    "use_repository_button": True,
}
html_theme_path = ["_themes"]

myst_enable_extensions = [
    "substitution",
]

myst_substitutions = {
    "Bokeh": "[Bokeh](https://bokeh.org)",
    "Clang": "[Clang](https://clang.llvm.org)",
    "GCC": "[GCC](https://gcc.gnu.org)",
    "HoloViews": "[HoloViews](https://holoviews.org)",
    "Matplotlib": "[Matplotlib](https://matplotlib.org)",
    "MSVC": "[MSVC](https://visualstudio.microsoft.com)",
    "NumPy": "[NumPy](https://numpy.org)",
    "PyPI": "[PyPI](https://pypi.org/project/contourpy)",
    "Scientific_Python": "[Scientific Python](https://scientific-python.org)",
    "Shapely": "[Shapely](https://shapely.readthedocs.io)",
    "SPEC_4": "[SPEC 4](https://scientific-python.org/specs/spec-0004)",
    "conda": "[conda](https://conda.io)",
    "conda_forge": "[conda-forge](https://anaconda.org/conda-forge/contourpy)",
    "github": "[github](https://www.github.com/contourpy/contourpy)",
    "meson": "[meson](https://mesonbuild.com)",
    "meson_python": "[meson-python](https://meson-python.readthedocs.io)",
    "ninja": "[ninja](https://ninja-build.org)",
    "pre_commit": "[pre-commit](https://pre-commit.com)",
    "pybind11": "[pybind11](https://pybind11.readthedocs.io)",
    "pyenv": "[pyenv](https://github.com/pyenv/pyenv)",
    "virtualenv": "[virtualenv](https://virtualenv.pypa.io/en/latest)",
}

python_use_unqualified_type_names = True

templates_path = ["_templates"]

process_changelog()
