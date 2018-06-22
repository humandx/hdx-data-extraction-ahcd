# -*- coding: utf-8 -*-
"""
Check if all the modules are importable and do not have cyclic import issue.
"""
# Python modules
from unittest import TestCase

# Third party modules
# -N/A

# Other modules
# -N/A


class ImportModuleTest(TestCase):
    """
    Test if modules can be imported successfully.
    Note: This is just a sanity check and does not validate any functionality.
    """
    def test_enums(self):
        import hdx_ahcd.namcs.enums

    def test_constants(self):
        import hdx_ahcd.namcs.constants

    def test_config(self):
        import hdx_ahcd.namcs.config

    def test_namcs_validators(self):
        import hdx_ahcd.scripts.namcs_validators

    def test_controllers_namcs_processors(self):
        import hdx_ahcd.controllers.namcs_processors

    def test_mapper_functions(self):
        import hdx_ahcd.mappers.functions

    def test_mapper_years(self):
        import hdx_ahcd.mappers.years

    def test_helpers_functions(self):
        import hdx_ahcd.helpers.functions

    def test_controllers_namcs_extractor(self):
        import hdx_ahcd.controllers.namcs_extractor

    def test_controllers_namcs_converter(self):
        import hdx_ahcd.controllers.namcs_converter

    def test_utils_context(self):
        import hdx_ahcd.utils.context

    def test_utils_decorators(self):
        import hdx_ahcd.utils.decorators

    def test_utils_exceptions(self):
        import hdx_ahcd.utils.exceptions

    def test_utils_utils(self):
        import hdx_ahcd.utils.utils
