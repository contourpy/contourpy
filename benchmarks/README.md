Benchmarking
============

`contourpy` uses ASV (https://asv.readthedocs.io) for benchmarking.

Installing ASV
--------------

ASV creates virtualenvs to run benchmarks in.  Before using it you need to

```
pip install asv==0.4.2 virtualenv
```
or the `conda` equivalent.

Running benchmarks
------------------

To run all benchmarks against the default `main` branch:
```
cd benchmarks
asv run
```

The first time this is run it creates a machine file to store information about your machine.  Then a virtual environment is created and each benchmark is run multiple times to obtain a statistically valid benchmark time.

To list the benchmark timings stored for the `main` branch use:
```
asv show main
```

ASV ships with its own simple webserver to interactively display the results in a webbrowser.  To use this:
```
asv publish
asv preview
```
and then open a web browser at the URL specified.

If you want to quickly run all benchmarks once only to check for errors, etc, use:
```
asv dev
```
instead of `asv run`.

Configuration
-------------

ASV configuration information is stored in `benchmarks/asv.conf.json`.  This includes a list of branches to benchmark.  If you are using a feature branch and wish to benchmark the code in that branch rather than `main`, edit `asv.conf.json` to change the line
```
"branches": ["main"],
```
