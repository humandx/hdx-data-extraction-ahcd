# -*- coding: utf-8 -*-
"""
Module to download(s) and extract(s) dataset file(s) from NAMCS public files
CDC server
More about NAMCS here:
http://www.cdc.gov/nchs/hdx_ahcd/about_ahcd.html
"""
# Python modules
import os
import zipfile
from urllib import request

# Other modules
from hdx_ahcd.helpers.functions import (
    get_customized_file_name,
    get_namcs_source_file_info,
    rename_namcs_dataset_for_year,
    get_namcs_dataset_path_for_year,
    get_iterable
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
    `download_path`.

    Parameters:
        namcs_year(:class:`int`): NAMCS year.
        download_path (:class:`str`): Download location for zip files.

    Returns:
        :class `str`: Download zip file name for provided `year`.

    Note:
        >>> from namcs.config import DOWNLOADED_FILES_DIR_PATH
        >>> DOWNLOADED_FILES_DIR_PATH
        '~/.hdx_ahcd/data/downloaded_files'
    """
    url = get_namcs_source_file_info(namcs_year).get("url")
    zip_file_name = \
        get_customized_file_name("NAMCS", "DATA", namcs_year, extension="zip")
    full_file_name = os.path.join(download_path, zip_file_name)
    log.info("Downloading file:{} for year:{}".format(url, namcs_year))

    # Handling any exception that might occur in :func:`urlretrieve`
    with try_except():
        request.urlretrieve(url, full_file_name)
    return full_file_name


@create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
def extract_data_zipfile(namcs_year, zip_file_name,
                         extract_path=EXTRACTED_DATA_DIR_PATH):
    """
    For a given year, extracts the NAMCS data zip file into `extract_path`.

    Parameters:
        namcs_year(:class:`int`): NAMCS year.
        zip_file_name(:class:`str`):
            Downloaded zip file name for provided `year`.
        extract_path(:class:`str`): Extract location for zip files.

    Note:
        >>> from namcs.config import EXTRACTED_DATA_DIR_PATH
        >>> EXTRACTED_DATA_DIR_PATH
        '~/.hdx_ahcd/data/extracted_data'
    """
    log.debug("Extracting data for year: {}".format(namcs_year))
    if os.path.exists(zip_file_name):
        # Enclosing block of code in try - except
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
def delete_namcs_zipfile(namcs_year, download_path=DOWNLOADED_FILES_DIR_PATH):
    """
    For a given year, delete the zipped NAMCS data set file.

    Parameters:
        namcs_year(:class:`int`): NAMCS year.
        download_path (:class:`str`): Download location for zip files.
    """
    zip_file_name = \
        get_customized_file_name("NAMCS", "DATA", namcs_year, extension="zip")
    full_file_name = os.path.join(download_path, zip_file_name)

    if not os.path.exists(full_file_name):
        raise Exception('Zip file for year:{} ,does not'
                        'exists at {}'.format(namcs_year, download_path))

    with try_except():
        log.debug("Deleting zip file:{} for "
                  "year:{}".format(full_file_name, namcs_year))
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
        year(:class:`int` or :class:`list` or :class:`tuple`): NAMCS year(s).
        force_download (:class:`bool`): Whether to force download
            NAMCS raw dataset file even if data set file exists.
            *Default** :const:`False`.
        extract_path(:class:`str`): Extract location for zip files.
        download_path (:class:`str`): Download location for zip files.
    Note:
        >>> from namcs.config import YEARS_AVAILABLE
        >>> YEARS_AVAILABLE
        [1973, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1985, 1989, 1990, 1992,
        1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
        2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
    """
    year = YEARS_AVAILABLE if year is None else get_iterable(year)

    # Download files for all the `year`
    for _year in year:
        # Checking if NAMCS dataset file already exists in the
        # `EXTRACTED_DATA_DIR_PATH`
        if get_namcs_dataset_path_for_year(_year) is None or force_download:
            # Download files for `_year`
            full_file_name = \
                download_namcs_zipfile(_year, download_path=download_path)
            # Extract downloaded zipped file
            extract_data_zipfile(_year, full_file_name,
                                 extract_path = extract_path)
            # Rename NAMCS file
            rename_namcs_dataset_for_year(_year)
            # Delete downloaded zip file.
            delete_namcs_zipfile(_year, download_path=download_path)
