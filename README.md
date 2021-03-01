# ContourPy

Python library for calculating contours of 2D quadrilateral grids.

Work in progress...

Will include current and previous Matplotlib contouring algorithms, plus a new
faster and more flexible one.  Intention is to allow Python libraries to use
contouring algorithms without having to have Matplotlib as a dependency.

To build and install using a new virtual environment

    python3 -m venv ~/venv
    . ~/venv/bin/activate
    pip install -v .

To build and install in developer's mode

    pip install -ve .

Alternatively can use

    python setup.py install

which will only recompile what has changed, but it does need pybind11 explicitly
installed beforehand using

    pip install pybind11

To run tests

    pip install -r requirements/test.txt
    pytest
