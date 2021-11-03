Psynteract Python bindings
==========================

**Real-time interactive experiments for the behavioral sciences, using
Python.**

This package allows researchers to build real-time interactive experiments in
pure Python. If you are using `PsychoPy <http://www.psychopy.org>`__,
`expyriment <http://www.expyriment.org/>`__ or a similar package to build your
studies and are studying strategic interactions or another paradigm that
requires that participants interact in real time, this is for you.

Please note that a `graphical interface for OpenSesame
<https://github.com/psynteract/psynteract-os>`__ is also available.

----

``psynteract-py`` is developed jointly by **Felix Henninger** and **Pascal
Kieslich**. It is published under the `Apache License, Version 2.0 </LICENSE>`__.

This software is stable and has been successfully used in several studies across
multiple labs. Additional features will be added, radical changes are not
currently planned.

Comments, suggestions, and pull requests are always very welcome -- please do
not hesitate to let the authors know if we can help in any way!

Installation
------------

The package can be installed locally via the ``pip`` command, specifying the
latest release URL, such as::

    pip install https://github.com/psynteract/psynteract-py/releases/download/v0.9.0/psynteract-0.9.0.tar.gz

The psynteract library should then be available within the local python
installation.

To install the latest development version, please run::

    pip install git+https://github.com/psynteract/psynteract-py.git

Please note that the `psynteract backend
<https://github.com/psynteract/psynteract-backend>`__, which is bundled with
the releases, needs to be downloaded and installed separately if you would like
to use the backend installation function from the library.

Citation
--------

Please drop us a line if you've used the library: We sincerely love to hear
from our users!

If you use ``psynteract`` in your published research, we kindly ask that you
cite the associated article as follows:

    Henninger, F., Kieslich, P. J., & Hilbig, B. E. (2017). Psynteract:
    A flexible, cross-platform, open framework for interactive experiments.
    *Behavior Research Methods, 49*\(5), 1605-1614. doi:`10.3758/s13428-016-0801-6
    <https://dx.doi.org/10.3758/s13428-016-0801-6>`__

Acknowledgements
----------------

We would like to thank Hosam Alqaderi and Susann Fiedler at the `Max Planck
Institute for Research on Collective Goods, Bonn <http://coll.mpg.de/>`__, and
the members of the `University of Mannheim Chair of Experimental Psychology
<http://cognition.uni-mannheim.de/>`__ and the `University of Landau Cognition
Lab <http://cognition.uni-landau.de/>`__ for their feedback and testing during
the  development of this library.

Development was supported by the University of Mannheim’s `Graduate School of
Economic and Social Sciences <http://gess.uni-mannheim.de/>`__, which is funded
by the German Research Foundation.

**Shoulders of giants**

The python-based implementation of psynteract depends on the following excellent
libraries:

* `Requests <https://github.com/kennethreitz/requests/>`__ by `Kenneth Reitz
  <http://www.kennethreitz.org/>`__
* `PyCouchDB <https://github.com/histrio/py-couchdb>`__ by `Rinat Sabitov
  <https://github.com/histrio>`__
