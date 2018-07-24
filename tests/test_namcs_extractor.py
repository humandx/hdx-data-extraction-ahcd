# -*- coding: utf-8 -*-
"""
Tests for module `namcs_extractor`.
"""
# Python modules
from unittest import mock, TestCase
import os

# Third party modules
# -N/A

# Other modules
from hdx_ahcd.controllers.namcs_extractor import (
    download_namcs_zipfile,
    extract_data_zipfile,
    initiate_namcs_dataset_download,
    delete_namcs_zipfile
)
from hdx_ahcd.helpers.functions import get_iterable
from hdx_ahcd.namcs import config
from hdx_ahcd.namcs.config import YEARS_AVAILABLE


class NAMCSExtractorTest(TestCase):
    """
    TestCase class for NAMCS extractor.
    """
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.download_namcs_zipfile")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.extract_data_zipfile")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.delete_namcs_zipfile")
    def test_initiate_namcs_dataset_download(
        self,
        mocked_delete_namcs_zipfile,
        mocked_extract_data_zipfile,
        mocked_download_namcs_zipfile,
    ):
        """
        Test if download and extraction of NAMCS public files is successful.
        """
        # Setup
        download_namcs_zipfile_mocked_return = "path-to-downloaded-file.zip"

        # Patch `EXTRACTED_DATA_DIR_PATH`
        config.DOWNLOADED_FILES_DIR_PATH = "/tmp/namcs_downloaded_files"
        config.EXTRACTED_DATA_DIR_PATH = "/tmp/namcs_extracted_files"

        # Mocking return value of `download_namcs_zipfile` call
        mocked_download_namcs_zipfile.return_value = \
            download_namcs_zipfile_mocked_return

        # Call to func :func:`initiate_namcs_dataset_download`
        initiate_namcs_dataset_download(force_download=True)

        # Assert :func:`download_namcs_zipfile` calls
        self.assertEqual(
            YEARS_AVAILABLE,
            [
                call[0][0]
                for call in mocked_download_namcs_zipfile.call_args_list
            ]
        )

        # Assert :func:`extract_data_zipfile` calls
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

    @mock.patch("hdx_ahcd.controllers.namcs_extractor.download_namcs_zipfile")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.extract_data_zipfile")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.delete_namcs_zipfile")
    def test_initiate_namcs_dataset_download_with_year(
        self,
        mocked_delete_namcs_zipfile,
        mocked_extract_data_zipfile,
        mocked_download_namcs_zipfile
    ):
        """
        Test if download and extraction of NAMCS public files is successful
        when `year` is provided.
        """
        # Setup
        download_namcs_zipfile_mocked_return = "path-to-downloaded-file.zip"

        # Patch `EXTRACTED_DATA_DIR_PATH`
        config.DOWNLOADED_FILES_DIR_PATH = "/tmp/namcs_downloaded_files"
        config.EXTRACTED_DATA_DIR_PATH = "/tmp/namcs_extracted_files"

        # Mocking return value of `download_namcs_zipfile` call
        mocked_download_namcs_zipfile.return_value = \
            download_namcs_zipfile_mocked_return

        # Case 1: when year is 2000
        # Setup
        year = 2000
        # Call to func :func:`initiate_namcs_dataset_download`
        initiate_namcs_dataset_download(year=year, force_download=True)

        # Assert `download_namcs_zipfile` calls
        self.assertEqual(
            get_iterable(year),
            [
                call[0][0]
                for call in mocked_download_namcs_zipfile.call_args_list
            ]
        )

        # Assert :func:`extract_data_zipfile` calls
        self.assertEqual(
            [
                (year, download_namcs_zipfile_mocked_return)
            ],
            [
                call[0]  # Accessing tuple directly here
                for call in mocked_extract_data_zipfile.call_args_list
            ]
        )

    @mock.patch("hdx_ahcd.controllers.namcs_extractor.download_namcs_zipfile")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.extract_data_zipfile")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.delete_namcs_zipfile")
    def test_initiate_namcs_dataset_download_with_multiple_years(
        self,
        mocked_delete_namcs_zipfile,
        mocked_extract_data_zipfile,
        mocked_download_namcs_zipfile
    ):
        """
        Test if download and extraction of NAMCS public files is successful
        when multiple `year` is provided.
        """
        # Setup
        download_namcs_zipfile_mocked_return = "path-to-downloaded-file.zip"

        # Patch `EXTRACTED_DATA_DIR_PATH`
        config.DOWNLOADED_FILES_DIR_PATH = "/tmp/namcs_downloaded_files"
        config.EXTRACTED_DATA_DIR_PATH = "/tmp/namcs_extracted_files"

        # Mocking return value of `download_namcs_zipfile` call
        mocked_download_namcs_zipfile.return_value = \
            download_namcs_zipfile_mocked_return

        # Case 1: when year = (2000, 2001)
        # Setup
        year = (2000, 2001)
        # Call to func :func:`initiate_namcs_dataset_download`
        initiate_namcs_dataset_download(year=year, force_download=True)

        # Assert :func:`download_namcs_zipfile` calls
        self.assertEqual(
            list(year),
            [
                call[0][0]
                for call in mocked_download_namcs_zipfile.call_args_list
            ]
        )

        # Assert :func:`extract_data_zipfile` calls
        self.assertEqual(
            [
                (_year, download_namcs_zipfile_mocked_return)
                for _year in year
            ],
            [
                call[0]  # Accessing tuple directly here
                for call in mocked_extract_data_zipfile.call_args_list
            ]
        )

    @mock.patch("hdx_ahcd.controllers.namcs_extractor.request.urlretrieve")
    def test_download_namcs_zipfile(self, mocked_urlretrieve):
        """
        Test if download NAMCS public file is successful.
        """
        # Setup
        namcs_year, download_path = 2000, "/tmp/namcs_downloaded_files"
        expected_filename = \
            "/tmp/namcs_downloaded_files/NAMCS_DATA_2000.zip"

        # Call to func :func:`download_namcs_zipfile`
        actual_filename = download_namcs_zipfile(namcs_year, download_path)

        # Assert :func:`urlretrieve` call
        urlretrieve_expected_args = (
            "ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/"
            "NAMCS00.exe",
            expected_filename
        )
        mocked_urlretrieve.assert_called_with(*urlretrieve_expected_args)

        # Assert :func:`download_namcs_zipfile` return value
        self.assertEqual(expected_filename, actual_filename)

    @mock.patch("hdx_ahcd.controllers.namcs_extractor.zipfile.ZipFile")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.os")
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

        # Call to func :func:`extract_data_zipfile`
        extract_data_zipfile(namcs_year, zip_file_name, extract_path)

        # Assert :class:`zipfile.ZipFile` call args
        mocked_zipfile.assert_called_with(zip_file_name)
        mocked_zipfile.return_value.extractall.assert_called_with(extract_path)

    @mock.patch("hdx_ahcd.controllers.namcs_extractor.os.remove")
    @mock.patch("hdx_ahcd.controllers.namcs_extractor.os.path.exists")
    def test_delete_namcs_zipfile(self, mocked_path_exists, mocked_os_remove):
        """
        Test to validate deletion of downloaded zip files.
        """
        # Setup
        year = 2000
        download_path = "/tmp/namcs_downloaded_files"

        zip_file_name = "NAMCS_DATA_2000.zip"

        # Mocking `os.path.exists` return value
        mocked_path_exists.return_value = True

        # Call to func :func:`delete_namcs_zipfile`
        delete_namcs_zipfile(year, download_path)

        # Asserting :func:`os.remove` call
        mocked_os_remove.assert_called_with(
            os.path.join(download_path, zip_file_name)
        )
