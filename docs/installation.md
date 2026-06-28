# Installation

## Installing from prepackaged binaries

### Official releases

Official releases of ContourPy are available from {{ PyPI }} and {{ conda_forge }} for Linux, macOS and
Windows.

1. To install from {{ PyPI }}:

   ```bash
   $ pip install contourpy
   ```

1. To install from {{ conda_forge }}:

   ```bash
   $ conda install -c conda-forge contourpy
   ```

The only compulsory runtime dependency is {{ NumPy }}.

If you want to make use of one of ContourPy's utility renderers in the {py:mod}`contourpy.util` module
you will also have to install either {{ Matplotlib }} or {{ Bokeh }}.

### Pre-releases

Prepackaged wheels of the latest pre-release ContourPy code, at most a week old, are available as
part of the {{ Scientific_Python }} nightly wheels service. These are intended to be used for testing
and are not necessarily stable. See {{ SPEC_4 }} for more details.


## Installing from source

If you wish to install from source code, see the {ref}`developer_guide`.
