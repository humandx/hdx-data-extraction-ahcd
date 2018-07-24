# -*- coding: utf-8 -*-
"""
Module that defines enums used in package hdx_ahcd.
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
        Implicitly represent key while creating a translated record in
        `hdx_ahcd.controllers.namcs_converter.get_generator_by_year`.
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
    VISIT_WEIGHT = "patient_visit_weight"
    PHYSICIANS_DIAGNOSES = "physician_diagnoses"
    PHYSICIANS_DIAGNOSES_1 = PHYSICIANS_DIAGNOSES  # "physician_diagnoses_1"
    PHYSICIANS_DIAGNOSES_2 = PHYSICIANS_DIAGNOSES  # "physician_diagnoses_2"
    PHYSICIANS_DIAGNOSES_3 = PHYSICIANS_DIAGNOSES  # "physician_diagnoses_3"
    PHYSICIANS_DIAGNOSES_4 = PHYSICIANS_DIAGNOSES  # "physician_diagnoses_4"
    PHYSICIANS_DIAGNOSES_5 = PHYSICIANS_DIAGNOSES  # "physician_diagnoses_5"


class NAMCSErrorFieldEnum(Enum):
    """
    Enums for defining header names for NAMCS dataset error file.
    """
    RECORD_NUMBER = "record_no"
    RECORD = "record"
    EXCEPTION = "exception"


class GenderEnum(Enum):
    """
    Enums for defining values for gender.
    """
    FEMALE = "Female"
    MALE = "Male"


class PhysicianDiagnosesEnum(Enum):
    """
    As per mentioned in Note section ,the documentation for NAMCS dataset files
    define certain codes with predefined meaning.
    This Enum that defines values for these specific physician diagnoses codes.

    Note:
        Specific physician diagnoses codes:
        - "V9910": "Left before being seen"
        - "209910": "Left before being seen"
        - "V9920": "Transferred to another facility"
        - "209920": "Transferred to another facility"
        - "209930": "HMO will not authorize treatment"

    """
    LEFT_BEFORE_BEING_SEEN = "AHCD.LBBS"  # Code: "V9910", "209910"
    TRANSFER_TO_ANOTHER_FACILITY = "AHCD.TTAF"  # Code: "V9920", "209920"
    HMO_WILL_NOT_AUTHORIZE_TREATMENT = "AHCD.HNAT"  # Code: "209930"
