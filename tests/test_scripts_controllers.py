# -*- coding: utf-8 -*-
"""
Tests for hdx_ahcd controller module.
"""
# Python modules
import inspect
import os
from unittest import TestCase, mock

# Third party modules
# -N/A

# Other modules
from hdx_ahcd.helpers import functions
from hdx_ahcd.helpers.functions import get_namcs_source_file_info
from hdx_ahcd.namcs.config import YEARS_AVAILABLE
from hdx_ahcd.scripts.controllers import NAMCSController


class ControllersTest(TestCase):
    """
    TestCase class for NAMCS controller.
    """
    def setUp(self):
        """
        Override of :func:`setUp` implementation
        """
        self.controller = NAMCSController()

    def test_execute_with_year_and_filename(self):
        """
        Test if `execute` method is working as expected.
        (Case: When Year and filename is specified.)
        """
        # Setup
        year = 2000
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = self.controller.execute(year, test_file_path)

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

    def test_execute_with_filename(self):
        """
        Test if `execute` method is working as expected.
        (Case: When filename is specified.)
        """
        # Setup
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = self.controller.execute(file_name=test_file_path)

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

    def test_execute_with_year(self):
        """
        Test if `execute` method is working as expected.
        (Case: When Year is specified.)
        """
        # Setup
        year = 2000
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = self.controller.execute(year)

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

    def test_execute_with_years(self):
        """
        Test if `execute` method is working as expected.
        (Case: When Year is specified.)
        """
        # Setup
        year = [2000, 2001]
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = self.controller.execute(year=year)

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

    @mock.patch("hdx_ahcd.scripts.controllers.download_namcs_zipfile")
    @mock.patch("hdx_ahcd.scripts.controllers.extract_data_zipfile")
    @mock.patch("hdx_ahcd.scripts.controllers.rename_namcs_dataset_for_year")
    def test_execute_with_years_when_file_not_already_exists(
            self,
            mocked_download_namcs_zipfile,
            mocked_extract_data_zipfile,
            mocked_rename_namcs_file
    ):
        """
        Test if `execute` method is working as expected.
        (Case: When Year is specified.)
        """
        # Setup
        year = [2002, 2003]
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = self.controller.execute(year=year)

        # Assert if the year wise dict has generator object
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2002).get("generator"))
        )
        self.assertTrue(
            inspect.isgenerator(year_wise_mld.get(2003).get("generator"))
        )

        # Assert if source file details are returned
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS02.exe',
                'year': '02',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS02.exe'
             },
            year_wise_mld.get(2002).get("source_file_info")
        )
        self.assertEqual(
            {
                'zip_file_name': 'NAMCS03.exe',
                'year': '03',
                'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/'
                       'NAMCS/NAMCS03.exe'
             },
            year_wise_mld.get(2003).get("source_file_info")
        )

    @mock.patch("hdx_ahcd.scripts.controllers.initiate_namcs_dataset_download")
    def test_execute_without_year_and_filename(
            self, mocked_initiate_namcs_dataset_download
    ):
        """
        Test if `execute` method is working as expected.
        (Case: When neither year nor filename is specified.)
        """
        # Setup
        functions.EXTRACTED_DATA_DIR_PATH = \
            os.path.join(os.path.dirname(__file__), "data")

        # Call to method
        year_wise_mld = self.controller.execute()

        # Assert if source file details are returned
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

    def test_validate(self):
        """
        Test if `validate` method is working as expected.
        """
        # Setup
        year = 2000
        test_file_path = \
            os.path.join(os.path.dirname(__file__), "data", "2000_NAMCS")

        # Call to method
        is_valid = self.controller.validate(year, test_file_path)

        # Assert returned generator
        self.assertTrue(is_valid)
