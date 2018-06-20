# -*- coding: utf-8 -*-
"""
Tests for namcs_converter module.
"""
# Python modules
import inspect
import os
from unittest import mock, TestCase

# Third party modules
# -N/A

# Other modules
from hdx_ahcd.controllers import namcs_converter
from hdx_ahcd.controllers.namcs_converter import (
    get_generator_by_year,
    get_year_wise_generator,
    export_to_csv,
)
from hdx_ahcd.helpers import functions
from hdx_ahcd.helpers.functions import get_namcs_source_file_info
from hdx_ahcd.namcs.config import YEARS_AVAILABLE


class NAMCSConverterTest(TestCase):
    """
    TestCase class for NAMCS converter.
    """

    def test_get_generator_by_year(self):
        """
        Test if valid generator object is returned by `get_generator_by_year`
        method.
        """
        # Setup
        year = 2000

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        generator_obj = get_generator_by_year(year)

        # Assert if the object returned is a generator
        self.assertTrue(inspect.isgenerator(generator_obj))

        # Assert rows count
        rows = [row for row in generator_obj]
        self.assertEqual(5, len(rows))

        # Assert rows by field details
        self.assertListEqual([
            {
                'age': 13140,
                'patient_visit_weight': 86790.0,
                'source_file_row': 1,
                'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 2190,
                'patient_visit_weight': 86790.0,
                'source_file_row': 2, 'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V20.20', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 20805,
                'patient_visit_weight': 86790.0,
                'source_file_row': 3, 'sex': 'Female',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V67.59', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 15695,
                'patient_visit_weight': 86790.0,
                'source_file_row': 4,
                'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
             },
            {
                'age': 13140,
                'patient_visit_weight': 86790.0,
                'source_file_row': 5, 'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            }
        ], rows)

    def test_get_generator_by_year_with_filename(self):
        """
        Test if valid generator object is returned by `get_generator_by_year`
        method.
        """
        # Setup
        year = 2000

        # Call to method
        generator_obj = get_generator_by_year(year, os.path.join(
            os.path.dirname(__file__), "data", "2000_NAMCS"))

        # Assert if the object returned is a generator
        self.assertTrue(inspect.isgenerator(generator_obj))

        # Assert rows count
        rows = [row for row in generator_obj]
        self.assertEqual(5, len(rows))

        # Assert rows by field details
        self.assertListEqual([
            {
                'age': 13140,
                'patient_visit_weight': 86790.0,
                'source_file_row': 1,
                'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 2190,
                'patient_visit_weight': 86790.0,
                'source_file_row': 2, 'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V20.20', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 20805,
                'patient_visit_weight': 86790.0,
                'source_file_row': 3, 'sex': 'Female',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V67.59', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 15695,
                'patient_visit_weight': 86790.0,
                'source_file_row': 4,
                'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 13140,
                'patient_visit_weight': 86790.0,
                'source_file_row': 5, 'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            }
        ], rows)

    @mock.patch("builtins.open")
    def test_export_to_csv(self, mocked_open):
        """
        Test if converted data is exported to a CSV file successfully.
        """
        # Setup
        year = 2000
        generator_object = (row for row in [
            {
                'age': 13140,
                'patient_visit_weight': 86790.0,
                'source_file_row': 1,
                'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 2190,
                'patient_visit_weight': 86790.0,
                'source_file_row': 2, 'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V20.20', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 20805,
                'patient_visit_weight': 86790.0,
                'source_file_row': 3, 'sex': 'Female',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V67.59', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 15695,
                'patient_visit_weight': 86790.0,
                'source_file_row': 4,
                'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            },
            {
                'age': 13140,
                'patient_visit_weight': 86790.0,
                'source_file_row': 5, 'sex': 'Male',
                'month_of_visit': 'September',
                'physician_diagnoses': ['V70.00', '', ''],
                'source_file_ID': '2000_NAMCS',
                'year_of_visit': '2000'
            }
        ])

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        namcs_converter.NAMCS_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        converted_file_path = export_to_csv(year, generator_object)

        # Assert return value
        self.assertEqual(
            os.path.join(
                os.path.dirname(__file__), "data", "2000_NAMCS_CONVERTED.csv"
            ),
            converted_file_path
        )

    def test_get_year_wise_generator_with_year(self):
        """
        Test if valid generator objects are returned by
        `get_year_wise_generator` method when a list of year is specified.
        """
        # Setup
        year = 2000

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = get_year_wise_generator(year)

        # Assert if the year wise dict has generator object
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2000).get("generator"))
        )

        # Assert if source file details are returned
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS00.exe',
                'year': '00',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS00.exe'
            },
            year_wise_mld.get(2000).get("source_file_info")
        )

    def test_get_year_wise_generator_with_year_and_file(self):
        """
        Test if valid generator objects are returned by
        `get_year_wise_generator` method when a list of year is specified.
        """
        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = get_year_wise_generator(
            year = 2000,
            namcs_raw_dataset_file =
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")
        )

        # Assert if the year wise dict has generator object
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2000).get("generator"))
        )

        # Assert if source file details are returned
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS00.exe',
                'year': '00',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS00.exe'
            },
            year_wise_mld.get(2000).get("source_file_info")
        )

    def test_get_year_wise_generator_for_multiple_year(self):
        """
        Test if valid generator objects are returned by
        `get_year_wise_generator` method when a list of year is specified.
        """
        # Setup
        years = (2000, 2001)

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = get_year_wise_generator(years)

        # Assert if the year wise dict has generator object
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2000).get("generator"))
        )
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2001).get("generator"))
        )

        # Assert if source file details are returned
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS00.exe',
                'year': '00',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS00.exe'
            },
            year_wise_mld.get(2000).get("source_file_info")
        )
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS01.exe',
                'year': '01',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS01.exe'
            },
            year_wise_mld.get(2001).get("source_file_info")
        )

    @mock.patch("hdx_ahcd.controllers.namcs_converter.export_to_csv")
    def test_get_year_wise_generator_for_year_with_export(self,
                                                          mocked_export_to_csv):
        """
        Test if valid generator objects are returned by
        `get_year_wise_generator` method when a list of year is specified.
        """
        # Setup
        years = (2000, 2001)

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = get_year_wise_generator(years, do_export=True)

        # Assert if the year wise dict has generator object
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2000).get("generator"))
        )
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2001).get("generator"))
        )

        # Assert if source file details are returned
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS00.exe',
                'year': '00',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS00.exe'
            },
            year_wise_mld.get(2000).get("source_file_info")
        )
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS01.exe',
                'year': '01',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS01.exe'
            },
            year_wise_mld.get(2001).get("source_file_info")
        )

        # Verify the `export_to_csv` call
        self.assertEqual(
            years,
            tuple([call[0][0] for call in mocked_export_to_csv.call_args_list])
        )
        self.assertTrue(all(
            [
                inspect.isgenerator(call[0][1])
                for call in mocked_export_to_csv.call_args_list
            ]
        ))

    def test_get_year_wise_generator_with_no_year(self):
        """
        Test if valid generator objects are returned by
        `get_year_wise_generator` method when a list of year is specified.
        """
        # Setup

        # Patch `EXTRACTED_DATA_DIR_PATH` to `test/data` directory
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = get_year_wise_generator()

        for year in YEARS_AVAILABLE:
            # Assert if the year wise dict has generator object
            self.assertTrue(
                inspect.isgenerator(year_wise_mld.get(2000).get("generator"))
            )
            # Assert if source file details are returned
            self.assertEqual(
                get_namcs_source_file_info(year),
                year_wise_mld.get(year).get("source_file_info")
            )
