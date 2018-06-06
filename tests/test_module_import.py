# -*- coding: utf-8 -*-
"""
Check if all the modules are importable and do not have cyclic import issue.
"""
# Python modules
from unittest import TestCase

# Third party modules
# -N/A

# HDx modules
# -N/A


class ImportModuleTest(TestCase):
    """
    Test if modules can be imported successfully.
    Note: This is just a sanity check and does not validate any functionality.
    """
    @classmethod
    def setUpClass(cls):
        """
        Extended implementation of setUpClass
        """
        import os
        import sys
        sys.path.insert(
            0,
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "namcs")
        )

    def test_enums(self):
        import namcs.enums

    def test_constants(self):
        import namcs.constants

    def test_config(self):
        import namcs.config

    def test_controllers(self):
        import scripts.controllers

    def test_script_validation(self):
        import scripts.validation

    def test_mapper_functions(self):
        import mapper.functions

    def test_mapper_years(self):
        import mapper.years

    def test_helpers_functions(self):
        import helpers.functions

    def test_general_namcs_extractor(self):
        import general.namcs_extractor

    def test_general_namcs_convertor(self):
        import general.namcs_convertor

    def test_utils_context(self):
        import utils.context

    def test_utils_decorators(self):
        import utils.decorators

    def test_utils_exceptions(self):
        import utils.exceptions

    def test_utils_utils(self):
        import utils.utils
