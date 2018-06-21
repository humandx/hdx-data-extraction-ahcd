# -*- coding: utf-8 -*-
"""
Tests for namcs_validators module.
"""
# Python modules
import os
from unittest import TestCase

# Third party modules
# -N/A

# Other modules
from hdx_ahcd.scripts.namcs_validators import (
    _check_if_file_exists,
    _validate_dataset_file_name_format,
    _validate_year_from_dataset_file_name,
    _validate_dataset_file_name,
    validate_arguments,
    validate_dataset_records,
    _validate_namcs_year
)


class ValidationTest(TestCase):
    """
    TestCase class for NAMCS validations.
    """
    def test_validate_dataset_records(self):
        """
        Test if downloaded NAMCS file is valid for given year.
        """
        # Setup
        year = 2000
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")

        # Call to func :func:`validate_dataset_records`
        validation_obj = validate_dataset_records(year, test_file_path)

        # Assert validation object
        self.assertTrue(validation_obj.is_valid)

    def test_validate_arguments(self):
        """
        Test if arguments provided to the methods are correct.
        """
        # Setup
        year = 2000
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")

        # Call to func :func:`validate_arguments`
        validation_obj = validate_arguments(year, test_file_path)

        # Assert validation object
        self.assertTrue(validation_obj.is_valid)

    def test__check_if_file_exists(self):
        """
        Test if NAMCS file provided by user exists in the filesystem.
        """
        # Setup
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")

        # Call to func :func:`_check_if_file_exists`
        validation_obj = _check_if_file_exists(test_file_path)

        # Assert validation object
        self.assertTrue(validation_obj.is_valid)

    def test__validate_dataset_file_name_format(self):
        """
        Test if NAMCS file specified by user is per expected format.
        """
        # Setup
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")

        # Call to func :func:`_validate_dataset_file_name_format`
        validation_obj = _validate_dataset_file_name_format(test_file_path)

        # Assert validation object
        self.assertTrue(validation_obj.is_valid)

    def test__validate_year_from_dataset_file_name(self):
        """
        Test if extraction of year from NAMCS file name is possible.
        """
        # Setup
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")

        # Call to func :func:`_validate_year_from_dataset_file_name`
        validation_obj = _validate_year_from_dataset_file_name(test_file_path)

        # Assert validation object
        self.assertTrue(validation_obj.is_valid)

    def test__validate_dataset_file_name(self):
        """
        Test if ,
            1. Extraction of year from NAMCS file name is possible.
            2. NAMCS file specified by user is per expected format.
        """
        # Setup
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")

        # Call to func :func:`_validate_dataset_file_name`
        validation_obj = _validate_dataset_file_name(test_file_path)

        # Assert validation object
        self.assertTrue(validation_obj.is_valid)

    def test__validate_namcs_year(self):
        """
        Test if year for NAMCS is valid or not.
        """
        # Case 1: year is valid
        # Setup
        year = 2000

        # Call to func :func:`_validate_namcs_year`
        validation_obj = _validate_namcs_year(year)

        # Assert validation object
        self.assertTrue(validation_obj.is_valid)

        # Case 2: year is not valid
        # Setup
        year = 1991

        # Call to func :func:`_validate_namcs_year`
        validation_obj = _validate_namcs_year(year)

        # Assert validation object
        self.assertFalse(validation_obj.is_valid)
