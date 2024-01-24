# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Project information -----------------------------------------------------
import datetime
from pathlib import Path

import pathlib
from datetime import datetime

from sunpy_soar import __version__

project = "sunpy-soar"
copyright = f"{datetime.datetime.now().year}, The SunPy Community"  # NOQA: A001, DTZ005
author = "The SunPy Community"
release = __version__
is_development = ".dev" in __version__

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "sphinx_changelog",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = ".rst"
master_doc = "index"
default_role = "obj"
napoleon_use_rtype = False
napoleon_google_docstring = False

# -- Options for intersphinx extension ---------------------------------------
intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3/",
        (None, "http://data.astropy.org/intersphinx/python3.inv"),
    ),
    "numpy": (
        "https://docs.scipy.org/doc/numpy/",
        (None, "http://data.astropy.org/intersphinx/numpy.inv"),
    ),
    "scipy": (
        "https://docs.scipy.org/doc/scipy/reference/",
        (None, "http://data.astropy.org/intersphinx/scipy.inv"),
    ),
    "matplotlib": (
        "https://matplotlib.org/",
        (None, "http://data.astropy.org/intersphinx/matplotlib.inv"),
    ),
    "astropy": ("http://docs.astropy.org/en/stable/", None),
    "sunpy": ("https://docs.sunpy.org/en/stable/", None),
    "parfive": ("https://parfive.readthedocs.io/en/stable/", None),
}

# -- Options for HTML output -------------------------------------------------
html_theme = "sunpy"
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Nfontsize=10",
    "-Nfontname=Helvetica Neue, Helvetica, Arial, sans-serif",
    "-Efontsize=10",
    "-Efontname=Helvetica Neue, Helvetica, Arial, sans-serif",
    "-Gfontsize=10",
    "-Gfontname=Helvetica Neue, Helvetica, Arial, sans-serif",
]

# -- Options for sphinx-copybutton ---------------------------------------------
# Python Repl + continuation, Bash, ipython and qtconsole + continuation, jupyter-console + continuation
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Enable nitpicky mode, which forces links to be non-broken
nitpicky = True
# This is not used. See docs/nitpick-exceptions file for the actual listing.
nitpick_ignore = []
with Path("nitpick-exceptions").open() as f:
    for line in f.readlines():
        if line.strip() == "" or line.startswith("#"):
            continue
        dtype, target = line.split(None, 1)
        target = target.strip()
        nitpick_ignore.append((dtype, target))

# -- Options for the Sphinx gallery -------------------------------------------
path = pathlib.Path.cwd()
example_dir = path.parent.joinpath("examples")
sphinx_gallery_conf = {
    "backreferences_dir": str(path.joinpath("generated", "modules")),
    "filename_pattern": "^((?!skip_).)*$",
    "examples_dirs": example_dir,
    "gallery_dirs": path.joinpath("generated", "gallery"),
    "default_thumb_file": path.joinpath("logo", "sunpy_icon_128x128.png"),
    "abort_on_example_error": False,
    "plot_gallery": "True",
    "remove_config_comments": True,
    "only_warn_on_example_error": True,
}
