# -*- coding: utf-8 -*-
"""
This file contains all configurable data,
Each entity in this file represents a necessary yet configurable details.
"""
# Python modules
import logging
import os

# Other modules
from hdx_ahcd.namcs.enums import NAMCSFieldEnum
from hdx_ahcd.utils.utils import RangeDict

# 3rd party modules
# -N/A

# Output file name
SOURCE_FILES_INFO_CSV_FILE_NAME = "SOURCE_FILES_INFO.csv"

# Converted csv file name suffix
CONVERTED_CSV_FILE_NAME_SUFFIX = "CONVERTED"

# All required columns in converted csv file are represented by
# `CONVERTED_CSV_FIELDS`
CONVERTED_CSV_FIELDS = (
    NAMCSFieldEnum.SOURCE_FILE_ID.value,
    NAMCSFieldEnum.SOURCE_FILE_ROW.value,
    NAMCSFieldEnum.MONTH_OF_VISIT.value,
    NAMCSFieldEnum.YEAR_OF_VISIT.value,
    NAMCSFieldEnum.GENDER.value,
    NAMCSFieldEnum.PATIENT_AGE.value,
    NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS.value
    # NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value,
    # NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value,
    # NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
)

# Path to NAMCS project root directory
NAMCS_ROOT_PATH = \
    os.path.realpath(os.path.join(os.path.expanduser("~"), ".hdx_ahcd"))

# NAMCS data files directory path
NAMCS_DATA_DIR_PATH = os.path.join(NAMCS_ROOT_PATH, "data")

# Directory path where data sets files are downloaded from FTP server
DOWNLOADED_FILES_DIR_PATH = \
    os.path.join(NAMCS_DATA_DIR_PATH, "downloaded_files")

# Directory path where downloaded data sets files are extracted
EXTRACTED_DATA_DIR_PATH = \
    os.path.join(NAMCS_DATA_DIR_PATH, "extracted_data")

# Directory path for error files
ERROR_FILES_DIR_PATH = \
    os.path.join(NAMCS_DATA_DIR_PATH, "errors")

# Dataset pattern to extract year from NAMCS record
NAMCS_DATASET_YEAR_PATTERNS = ("%y", "%Y")

# Dataset pattern to extract month from NAMCS record
NAMCS_DATASET_MONTH_PATTERNS = ("%m", "%b", "%B")

# Creating "hdx_ahcd" as logger.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("hdx_ahcd")

# Defining Range dicts to make sure we can query the proper url for a given year
BASE_FILE_NAME = RangeDict(
    {
        (1973, 1999): "namcs",  # plus last 2 digits of the year
        (2000, 2009): "NAMCS",  # plus last 2 digits of the year
        (2010, 2015): "namcs20"  # plus last 2 digits of the year
    }
)

NAMCS_FILE_NAME = RangeDict(
    {
        (1973, 2009): ["NAMCS", "NAM"],  # plus last 2 digits of the year
        2010: ["NAMCS20"],
        (2011, 2015): ["namcs20"]  # plus last 2 digits of the year
    }
)

# Create a list of years for which data is available
YEARS_MISSING = (1974, 1982, 1983, 1984, 1986, 1987, 1988, 1991)
YEARS_AVAILABLE = \
    [year for year in range(1973, 2016) if year not in YEARS_MISSING]

# NAMCS public files FTP url by year
FTP_URL_TO_1973_1992_PUBLIC_FILES = \
    "ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/"
FTP_URL_TO_1993_2015_PUBLIC_FILES =\
    "ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/"
NAMCS_PUBLIC_FILE_URL = \
    RangeDict(
        {
            (1973, 1992): FTP_URL_TO_1973_1992_PUBLIC_FILES,
            (1993, 2015): FTP_URL_TO_1993_2015_PUBLIC_FILES
        }
    )

# File extensions for NAMCS public files by year
NAMCS_PUBLIC_FILE_EXTENSIONS = RangeDict(
    {
        (1973, 2010): ".exe",
        2011: ".zip",
        2012: ".exe",
        (2013, 2015): ".zip"
    }
)

# NAMCS public files record length by year
# Note: Do not consider newline character(\n) in this count.
NAMCS_PUBLIC_FILE_RECORD_LENGTH_BY_YEAR = RangeDict(
    {
        (1973, 1976): 92,
        (1977, 1978): 90,
        1979: 99,
        (1980, 1981): 143,
        1985: 146,
        (1989, 1990): 153,
        1992: 355,
        (1993, 1996): 542,
        (1997, 2000): 663,
        2001: 679,
        2002: 741,
        (2003, 2004): 792,
        2005: 778,
        2006: 905,
        (2007, 2008): 997,
        2009: 980,
        2010: 1065,
        2011: 1064,
        2012: 1414,
        2013: 1394,
        2014: 2754,
        2015: 2713,
    }
)
