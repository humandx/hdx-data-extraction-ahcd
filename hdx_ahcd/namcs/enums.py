# -*- coding: utf-8 -*-
"""
Module for enums used by NAMCS-NAHMCS extractor
"""
# Python modules
from enum import Enum

# Other modules
# - N/A

# 3rd party modules
# - N/A

# Global vars
# -N/A


class NAMCSFieldEnum(Enum):
    """
    Enums for defining field names for NAMCS dataset.

    Note:
        Implicitly represent key for creating a dict row in
        `NAMCS.general.translate_namcs_dataset_file`.
    """
    SOURCE_FILE_ID = "source_file_ID"
    SOURCE_FILE_ROW = "source_file_row"
    DATE_OF_VISIT = "date_of_visit"
    DATE_OF_BIRTH = "date_of_birth"
    YEAR_OF_VISIT = "year_of_visit"
    YEAR_OF_BIRTH = "year_of_birth"
    MONTH_OF_VISIT = "month_of_visit"
    MONTH_OF_BIRTH = "month_of_birth"
    PATIENT_AGE = "age"
    GENDER = "sex"
    PHYSICIANS_DIAGNOSIS = "physician_diagnosis"
    PHYSICIANS_DIAGNOSIS_1 = PHYSICIANS_DIAGNOSIS  # "physician_diagnosis_1"
    PHYSICIANS_DIAGNOSIS_2 = PHYSICIANS_DIAGNOSIS  # "physician_diagnosis_2"
    PHYSICIANS_DIAGNOSIS_3 = PHYSICIANS_DIAGNOSIS  # "physician_diagnosis_3"
    PHYSICIANS_DIAGNOSIS_4 = PHYSICIANS_DIAGNOSIS  # "physician_diagnosis_4"
    PHYSICIANS_DIAGNOSIS_5 = PHYSICIANS_DIAGNOSIS  # "physician_diagnosis_5"


class GenderEnum(Enum):
    """
    Enums for gender.
    """
    FEMALE = "Female"
    MALE = "Male"
