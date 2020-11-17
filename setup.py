# --------------------------------------------
# Copyright 2020, Grant Viklund
# @Author: Grant Viklund
# @Date:   2020-11-17 12:32:06
# --------------------------------------------

from os import path
from setuptools import setup, find_packages

from releasenotes.__version__ import VERSION

readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')

try:
    from m2r import parse_from_file
    long_description = parse_from_file(readme_file)     # Convert the file to RST for PyPI
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        long_description = f.read()

package_metadata = {
    'name': 'django-release-notes',
    'version': VERSION,
    'description': "A Simple Tools for Managing Release Notes for a Site",
    'long_description': long_description,
    'url': 'https://github.com/renderbox/django-release-notes/',
    'author': 'Grant Viklund',
    'author_email': 'renderbox@gmail.com',
    'license': 'MIT license',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    'keywords': ['django', 'app'],
}

setup(
    **package_metadata,
    packages=find_packages(),
    package_data={'releasenotes': ['*.html']},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'Django>=3.0,<3.2',
        'django-autoslug',
    ],
    extras_require={
        'dev': [                            # Packages needed by developers
            'django-crispy-forms',
            'django-allauth',
            'django-extensions',
        ],
        'test': [],                         # Packages needed to run tests
        'prod': [],                         # Packages needed to run in the deployment
        'build': [                          # Packages needed to build the package
            'setuptools',
            'wheel',
            'twine',
        ],
        'docs': [                           # Packages needed to generate docs
            'coverage',
            'Sphinx',
            'recommonmark',
            'rstcheck',
            'sphinx-rtd-theme',  # Assumes a Read The Docs theme for opensource projects
        ],
    }
)