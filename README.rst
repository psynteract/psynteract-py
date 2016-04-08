Psynteract Python bindings
==========================

**Real-time interactive experiments for the behavioral sciences, using
Python.**

This package allows researchers to build real-time interactive
experiments in pure Python. If you are using
`PsychoPy <http://www.psychopy.org>`__,
`expyriment <http://www.expyriment.org/>`__ or a similar package to
build your studies, this is for you. If you would like to get started as
quickly as possible, please download the `latest
release <https://github.com/psynteract/psynteract-py/releases>`__ and
add the psynteract directory to your project folder.

Finally, just to be sure, please note that a `graphical interface for
OpenSesame <https://github.com/felixhenninger/psynteract-os>`__ is also
available.

Status
------

This software is currently in early beta: Most core functionality is
present and relatively stable. Additional features will be added and
internal changes are likely.

Comments, suggestions, and pull requests are very welcome!

Installation
------------

The package can be installed locally via the ``pip`` command, specifying the
latest release URL, such as::

    pip install https://github.com/psynteract/psynteract-py/releases/download/v0.6.1/psynteract-0.6.1.tar.gz

The psynteract library should then be available within the local python
installation.

To install the latest development version, please run::

    pip install git+https://github.com/psynteract/psynteract-py.git

Please note that the `psynteract backend
<https://github.com/psynteract/psynteract-backend>`__, which is bundled with
the releases, needs to be downloaded and installed separately when working
with the development version.

Shoulders of giants
-------------------

The python-based implementation of psynteract depends on the following excellent
libraries:

* `Requests <https://github.com/kennethreitz/requests/>`__ by `Kenneth Reitz
  <http://www.kennethreitz.org/>`__
* `PyCouchDB <https://github.com/histrio/py-couchdb>`__ by `Rinat Sabitov
  <https://github.com/histrio>`__

Both are bundled in the release packages.
