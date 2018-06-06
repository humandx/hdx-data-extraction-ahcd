# -*- coding: utf-8 -*-
"""
File for installing namcs package.
"""
# Python modules
import os
import setuptools

# Third party modules
# -N/A

# Global vars
# -N/A


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as \
        file_handle:
    long_description = file_handle.read()

# Call to method
setuptools.setup(
    name = 'namcs',
    version = '0.0.2.2',
    author = 'HumanDx',
    author_email = 'rishab.parate@icc.humandx.org',
    description = 'NAMCS data extractor and converter',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/humandx/NAMCS-NHAMCS-data-extraction'
          '#namcs-nhamcs-data-extraction',
    packages = setuptools.find_packages(),
    classifiers = (
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
