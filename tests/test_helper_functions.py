# -*- coding: utf-8 -*-
"""
Tests for helper_functions module.
"""
# Python modules
import datetime
import os
from unittest import mock, TestCase

# Other modules
from namcs.helpers import functions
from namcs.helpers.functions import (
    get_namcs_source_file_info,
    get_year_from_dataset_file_name,
    get_string_representations_of_date,
    get_slice_object,
    process_multiple_slice_objects,
    get_icd_9_code_from_numeric_string,
    get_icd_9_code_from_database,
    get_customized_file_name,
    get_conversion_method,
    get_field_code_from_record,
    get_namcs_datset_path_for_year,
    rename_namcs_dataset_for_year, populate_missing_fields
)
from namcs.namcs.enums import NAMCSFieldEnum

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
        field_name = 'age'
        expected_method_for_field_name = 'age_reduced_to_days'

        # Call to method
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Setup
        field_name = 'month_of_birth'
        expected_method_for_field_name = 'get_month_from_date'

        # Call to method
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Setup
        field_name = 'month_of_visit'
        expected_method_for_field_name = 'get_month_from_date'

        # Call to method
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Setup
        field_name = 'physician_diagnosis'
        expected_method_for_field_name = 'convert_physician_diagnosis_code'

        # Call to method
        actual_method_for_field_name = get_conversion_method(field_name)

        # Assert to validate correct method name
        self.assertEqual(
            expected_method_for_field_name,
            actual_method_for_field_name.__name__
        )

        # Case 2: when corresponding method for `field_name` is  not present
        # Setup
        field_name = 'Test_field_name'

        # Asserting if exception is raised
        with self.assertRaises(Exception):
            # Call to method
            actual_method_for_field_name = get_conversion_method(field_name)

    def test_get_customized_file_name(self):
        """
        Test to check valid file name in customized way.
        """
        # Case 1: when only one string needs to be customized
        # example: "NAME.CSV"

        # Setup
        names = 'Test'
        separator = None
        extension = 'CSV'
        expected_file_name = 'Test.CSV'

        # Call to method
        actual_file_name = \
            get_customized_file_name(
                names, separator=separator, extension=extension
            )

        # Assert for valid customized file name
        self.assertEqual(expected_file_name, actual_file_name)

        # Case 2: when only multiple string needs to be customized
        # example: "1993_NAMCS_RAW_DATASET_FILE_NAME.CSV"
        # Setup
        names = (1993, 'NAMCS', 'RAW', 'DATASET', 'FILE', 'NAME')
        separator = '_'
        extension = 'csv'
        expected_file_name = '1993_NAMCS_RAW_DATASET_FILE_NAME.csv'

        # Call to method
        actual_file_name = \
            get_customized_file_name(
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
        record = \
            '067310101131200000000031101000000000004700Y0320000010100' \
            '10000010000005000001347910111'

        # Case 1: when corresponding method for `field_name` is present
        # Field name gender
        field_name = NAMCSFieldEnum.GENDER.value
        slice_object = slice(8, 9, None)
        expected_field_code = 'Female'

        # Call to method
        actual_field_code = get_field_code_from_record(
            line = record, field_name = field_name, slice_object = slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Field name month of birth
        field_name = NAMCSFieldEnum.MONTH_OF_BIRTH.value
        slice_object = slice(4, 6, None)
        expected_field_code = 'October'

        # Call to method
        actual_field_code = get_field_code_from_record(
            line = record, field_name = field_name, slice_object = slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Field name month of visit
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
        slice_object = slice(0, 2, None)
        expected_field_code = 'June'

        # Call to method
        actual_field_code = get_field_code_from_record(
            line = record, field_name = field_name, slice_object = slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Field name year of visit
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
        slice_object = slice(2, 4, None)
        expected_field_code = '1973'

        # Call to method
        actual_field_code = get_field_code_from_record(
            line = record, field_name = field_name, slice_object = slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

        # Case 2: when corresponding method for `field_name` is not present
        # Field name gender
        field_name = NAMCSFieldEnum.GENDER.value
        slice_object = slice(11, 15, None)
        expected_field_code = 'CODE1200'

        # Call to method
        actual_field_code = get_field_code_from_record(
            line = record, field_name = field_name, slice_object = slice_object
        )

        # Assert to validate correct field code
        self.assertEqual(expected_field_code, actual_field_code)

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
            os.path.join(functions.EXTRACTED_DATA_DIR_PATH, '2000_NAMCS')

        # Call to method
        actual_file_path = get_namcs_datset_path_for_year(year)

        # Assert for valid file name for year 2000
        self.assertEqual(expected_file_path, actual_file_path)

    def test_get_icd_9_code_from_database(self):
        """
        Test for valid ICD-9 code for `diagnosis_code`.
        """
        # TODO : Fetch corresponding ICD-9 code for `diagnosis_code`
        # from database
        # Setup
        diagnosis_icd_9_code = 'Y997'

        # TODO: change this value to actual value returned from database
        expected_icd_9_code = 'Y997'

        # Call to method
        actual_icd_9_code = \
            get_icd_9_code_from_database(diagnosis_icd_9_code)

        # Assert for valid ICD-9 code fetched form database
        self.assertEqual(
            expected_icd_9_code, actual_icd_9_code
        )

    def test_get_icd_9_code_from_numeric_string(self):
        """
        Test for validating correctness of ICD-9 code from raw `diagnosis_code`.
        """
        # Setup
        # Case 1: `diagnosis_code` is constant
        diagnosis_code = 'Y997'
        expected_diagnosis_icd_9_code = ''

        # Call to method
        actual_diagnosis_icd_9_code = \
            get_icd_9_code_from_numeric_string(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_diagnosis_icd_9_code, actual_diagnosis_icd_9_code
        )

        # Case 2: `diagnosis_code` is of 4 length and starts with 1
        diagnosis_code = '1381'
        expected_diagnosis_icd_9_code = '381.'

        # Call to method
        actual_diagnosis_icd_9_code = \
            get_icd_9_code_from_numeric_string(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_diagnosis_icd_9_code, actual_diagnosis_icd_9_code
        )

        # Case 3: `diagnosis_code` is of 6 length and starts with 1
        diagnosis_code = '138100'
        expected_diagnosis_icd_9_code = '381.00'

        # Call to method
        actual_diagnosis_icd_9_code = \
            get_icd_9_code_from_numeric_string(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_diagnosis_icd_9_code, actual_diagnosis_icd_9_code
        )

        # Case 4: `diagnosis_code` is of 4 length and starts with 2
        diagnosis_code = '2010'
        expected_diagnosis_icd_9_code = 'V10.'

        # Call to method
        actual_diagnosis_icd_9_code = \
            get_icd_9_code_from_numeric_string(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_diagnosis_icd_9_code, actual_diagnosis_icd_9_code
        )

        # Case 5: `diagnosis_code` is of 6 length and starts with 2
        diagnosis_code = '201081'
        expected_diagnosis_icd_9_code = 'V10.81'

        # Call to method
        actual_diagnosis_icd_9_code = \
            get_icd_9_code_from_numeric_string(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_diagnosis_icd_9_code, actual_diagnosis_icd_9_code
        )

        # Case 6: `diagnosis_code` starts with '-'
        diagnosis_code = '-00009'
        expected_diagnosis_icd_9_code = '000.09'

        # Call to method
        actual_diagnosis_icd_9_code = \
            get_icd_9_code_from_numeric_string(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_diagnosis_icd_9_code, actual_diagnosis_icd_9_code
        )

    def test_get_public_file_name_url(self):
        """
        Test for valid source file details.
        """
        # Setup
        expected_source_file_info = \
            {
                'zip_file_name': 'NAMCS00.exe',
                'year': '00',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS00.exe'
            }
        year = 2000

        # Call to method
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
        # Case 1: When indexes is provided as ["2", "3"]
        indexes = [4, 10]
        expected_slice_object = slice(3, 10)

        # Call to method
        actual_slice_object = get_slice_object(indexes)

        # Assert for valid slice object
        self.assertEqual(expected_slice_object, actual_slice_object)

        # Case 2: When indexes is provided as ["3"]
        indexes = [4]
        expected_slice_object = slice(3, 4)

        # Call to method
        actual_slice_object = get_slice_object(indexes)

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
        expected_date_representations = \
            {
                'day_numeric': '01',
                'date_time_object': datetime.datetime(1997, 6, 1, 0, 0),
                'month_long': 'June',
                'month_short': 'Jun',
                'year_short': '97',
                'month_numeric': '06',
                'year_long': '1997'
            }

        # Call to method
        actual_date_representations = \
            get_string_representations_of_date(year, month, day)

        # Assert for valid date representations
        self.assertDictEqual(
            expected_date_representations, actual_date_representations
        )

    def test_get_year_from_dataset_file(self):
        """
        Test to check if valid year is returned from NAMCS dataset file name.
        """
        # Setup
        file_name = '2000_NAMCS'
        expected_year = '2000'

        # Call to method
        actual_year = get_year_from_dataset_file_name(file_name)

        # Assert if correct year is extracted from the file_name
        self.assertEqual(expected_year, actual_year)

    def test_handle_iterable_slice_object(self):
        """
        Test for valid field codes from raw record.
        """
        # Setup
        # NAMCS 1973 raw record
        record = \
            "067310101131200000000031101000000000004700Y0320000010100" \
            "10000010000005000001347910111"
        # Field name physician_diagnosis
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS.value
        iterable_slice_object = [
            slice(38, 42, None), slice(42, 46, None), slice(46, 50, None)
        ]
        expected_field_codes = ['470.0', 'Y03.2', '']

        # Call to method
        actual_field_codes = process_multiple_slice_objects(
            record= record,
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
        expected_headers = \
            (
                'source_file_ID',
                'source_file_row',
                'sex',
                'physician_diagnosis',
                'patient_age',
                'month_of_visit',
                'year_of_visit',
            )
        expected_field_codes_for_record = \
            {
                'source_file_ID': '1973_NAMCS',
                'source_file_row': 1,
                'sex': 'Female',
                'physician_diagnosis': '470.0,Y03.2,',
                'patient_age': 22889,
                'month_of_visit': 'June',
                'year_of_visit': '1973'
            }

        # Converted field codes for single record which needs to be filtered
        # and modified
        field_codes_for_record = \
            {
                'source_file_ID': '1973_NAMCS',
                'source_file_row': 1,
                'sex': 'Female',
                'physician_diagnosis': '470.0,Y03.2,',
                'month_of_birth': 'October',
                'month_of_visit': 'June',
                'year_of_birth': '2010',
                'year_of_visit': '1973',
            }

        # Call to method
        actual_field_codes_for_record = \
            populate_missing_fields(
                headers = expected_headers,
                field_codes_for_single_record = field_codes_for_record
            )

        # Asserting if unnecessary fields are filtered and
        # required fields are populated
        self.assertDictEqual(
            expected_field_codes_for_record,actual_field_codes_for_record
        )

    @mock.patch('helpers.functions.os.rename')
    @mock.patch('helpers.functions.os.path.exists')
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
            os.path.join(functions.EXTRACTED_DATA_DIR_PATH, '2000_NAMCS')

        # Call to method
        actual_renamed_file_name = rename_namcs_dataset_for_year(year)

        # Asserting os.rename call
        mocked_os_rename.assert_called_with(
            os.path.join(functions.EXTRACTED_DATA_DIR_PATH, 'NAM00'),
            expected_renamed_file_name
        )

        # Assert for valid file name for year 2000
        self.assertEqual(expected_renamed_file_name, actual_renamed_file_name)
