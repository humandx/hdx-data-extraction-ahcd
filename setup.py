# -*- coding: utf-8 -*-
"""
Module for installing package hdx_ahcd.
"""
# Python modules
import os
from setuptools import (find_packages, setup)

# Third party modules
# -N/A

# Global vars
# -N/A


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as \
        file_handle:
    long_description = file_handle.read()

config = {
    'name': 'hdx_ahcd',
    'version': '1.0.24',

    # 1.0.1 - Initial setup.
    # 1.0.2 - Added NAMCS extractor and converter for public dataset.
    # 1.0.3 - Added use_regex parameter for decorator enforce_type.
    # 1.0.4 - Fixed typos.
    # 1.0.5 - Added traceback details for exception and tests for use_regex
    # parameter of decorator enforce_type.
    # 1.0.6 - Minor code fixes encountered in testing.
    # 1.0.7 - Update README with AHCD description.
    # 1.0.8 - Merge branch 'master' into feat/download-and-extract-NAMCS.
    # 1.0.9 - Changed package name to hdx_ahcd.
    # 1.0.10 - Removed .pyc files.
    # 1.0.11 - Fixed issue with relative import.
    # 1.0.12 - Added mapping for year 1992 to 1998.
    # 1.0.13 - Added mappings for year 1995 and 1996.
    # 1.0.14 - Added visit weight for all years.
    # 1.0.15 - Added NAMCS extractor and converter for public dataset.
    # 1.0.16 - Merge pull request #1 from
    # humandx/feat/download-and-extract-NAMCS.
    # 1.0.17 - Restructuring_and_refactoring_package.
    # 1.0.18 - Refactored code, minor code fixes.
    # 1.0.19 - Refactored code, minor code fixes.
    # 1.0.20 - Refactored code,changed logic of module namcs_processors and
    #   namcs_extractor.
    # 1.0.21 - Refactored code,minor code fixes.
    # 1.0.22 - Changed docstring.
    # 1.0.23 - Import issue fixed.
    # 1.0.24 - Added abstract methods to module `years`,
    # Moved contents ofCHANGELOG.MD to setup.py,Removed some of
    # contents from docstring.

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
