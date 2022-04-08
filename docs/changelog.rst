.. _changelog:

Changelog
#########

v1.0.2 (2022-04-08)
-------------------

* Add tests that do not write text to images `#124 <https://github.com/contourpy/contourpy/pull/124>`_

v1.0.1 (2022-03-02)
-------------------

* Add docs and tests to sdist `#119 <https://github.com/contourpy/contourpy/pull/119>`_
* Relax numpy version requirement `#120 <https://github.com/contourpy/contourpy/pull/120>`_

v1.0.0 (2022-02-19)
-------------------

Finalised API for version 1.0 release.

* Synonym functions for backward compatibility with Matplotlib `#111 <https://github.com/contourpy/contourpy/pull/111>`_
* Add benchmarks to docs `#112 <https://github.com/contourpy/contourpy/pull/112>`_
* Updated readmes, added security policy and code of conduct `#113 <https://github.com/contourpy/contourpy/pull/113>`_
* Improved name to class mapping `#114 <https://github.com/contourpy/contourpy/pull/114>`_
* Convert np.nan/np.inf in z to masked array `#115 <https://github.com/contourpy/contourpy/pull/115>`_

v0.0.5 (2022-02-13)
-------------------

* All ContourGenerator classes implement the same readonly properties `#91 <https://github.com/contourpy/contourpy/pull/91>`_
* Support string to enum conversion in contour_generator `#92 <https://github.com/contourpy/contourpy/pull/92>`_
* Default line/fill type for serial/threaded `#96 <https://github.com/contourpy/contourpy/pull/96>`_
* Check for negative z if using log interp `#97 <https://github.com/contourpy/contourpy/pull/97>`_
* contour_generator args vs kwargs `#99 <https://github.com/contourpy/contourpy/pull/99>`_
* String to enum moved from C++ to python `#100 <https://github.com/contourpy/contourpy/pull/100>`_
* Don't store mask in mpl2005 `#101 <https://github.com/contourpy/contourpy/pull/101>`_
* Sphinx documentation `#102 <https://github.com/contourpy/contourpy/pull/102>`_
* Fixed missing SW corner mask starts `#105 <https://github.com/contourpy/contourpy/pull/105>`_
* Finalise enum spellings `#106 <https://github.com/contourpy/contourpy/pull/106>`_
* Complete mask render function `#107 <https://github.com/contourpy/contourpy/pull/107>`_
* Test filled compare slow `#108 <https://github.com/contourpy/contourpy/pull/108>`_

v0.0.4 (2021-11-07)
-------------------

* Build on Python 3.10 `#76 <https://github.com/contourpy/contourpy/pull/76>`_

v0.0.3 (2021-10-01)
-------------------

* Improvements to build on older MSVC. `#85 <https://github.com/contourpy/contourpy/pull/85>`_

v0.0.2 (2021-09-30)
-------------------

* Include license file in sdist. `#81 <https://github.com/contourpy/contourpy/pull/81>`_

v0.0.1 (2021-09-20)
-------------------

* Initial release.
