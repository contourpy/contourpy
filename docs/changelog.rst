.. _changelog:

Changelog
#########

v1.2.1 (2024 ???)
-----------------

ContourPy 1.2.1 is a compatibility release to support NumPy 2.

This release supports Python 3.9 to 3.12.

Thanks to new contributor :user:`motoro` and core maintainer :user:`ianthomas23`.

Compatibility:

- Support NumPy 2 (:pr:`331`, :pr:`371`)

Code improvements:

- Fix a few f-strings (:pr:`332`)

Documentation improvements:

- Clarify use of quotes in ``pip install`` (:pr:`349`)

Build, testing and CI improvements:

- Improved linting (:pr:`322`, :pr:`323`, :pr:`333`, :pr:`337`)
- Update ``cppcheck`` to 2.11 (:pr:`324`)
- Support running tests on unicore hosts (:pr:`327`)
- In nightly wheel tests use matplotlib as well as numpy nightlies (:pr:`329`)
- Update to chromium 118 for Bokeh renderer tests (:pr:`325`)
- Add CI run using earliest supported numpy (:pr:`347`)

v1.2.0 (2023-11-03)
-------------------

ContourPy 1.2.0 is a significant release with a number of new features. There is a new format for
contour lines called ``LineType.ChunkCombinedNan`` that is designed to work directly with Bokeh and
HoloViews. There are also new functions for manipulating contour lines and filled contours
(``convert_filled``, ``convert_lines``, ``dechunk_filled`` and ``dechunk_lines``).

Calling ``ContourGenerator.filled()`` with two identical levels now raises a ``ValueError`` whereas
previously it gave different results depending on algorithm ``name``.

This release supports Python 3.9 to 3.12, and is the first release to ship musllinux aarch64 wheels.

Enhancements:

- Support strings as well as enums in renderer functions (:pr:`284`)
- Add new functions ``dechunk_filled`` and ``dechunk_lines`` (:pr:`290`)
- Add new functions ``convert_filled`` and ``convert_lines`` (:pr:`291`, :pr:`293`, :pr:`294`, :pr:`312`, :pr:`313`)
- Add new ``LineType.ChunkCombinedNan`` (:pr:`296`, :pr:`301`, :pr:`308`)
- Raise if call ``filled()`` with ``lower_level==upper_level`` (:pr:`317`)

Code improvements:

- Code quality improvements (:pr:`282`, :pr:`310`)
- Improvements to array checking functions (:pr:`298`)
- Better use of dtypes and casting when calling numpy functions (:pr:`300`, :pr:`306`, :pr:`308`, :pr:`314`)
- Update type annotations for matplotlib 3.8 (:pr:`303`)
- Extra validation when dechunking and converting contour lines and filled contours (:pr:`316`)

Documentation improvements:

- Use ``versionadded`` sphinx directive (:pr:`285`)
- Remove threaded experimental warnings (:pr:`297`)
- Extract benchmark ratios when generating benchmark plots (:pr:`302`)
- Document new functions and conversion to Shapely geometries (:pr:`318`)

Build, testing and CI improvements:

- Add new CI run using NumPy nightly wheels (:pr:`280`)
- Test contour levels that are ``+/-np.inf`` (:pr:`283`)
- Improved PyPy CI (:pr:`287`, :pr:`307`)
- Use better names for enums when reporting parameterised tests (:pr:`292`)
- Improved mpl debug renderer tests (:pr:`295`)
- Support musllinux aarch64 (:pr:`305`)
- Run test suite in parallel (:pr:`311`)
- Miscellaneous build and CI improvements (:pr:`279`, :pr:`281`, :pr:`288`, :pr:`315`, :pr:`319`)

v1.1.1 (2023-09-16)
-------------------

This release adds support for CPython 3.12 and reinstates the release of
Windows 32-bit wheels following NumPy's intention to continue doing so.
There is a new keyword argument ``webdriver`` to the ``BokehRenderer`` save
functions to reuse the same Selenium WebDriver instance across multiple calls.

This release supports Python 3.8 to 3.12.

Thanks to new contributor :user:`shadchin` and existing contributors
:user:`eli-schwartz` and :user:`ianthomas23`.

Enhancements:

- Add ``webdriver`` kwarg to Bokeh export functions (:pr:`261`)
- Add ``--driver-path`` pytest option to specify chrome driver path (:pr:`264`)

Code improvements:

- Sync constant name with C++ code (:pr:`258`)
- Improved validation in internal chunk functions (:pr:`266`)

Documentation improvements:

- Exclude prompts when using sphinx copybutton (:pr:`269`)

Build system and CI improvements:

- Support CPython 3.12 (:pr:`254`, :pr:`272`)
- Reinstate Windows 32-bit testing and wheels (:pr:`274`, :pr:`275`)
- Update build and CI dependencies (:pr:`256`, :pr:`257`, :pr:`259`)
- Don't require `ninja`_ to come from PyPI (:pr:`260`)
- Re-enable bokeh tests in CI (:pr:`263`)
- Add tests for saving to PNG and SVG using Matplotlib and Bokeh renderers (:pr:`267`)
- Pin numpy to less than 2.0 (:pr:`268`)
- Remove `ninja`_ build requirements (:pr:`270`)

v1.1.0 (2023-06-13)
-------------------

This release features a change in the build system from ``distutils``, which
is scheduled for removal in Python 3.12, to `meson`_ and `meson-python`_.
It includes the building of wheels for ppc64le and s390x (on x86_64 only) and
removes building of all 32-bit wheels and macOS universal2 wheels.

.. note::

   Windows 32-bit wheels were retroactively released for v1.1.0 on 2023-09-15
   following NumPy's decision to keep releasing Win32 wheels.

This release supports Python 3.8 to 3.11.

Thanks to new contributor :user:`eli-schwartz`.

Build system improvements:

* New meson build system (:pr:`183`, :pr:`226`, :pr:`232`, :pr:`249`, :pr:`250`)
* Drop building universal2 wheels (:pr:`225`)
* Add build_config to store and show build configuration info (:pr:`227`)
* Build ppc64le and s390x wheels (:pr:`246`)

Code improvements:

* Rearrange functions alphabetically (:pr:`219`)
* Remove unused mpl2005 and mpl2014 code (:pr:`234`, :pr:`237`)
* Improve mpl2014 chunk count error handling (:pr:`238`)

Documentation improvements:

* Improve API docs (:pr:`220`, :pr:`221`, :pr:`222`)
* Update benchmarks (:pr:`233`)
* Add meson-specific build docs (:pr:`245`)
* Add simpler README for PyPI (:pr:`247`)

CI improvements:

* Replace flake8 with ruff (:pr:`211`)
* Building and testing on cirrus CI (:pr:`213`)
* Run mypy in CI (:pr:`230`)
* Set up code coverage in CI (:pr:`235`, :pr:`236`, :pr:`183`)
* New internal API, codebase and debug renderer tests (:pr:`239`, :pr:`241`, :pr:`244`)
* Use correct version of chromium for Bokeh image tests (:pr:`243`)
* Add tests for musllinux (on x86_64), ppc64le and s390x (:pr:`246`)

v1.0.7 (2023-01-13)
-------------------

This release adds type annotations and moves project metadata to pyproject.toml (PEP 621).
Documentation now uses the Sphinx Furo theme, supporting dark and light modes. There are no
functional changes.

Type annotations:

* Add type annotations (:pr:`199`, :pr:`200`, :pr:`201`, :pr:`202`)
* Complete mypy configuration (:pr:`206`)

Documentation improvements:

* Support dark mode (:pr:`185`, :pr:`188`)
* Use sphinx copy button (:pr:`189`)
* Add conda monthly download badges to README (:pr:`192`)
* Furo sphinx theme (:pr:`195`)

Code improvements:

* Improved if statement (:pr:`186`)
* Test nonfinite z and decreasing zlevel for filled (:pr:`190`)
* Add abstract base class Renderer (:pr:`198`)
* Replace mpl scatter call with plot instead (:pr:`203`)
* Use absolute imports (:pr:`204`)
* Minor improvement to get_boundary_start_point (:pr:`205`)

Build system and CI improvements:

* Switch from setup.cfg to pyproject.toml (:pr:`181`)
* Add git pre-commit (:pr:`191`)
* Test improvements (:pr:`193`, :pr:`194`, :pr:`197`)
* CI improvements (:pr:`179`, :pr:`180`, :pr:`184`)

v1.0.6 (2022-10-30)
-------------------

This release features major improvements to the robustness of the threaded algorithm on both
CPython and PyPy.

Thanks to new contributors :user:`mgorny` and :user:`Zac-HD`.

Threaded algorithm improvements:

* Correctly acquire and release GIL in multithreaded code (:pr:`172`)
* Update benchmarks in line with recent changes (:pr:`174`)

CI improvements:

* Add PyPy 3.9 to CI (:pr:`173`)
* Use numpy debug build in debug CI run (:pr:`175`)

v1.0.5 (2022-09-02)
-------------------

This release includes performance improvements for threaded and serial chunked algorithms, and is
the first release to support CPython 3.11.

Performance improvements:

* Shorter threaded lock (:pr:`154`)
* Init cache by chunk if more than 1 chunk (:pr:`155`)
* Update benchmark documentation and plots (:pr:`156`)

CPython 3.11 support:

* Add python 3.11 release candidate to CI (:pr:`151`)
* Build CPython 3.11 wheels (:pr:`152`)

v1.0.4 (2022-07-31)
-------------------

This release puts all C++ code within a namespace to avoid symbol conflicts such as on IBM AIX.

* Add namespace (:pr:`144`)
* Allow install of test dependencies without codebase deps (:pr:`147`)

v1.0.3 (2022-06-12)
-------------------

* Remove unnecessary code duplication (:pr:`130`)
* ContourGenerator base class (:pr:`131`)
* Mark tests that need mpl (:pr:`133`)
* Fix for PyPy np.resize bug (:pr:`135`)
* Initialise mpl backend when first needed (:pr:`137`)
* Add isort to pytest (:pr:`138`)

v1.0.2 (2022-04-08)
-------------------

* Add tests that do not write text to images (:pr:`124`)

v1.0.1 (2022-03-02)
-------------------

* Add docs and tests to sdist (:pr:`119`)
* Relax numpy version requirement (:pr:`120`)

v1.0.0 (2022-02-19)
-------------------

Finalised API for version 1.0 release.

* Synonym functions for backward compatibility with Matplotlib (:pr:`111`)
* Add benchmarks to docs (:pr:`112`)
* Updated readmes, added security policy and code of conduct (:pr:`113`)
* Improved name to class mapping (:pr:`114`)
* Convert np.nan/np.inf in z to masked array (:pr:`115`)

v0.0.5 (2022-02-13)
-------------------

* All ContourGenerator classes implement the same readonly properties (:pr:`91`)
* Support string to enum conversion in contour_generator (:pr:`92`)
* Default line/fill type for serial/threaded (:pr:`96`)
* Check for negative z if using log interp (:pr:`97`)
* contour_generator args vs kwargs (:pr:`99`)
* String to enum moved from C++ to python (:pr:`100`)
* Don't store mask in mpl2005 (:pr:`101`)
* Sphinx documentation (:pr:`102`)
* Fixed missing SW corner mask starts (:pr:`105`)
* Finalise enum spellings (:pr:`106`)
* Complete mask render function (:pr:`107`)
* Test filled compare slow (:pr:`108`)

v0.0.4 (2021-11-07)
-------------------

* Build on Python 3.10 (:pr:`76`)

v0.0.3 (2021-10-01)
-------------------

* Improvements to build on older MSVC (:pr:`85`)

v0.0.2 (2021-09-30)
-------------------

* Include license file in sdist (:pr:`81`)

v0.0.1 (2021-09-20)
-------------------

* Initial release.
