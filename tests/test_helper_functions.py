# -*- coding: utf-8 -*-
"""
Module containing tests for module `helper.functions`.
"""
# Python modules
from unittest import mock, TestCase
import datetime
import os

# Other modules
from hdx_ahcd.helpers import functions
from hdx_ahcd.helpers.functions import (
    get_customized_file_name,
    get_conversion_method,
    get_field_code_from_record,
    get_iterable,
    get_namcs_dataset_path_for_year,
    get_namcs_source_file_info,
    get_normalized_namcs_file_name, 
    get_string_representations_of_date,
    get_slice_object,
    get_year_from_dataset_file_name,
    rename_namcs_dataset_for_year,
    populate_missing_fields,
    process_multiple_slice_objects,
)
from hdx_ahcd.namcs.enums import NAMCSFieldEnum

# Third party modules
# -N/A


class HelperFunctionsTest(TestCase):
    """
    TestCase class for helper functions.
    """
    def test_get_conversion_method(self):
        """
        Test to validate correct method for `field_name`.
        """
        # Case 1: when corresponding method for `field_name` is present
        # Setup
        field_name = "age"
        expected_method_for_field_name = "get_age_normalized_to_days"

        # Call to :func:`get_conversion_method`
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Setup
        field_name = "month_of_birth"
        expected_method_for_field_name = "get_month_from_date"

        # Call to func :func:`get_conversion_method`
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Setup
        field_name = "month_of_visit"
        expected_method_for_field_name = "get_month_from_date"

        # Call to func :func:`get_conversion_method`
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Setup
        field_name = "physician_diagnoses"
        expected_method_for_field_name = "convert_physician_diagnoses_code"

        # Call to func :func:`get_conversion_method`
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Case 2: when corresponding method for `field_name` is  not present
        # Setup
        field_name = "Test_field_name"

        # Call to func :func:`get_conversion_method`
        # Asserting if exception is raised
        with self.assertRaises(Exception):
            get_conversion_method(field_name)

    def test_get_customized_file_name(self):
        """
        Test to check valid file name in customized way.
        """
        # Case 1: when only one string needs to be customized
        # example: "NAME.CSV"
        # Setup
        names = "Test"
        extension = "CSV"
        expected_file_name = "Test.CSV"

        # Call to func :func:`get_customized_file_name`
        actual_file_name = \
            get_customized_file_name(names, extension=extension)

        # Assert for valid customized file name
        self.assertEqual(expected_file_name, actual_file_name)

        # Case 2: when only multiple string needs to be customized
        # example: "1993_NAMCS_RAW_DATASET_FILE_NAME.CSV"
        # Setup
        names = (1993, "NAMCS", "RAW", "DATASET", "FILE", "NAME")
        separator = "_"
        extension = "csv"
        expected_file_name = "1993_NAMCS_RAW_DATASET_FILE_NAME.csv"

        # Call to func :func:`get_customized_file_name`
        actual_file_name = get_customized_file_name(
                names, separator=separator, extension=extension
        )

        # Assert for valid customized file name
        self.assertEqual(expected_file_name, actual_file_name)

    def test_get_field_code_from_record(self):
        """
        Test to validate correct field code for `field_name` from raw dataset
        record.
        """
        # Setup
        # NAMCS 1973 raw record
        record = "067310101131200000000031101000000000004700Y0320000010100" \
                 "10000010000005000001347910111"

        # Case 1: when corresponding method for `field_name` is present
        # Field name gender
        field_name = NAMCSFieldEnum.GENDER.value
        slice_object = slice(8, 9, None)
        expected_field_code = "Female"

        # Call to func :func:`get_field_code_from_record`
        actual_field_code = get_field_code_from_record(
            record=record, field_name=field_name, slice_object=slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Field name month of birth
        field_name = NAMCSFieldEnum.MONTH_OF_BIRTH.value
        slice_object = slice(4, 6, None)
        expected_field_code = 10

        # Call to func :func:`get_field_code_from_record`
        actual_field_code = get_field_code_from_record(
            record=record, field_name=field_name, slice_object=slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Field name month of visit
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
        slice_object = slice(0, 2, None)
        expected_field_code = 6

        # Call to func :func:`get_field_code_from_record`
        actual_field_code = get_field_code_from_record(
            record=record, field_name=field_name, slice_object=slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Field name year of visit
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
        slice_object = slice(2, 4, None)
        expected_field_code = 1973

        # Call to func :func:`get_field_code_from_record`
        actual_field_code = get_field_code_from_record(
            record=record, field_name=field_name, slice_object=slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Case 2: when corresponding method for `field_name` is not present
        # Field name gender
        field_name = NAMCSFieldEnum.GENDER.value
        slice_object = slice(11, 15, None)

        # Call to func :func:`get_field_code_from_record`
        # Asserting Exception is raised
        with self.assertRaises(Exception):
            get_field_code_from_record(
                record=record, field_name=field_name, slice_object=slice_object
            )

    def test_get_file_path_by_year(self):
        """
        Test to validate correct raw dataset file path for NAMCS year
        """
        # Setup
        year = 2000

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        expected_file_path = \
            os.path.join(functions.EXTRACTED_DATA_DIR_PATH, "2000_NAMCS")

        # Call to func :func:`get_namcs_dataset_path_for_year`
        actual_file_path = get_namcs_dataset_path_for_year(year)

        # Assert for valid file name for year 2000
        self.assertEqual(expected_file_path, actual_file_path)

    def test_get_public_file_name_url(self):
        """
        Test for valid source file details.
        """
        # Setup
        expected_source_file_info = {
            "zip_file_name": "NAMCS00.exe",
            "year": "00",
            "url": "ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/"
                   "NAMCS/NAMCS00.exe"
        }
        year = 2000

        # Call to func :func:`get_namcs_source_file_info`
        actual_source_file_info = get_namcs_source_file_info(year)

        # Assert for valid source file info details
        self.assertDictEqual(
            expected_source_file_info, actual_source_file_info
        )

    def test_get_slice_object(self):
        """
        Test for valid slice object based on the `indexes` passed.
        """
        # Setup
        # Case 1: When `field_length` > 1
        field_location = 47
        field_length = 4
        expected_slice_object = slice(46, 50, None)

        # Call to func :func:`get_slice_object`
        actual_slice_object = get_slice_object(field_location, field_length)

        # Assert for valid slice object
        self.assertEqual(expected_slice_object, actual_slice_object)

        # Case 2: When `field_length` is 1
        field_location = 11
        field_length = 1
        expected_slice_object = slice(10, 11)

        # Call to func :func:`get_slice_object`
        actual_slice_object = get_slice_object(field_location, field_length)

        # Assert for valid slice object
        self.assertEqual(expected_slice_object, actual_slice_object)

    def test_get_string_format_date_time(self):
        """
        Test for valid year, month, day from date in desired format.
        """
        # Setup
        year = 1997
        month = 6
        day = 1
        expected_date_representations = {
            "day_numeric": "01",
            "date_time_object": datetime.datetime(1997, 6, 1, 0, 0),
            "month_long": "June",
            "month_short": "Jun",
            "year_short": "97",
            "month_numeric": "06",
            "year_long": "1997"
        }

        # Call to func :func:`get_string_representations_of_date`
        actual_date_representations = \
            get_string_representations_of_date(year, month, day)

        # Assert for valid date representations
        self.assertDictEqual(
            expected_date_representations, actual_date_representations
        )

    @mock.patch("hdx_ahcd.helpers.functions.os.path.exists")
    def test_get_year_from_dataset_file(self, mocked_path_exists):
        """
        Test to check if valid year is returned from NAMCS dataset file name.
        """
        # Setup
        file_name = "2000_NAMCS"
        expected_year = 2000

        # Mocking `os.path.exists` return value
        mocked_path_exists.return_value = True

        # Call to func :func:`get_year_from_dataset_file_name`
        actual_year = get_year_from_dataset_file_name(file_name)

        # Assert if correct year is extracted from the file_name
        self.assertEqual(expected_year, actual_year)

    def test_handle_iterable_slice_object(self):
        """
        Test for valid field codes from raw record.
        """
        # Setup
        # NAMCS 1973 raw record
        record = "067310101131200000000031101000000000004700Y0320000010100" \
                 "0000010000005000001347910111"
        # Field name physician_diagnosis
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSES.value
        iterable_slice_object = [
            slice(38, 42, None), slice(42, 46, None), slice(46, 50, None)
        ]
        expected_field_codes = ["470.0", "V03.2", ""]

        # Call to func :func:`process_multiple_slice_objects`
        actual_field_codes = process_multiple_slice_objects(
            record = record,
            field_name = field_name,
            iterable_slice_object = iterable_slice_object
        )

        # Assert for valid field codes for `field_name`
        self.assertSetEqual(
            set(expected_field_codes), set(actual_field_codes)
        )

    def test_populate_calculated_fields(self):
        """
        Test to check if only `CONVERTED_CSV_FIELDS` are being populated for
        NAMCS year.
        """
        # Setup
        # Fields those are required in the final converted csv file
        expected_headers = (
            "source_file_ID",
            "source_file_row",
            "sex",
            "physician_diagnoses",
            "age",
            "month_of_visit",
            "year_of_visit",
        )
        expected_field_codes_for_record = {
            "source_file_ID": "1973_NAMCS",
            "source_file_row": 1,
            "sex": "Female",
            "physician_diagnoses": ["470.0", "Y03.2"],
            "age": 22889,
            "month_of_visit": 6,
            "year_of_visit": 1973
        }

        # Converted field codes for single record which needs to be filtered
        # and modified
        field_codes_for_record = {
            "source_file_ID": "1973_NAMCS",
            "source_file_row": 1,
            "sex": "Female",
            "physician_diagnoses": ["470.0", "Y03.2"],
            "month_of_birth": 10,
            "month_of_visit": 6,
            "year_of_birth": 2010,
            "year_of_visit": 1973,
        }

        # Call to func :func:`populate_missing_fields`
        actual_field_codes_for_record = populate_missing_fields(
                headers = expected_headers,
                field_codes_for_single_record = field_codes_for_record
        )

        # Asserting if unnecessary fields are filtered and
        # required fields are populated
        self.assertDictEqual(
            expected_field_codes_for_record, actual_field_codes_for_record
        )

    @mock.patch("hdx_ahcd.helpers.functions.os.rename")
    @mock.patch("hdx_ahcd.helpers.functions.os.path.exists")
    def test_rename_namcs_file(self, mocked_path_exists, mocked_os_rename):
        """
        Test to check if NAMCS raw dataset file name is renamed correctly
        """
        # Setup
        year = 2000

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Mocking `os.path.exists` return value
        mocked_path_exists.return_value = True
        expected_renamed_file_name = \
            os.path.join(functions.EXTRACTED_DATA_DIR_PATH, "2000_NAMCS")

        # Call to func :func:`rename_namcs_dataset_for_year`
        actual_renamed_file_name = rename_namcs_dataset_for_year(year)

        # Asserting os.rename call
        mocked_os_rename.assert_called_with(
            os.path.join(functions.EXTRACTED_DATA_DIR_PATH, "NAM00"),
            expected_renamed_file_name
        )

        # Assert for valid file name for year 2000
        self.assertEqual(expected_renamed_file_name, actual_renamed_file_name)

    def test_get_normalized_namcs_file_name(self):
        """
        Test for valid NAMCS file name.
        """
        # Setup
        year = 2000
        expected_file_name = "2000_NAMCS"

        # Call to :func:`get_normalized_namcs_file_name`
        actual_file_name = get_normalized_namcs_file_name(year)

        # Asert for valid NAMCS file name
        self.assertEqual(expected_file_name, actual_file_name)

    def test_get_iterable(self):
        """
        Test to check if iterable is returned by method `get_iterable`
        """
        # Case 1: When `parameter` is not iterable
        # Setup
        parameter = 2000
        expected_parameter = [2000]

        # Call to :func:`get_iterable`
        actual_parameter = get_iterable(parameter)

        # Asert for iterable `parameter`
        self.assertEqual(expected_parameter, actual_parameter)

        # Case 2: When `parameter` is iterable.
        # Setup
        parameter = ["test", "parameter"]
        expected_parameter = ["test", "parameter"]

        # Call to :func:`get_iterable`
        actual_parameter = get_iterable(parameter)

        # Asert for iterable `parameter`
        self.assertEqual(expected_parameter, actual_parameter)
