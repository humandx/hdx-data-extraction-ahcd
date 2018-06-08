# -*- coding: utf-8 -*-
"""
Tests for namcs_extractor module.
"""
# Python modules
from unittest import mock, TestCase

# Third party modules
# -N/A

# Other modules
from namcs.general.namcs_extractor import (
    download_namcs_zipfile,
    extract_data_zipfile,
    initiate_namcs_dataset_download,
)
from namcs.namcs.config import YEARS_AVAILABLE


class NAMCSExtractorTest(TestCase):
    """
    TestCase class for NAMCS extractor.
    """
    @mock.patch("general.namcs_extractor.download_namcs_zipfile")
    @mock.patch("general.namcs_extractor.extract_data_zipfile")
    def test_initiate_namcs_dataset_download(self, mocked_extract_data_zipfile,
                                             mocked_download_namcs_zipfile):
        """
        Test if download and extraction of NAMCS public files is successful.
        """
        # Setup
        download_namcs_zipfile_mocked_return = "path-to-downloaded-file.zip"

        # Mocking return value of `download_namcs_zipfile` call
        mocked_download_namcs_zipfile.return_value = \
            download_namcs_zipfile_mocked_return

        # Call to method
        initiate_namcs_dataset_download()

        # Assert `download_namcs_zipfile` calls
        self.assertEqual(
            YEARS_AVAILABLE,
            [
                call[0][0]
                for call in mocked_download_namcs_zipfile.call_args_list
            ]
        )

        # Assert `extract_data_zipfile` calls
        self.assertEqual(
            [
                (year, download_namcs_zipfile_mocked_return)
                for year in YEARS_AVAILABLE
            ],
            [
                call[0]  # Accessing tuple directly here
                for call in mocked_extract_data_zipfile.call_args_list
            ]
        )

    @mock.patch("general.namcs_extractor.request.urlretrieve")
    def test_download_namcs_zipfile(self, mocked_urlretrieve):
        """
        Test if download NAMCS public file is successful.
        """
        # Setup
        namcs_year, download_path = 2000, "/tmp/namcs_downloaded_files"
        expected_filename = \
            '/tmp/namcs_downloaded_files/NAMCS_DATA_2000.zip'

        # Call to method
        actual_filename = download_namcs_zipfile(namcs_year, download_path)

        # Assert `urlretrieve` call
        urlretrieve_expected_args = (
            'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/'
            'NAMCS00.exe',
            expected_filename
        )
        mocked_urlretrieve.assert_called_with(*urlretrieve_expected_args)

        # Assert `download_namcs_zipfile` return value
        self.assertEqual(expected_filename, actual_filename)

    @mock.patch("general.namcs_extractor.zipfile.ZipFile")
    @mock.patch("general.namcs_extractor.os")
    def test_extract_data_zipfile(self, mocked_os, mocked_zipfile):
        """
        Test if extraction of downloaded NAMCS public file is successful.
        """
        # Setup
        namcs_year, zip_file_name, extract_path = \
            2000, "/tmp/namcs_downloaded_files/NAMCS_DATA_2000.zip", \
            "/tmp/namcs_extracted_files"

        # Mocking `os.path.exists` return value
        mocked_os.return_value = True

        # Call to method
        extract_data_zipfile(namcs_year, zip_file_name, extract_path)

        # Assert :class:`zipfile.ZipFile` call args
        mocked_zipfile.assert_called_with(zip_file_name)
        mocked_zipfile.return_value.extractall.assert_called_with(extract_path)
