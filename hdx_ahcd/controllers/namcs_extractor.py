# -*- coding: utf-8 -*-
"""
Module to download(s) and extract(s) dataset file(s) from NAMCS public files
CDC server
More about NAMCS here:
http://www.cdc.gov/nchs/hdx_ahcd/about_ahcd.html
"""
# Python modules
from urllib import request
import os
import zipfile

# Other modules
from hdx_ahcd.helpers.functions import (
    get_customized_file_name,
    get_iterable,
    get_namcs_source_file_info,
    get_namcs_dataset_path_for_year,
    rename_namcs_dataset_for_year,
)
from hdx_ahcd.namcs.config import (
    EXTRACTED_DATA_DIR_PATH,
    DOWNLOADED_FILES_DIR_PATH,
    log,
    YEARS_AVAILABLE,
)
from hdx_ahcd.utils.context import try_except
from hdx_ahcd.utils.decorators import (
    catch_exception,
    create_path_if_does_not_exists
)
from hdx_ahcd.utils.utils import detailed_exception_info

# 3rd party modules
# -N/A

# Global vars
# -N/A


@create_path_if_does_not_exists(DOWNLOADED_FILES_DIR_PATH)
def download_namcs_zipfile(namcs_year, download_path=DOWNLOADED_FILES_DIR_PATH):
    """
    For a given year, download the zipped NAMCS data file into
    `download_path` from public CDC server.

    Parameters:
        namcs_year (:class:`int`): Year for which NAMCS dataset file will
            be downloaded from public CDC server.
        download_path (:class:`str`): Download location path for downloaded
            zip files.

    Returns:
        :class:`str`: Downloaded zipped dataset file path for `year`.

    Note:
        >>> from hdx_ahcd.namcs.config import DOWNLOADED_FILES_DIR_PATH
        >>> DOWNLOADED_FILES_DIR_PATH
        "~/.hdx_ahcd/data/downloaded_files"
    """
    url = get_namcs_source_file_info(namcs_year).get("url")
    zip_file_name = \
        get_customized_file_name("NAMCS", "DATA", namcs_year, extension="zip")
    full_file_name = os.path.join(download_path, zip_file_name)
    log.info("Downloading file: {} for year: {}".format(url, namcs_year))

    # Handle exception in call to :func:`urlretrieve`
    with try_except():
        request.urlretrieve(url, full_file_name)
    return full_file_name


@create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
def extract_data_zipfile(year, zip_file_name,
                         extract_path=EXTRACTED_DATA_DIR_PATH):
    """
    For a given `year`, extract the NAMCS data set zip file in path
    `extract_path`.

    Parameters:
        year (:class:`int`): Year for which downloaded zipped dataset file will
            be extracted.
        zip_file_name (:class:`str`): Downloaded zipped dataset file path for
            `year`.
        extract_path (:class:`str`): Extract path where zip files will be
            extracted.

    Note:
        >>> from hdx_ahcd.namcs.config import EXTRACTED_DATA_DIR_PATH
        >>> EXTRACTED_DATA_DIR_PATH
        "~/.hdx_ahcd/data/extracted_data"
    """
    log.debug("Extracting data for year: {}".format(year))
    if os.path.exists(zip_file_name):
        # Handle exception in call to :func:`zipfile.ZipFile`
        with try_except(zipfile.BadZipfile, zipfile.LargeZipFile):
            file_handle = zipfile.ZipFile(zip_file_name)
            try:
                file_handle.extractall(extract_path)
            except Exception as exc:
                detailed_exception_info()
                raise exc
            finally:
                file_handle.close()


@catch_exception(re_raise=True)
def delete_namcs_zipfile(year, download_path=DOWNLOADED_FILES_DIR_PATH):
    """
    For a given `year`, delete the downloaded zipped NAMCS data set file.

    Parameters:
        year (:class:`int`): Year for which downloaded zipped dataset file will
            be deleted.
        download_path (:class:`str`): Downloaded zipped dataset file path for
            `year`.
    """
    zip_file_name = \
        get_customized_file_name("NAMCS", "DATA", year, extension="zip")
    full_file_name = os.path.join(download_path, zip_file_name)

    if not os.path.exists(full_file_name):
        raise Exception("Zip file for year: {} ,does not"
                        "exists at: {}".format(year, download_path))

    with try_except():
        log.debug("Deleting zip file: {} for"
                  "year: {}".format(full_file_name, year))
        os.remove(full_file_name)


@catch_exception()
def initiate_namcs_dataset_download(year=None,
                                    force_download = False,
                                    extract_path = EXTRACTED_DATA_DIR_PATH,
                                    download_path = DOWNLOADED_FILES_DIR_PATH):
    """
    Download and extract all the NAMCS dataset files available for public use
    in ftp.cdc.gov FTP server.

    Parameters:
        year(:class:`int` or :class:`list` or :class:`tuple`): Year(s) for
            which dataset files will be downloaded and extracted.
        force_download (:class:`bool`): Whether to force download
            NAMCS raw dataset file even if data set file exists locally.
            *Default** :const:`False`.
        extract_path(:class:`str`): Extract path where zip files will be
            extracted.
        download_path (:class:`str`): Downloaded zipped dataset file path for
            `year`.
    Note:
        >>> from hdx_ahcd.namcs.config import YEARS_AVAILABLE
        >>> YEARS_AVAILABLE
        [1973, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1985, 1989, 1990, 1992,
        1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
        2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
    """
    year = YEARS_AVAILABLE if year is None else get_iterable(year)

    # Download files for all the `year`
    # Using integer value for `year`
    for _year in map(int, year):
        # Checking if NAMCS dataset file already exists in the
        # `EXTRACTED_DATA_DIR_PATH`
        if get_namcs_dataset_path_for_year(_year) is None or force_download:
            # Download files for `_year`
            full_file_name = \
                download_namcs_zipfile(_year, download_path=download_path)
            # Extract downloaded zipped file
            extract_data_zipfile(
                _year, full_file_name, extract_path=extract_path
            )
            # Rename NAMCS file
            rename_namcs_dataset_for_year(_year)
            # Delete downloaded zip file.
            delete_namcs_zipfile(_year, download_path=download_path)
