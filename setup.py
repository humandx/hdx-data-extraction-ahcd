# -*- coding: utf-8 -*-
"""
Module for installing package `hdx_ahcd`.
"""
# Python modules
from setuptools import (find_packages, setup)
import os

# Third party modules
# -N/A

# Global vars
# -N/A


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as \
        file_handle:
    long_description = file_handle.read()

config = {
    'name': 'hdx_ahcd',
    'version': '1.0.1',

    # 1.0.0 - Initial setup.
    # 1.0.1 - Added visit weight for all years.

    # Author details
    'author': 'HumanDx',
    'author_email': 'engineering@humandx.org',

    'description': 'NAMCS data extractor and converter',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'url': 'https://github.com/humandx/NAMCS-NHAMCS-data-extraction#hdx_ahcd'
           '-nhamcs-data-extraction',
    'packages': find_packages(),
    'classifiers': (
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    )
}

# Call to method
setup(**config)
