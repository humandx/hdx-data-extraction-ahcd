# -*- coding: utf-8 -*-
"""
This script downloads and extracts the data files from all
the available public use NAMCS data.
More about NAMCS here:
http://www.cdc.gov/nchs/ahcd/about_ahcd.htm
"""
# Python modules
import os
import zipfile
from urllib import request

# Other modules
from helpers.functions import (
    get_customized_file_name,
    get_namcs_source_file_info,
    rename_namcs_dataset_for_year,
    get_namcs_datset_path_for_year
)
from namcs.config import (
    EXTRACTED_DATA_DIR_PATH,
    DOWNLOADED_FILES_DIR_PATH,
    log,
    YEARS_AVAILABLE,
)
from utils.context import try_except
from utils.decorators import catch_exception, create_path_if_does_not_exists


# 3rd party modules
# -N/A

# Global vars
# -N/A


@create_path_if_does_not_exists(DOWNLOADED_FILES_DIR_PATH)
def download_namcs_zipfile(namcs_year,
                           download_path=DOWNLOADED_FILES_DIR_PATH):
    """
    For a given year, download the zipped NAMCS data file into
    `download_path`.

    Parameters:
        namcs_year(:class:`int`): The year for which data is requested.
        download_path (:class:`str`): Download location for zip files,
            default value `DOWNLOADED_FILES_DIR_PATH`.
    Returns:
        :class `str`: Download zip file name for provided `year`
    """
    url = get_namcs_source_file_info(namcs_year).get("url")
    zip_file_name = \
        get_customized_file_name("NAMCS", "DATA", namcs_year, extension="zip")
    full_file_name = os.path.join(download_path, zip_file_name)
    log.info("Downloading file:{} for year:{}".format(url, namcs_year))

    # Enclosing block of code in try - except
    with try_except():
        request.urlretrieve(url, full_file_name)
    return full_file_name


@create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
def extract_data_zipfile(namcs_year, zip_file_name,
                         extract_path=EXTRACTED_DATA_DIR_PATH):
    """
    For a given year, extracts the NAMCS data zip file into `extract_path`

    Parameters:
        namcs_year(:class:`int`): The year for which data is requested.
        zip_file_name(:class:`str`):
            Downloaded zip file name for provided `year`.
        extract_path(:class:`str`): Extract location for zip files,
            default value `EXTRACTED_DATA_DIR_PATH`.
    """
    log.info("Extracting data for year: {}".format(namcs_year))
    if os.path.exists(zip_file_name):
        # Enclosing block of code in try - except
        with try_except(zipfile.BadZipfile, zipfile.LargeZipFile):
            file_handle = zipfile.ZipFile(zip_file_name)
            try:
                file_handle.extractall(extract_path)
            except Exception as exc:
                raise exc
            finally:
                file_handle.close()


@catch_exception()
def initiate_namcs_dataset_download(force_download=True):
    """
    Download and extract all the NAMCS dataset files available for public use
    in ftp.cdc.gov FTP server

    Parameters:
        force_download (:class:`bool`): Whether to force download
            NAMCS raw dataset file even if it exists,Default value True.
    """
    for year in YEARS_AVAILABLE:
        # Checking if raw NAMCS dataset file exists for year
        if get_namcs_datset_path_for_year(year) is None or force_download:
            # Download files for all the years
            full_file_name = download_namcs_zipfile(year)
            # Extract downloaded zipped file
            extract_data_zipfile(year, full_file_name)
            # Renaming NAMCS file
            rename_namcs_dataset_for_year(year)
