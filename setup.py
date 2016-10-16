"""Python Bindings for Psynteract.

"""

# This is built on the demo package as described at
# https://packaging.python.org/en/latest/distributing.html

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='psynteract',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.8.0',

    description='Psynteract Python bindings',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/psynteract/psynteract-py',

    # Author details
    author='Felix Henninger & Pascal Kieslich',
    author_email='mailbox@felixhenninger.com',

    # License
    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Some day this will change to
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Audience
        'Intended Audience :: Developers',

        # License
        'License :: OSI Approved :: Apache Software License',

        # Python version support
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    package_dir = {'psynteract': 'psynteract'},

    package_data={
        'psynteract': ['backend.json'],
    },

    # Files to include in package
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # Run-time dependencies
    install_requires=['requests', 'pycouchdb'],

    zip_safe=False,
)
