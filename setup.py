from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with(open(path.join(here, 'README.md'), encoding='utf-8')) as f:
    longdesc = f.read()

with(open(path.join(here, 'VERSION'), encoding='utf-8')) as f:
    version = f.read()

setup(
    name = 'cinema_asqlpy',
    version = version.strip(),
    description = 'An apsw/SQLite interface to Cinema databases.',
    long_description = longdesc,
    url = 'https://cinemascience.org',
    author = 'Jon Woodring',
    author_email = 'woodring@lanl.gov',
    license = 'BSD',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        # TODO Get the software type category
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        ],
    keywords = 'Cinema apsw SQL SQLite',
    packages = find_packages(exclude=['docs', 'test']),

    # There isn't a requirements on apsw, because:
    # The author of apsw doesn't suggest using the pypi version,
    # as he doesn't maintain it. The proper way to install is to
    # clone from github @ https://github.com/rogerbinns/apsw
    # and then 'pip install .' from the cloned 'apsw' directory.

    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    )
