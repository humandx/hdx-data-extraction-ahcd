# -*- coding: utf-8 -*-
"""
Module containing methods to evaluate fields in data set file and convert them
in respective human readable format.
"""
# Python modules
from datetime import datetime

# 3rd party modules
# -N/A

# Other modules
from hdx_ahcd.namcs.config import (
    NAMCS_DATASET_MONTH_PATTERNS,
    NAMCS_DATASET_YEAR_PATTERNS,
)
from hdx_ahcd.namcs.constants import ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS
from hdx_ahcd.utils.decorators import enforce_type
from hdx_ahcd.utils.decorators import (
    add_method_to_mapping_dict,
    catch_exception
)
from hdx_ahcd.namcs.enums import (
    GenderEnum,
    NAMCSFieldEnum,
)

# Global vars
REGEX_FOR_GENDER = "^[1|2]$"
REGEX_FOR_MONTH = "^((0[1-9]|1[012])|([A-Z][a-z]{2,8}))$"
REGEX_FOR_PATIENT_AGE = "^[0|1]{0,1}[0-9]{1,2}$"
REGEX_FOR_PATIENT_VISIT_WEIGHT = "^(([0-9.]{5,6})|([0-9.]{10,11}))$"
REGEX_FOR_PHYSICIAN_DIAGNOSES = \
    "^([V|Y|\-|\&|0-9][0-9]{3,5}|[V|0-9]{1}[0-9]{2}[\-|0-9]{1,2})$"
REGEX_FOR_YEAR = "^([1-2][0|9])?[0-9]{2}$"
REGEX_FOR_YEAR_AND_MONTH = "^(0[1-9]|1[012])([0-9]{2})$"


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.DATE_OF_VISIT.value,
            NAMCSFieldEnum.DATE_OF_BIRTH.value
    )
)
@enforce_type(str, return_type=(int, int), use_regex=REGEX_FOR_YEAR_AND_MONTH)
def get_year_and_month_from_date(raw_format_date):
    """
    Fetch year and month from provided date string.

    Parameters:
        raw_format_date (:class:`str`): Date string in format MMYY.

    Returns:
        :class:`tuple`: With elements as:
            :class:`int`: Numeric value of year.
            :class:`int`: Numeric value of month.
    """
    date = datetime.strptime(raw_format_date, "%m%y")

    # Get string representation of date for year and month
    year = int(date.strftime("%Y"))
    month = int(date.strftime("%m"))
    return year, month


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_1.value,
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_2.value,
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_3.value,
    )
)
@enforce_type(str, return_type=str, use_regex=REGEX_FOR_PHYSICIAN_DIAGNOSES)
def convert_physician_diagnoses_code(diagnoses_code):
    """
    Method to get convert raw `diagnoses_code` into ICD-9 format.

    Parameters:
        diagnoses_code (:class:`str`): String representation of diagnosis_code.

    Returns:
        :class:`str`: Mapped representation of corresponding ICD-9 code for
            `diagnoses_code`.
    Note:
        - `diagnoses_code` is provided in two formats "a numeric format" and
            `a character format`
        - Reference from documentation: "From 1999, the ICD-9-CM codes are
            provided in two formats, the true ICD-9-CM code in character format,
            and a numeric recode found at the end of the record format".
        - Example:
            numeric format: "20700"
            character format: "V700"
    """
    if diagnoses_code in ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS:
        diagnoses_icd_9_code = \
            ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS.get(diagnoses_code)
        if diagnoses_icd_9_code in \
                ("Blank", "Blank diagnosis", "Diagnosis of 'none'",
                 "Noncodable diagnosis", "Noncodable", "Illegible diagnosis"):
            return ""
        return diagnoses_icd_9_code

    # 1975-76 - Instead of a "Y" to prefix codes in the supplementary
    # classification, an ampersand (&) was used
    # 1977 - 78 - Same as above, except that the prefix character is a dash(-)
    # For year 1973 till 1978 `diagnoses_code` is 4 length character
    if len(diagnoses_code) < 5 and (
            diagnoses_code.startswith("&") or diagnoses_code.startswith("-")
            or diagnoses_code.startswith("Y")
    ):
        diagnoses_code = "V{}".format(diagnoses_code[1:])

    # Character format
    # For inapplicable fourth or fifth digits, a dash is inserted.
    # 0010[-] - V829[-] = 001.0[0]-V82.9[0]
    elif "-" in diagnoses_code[3:]:
        diagnoses_code = diagnoses_code.replace("-", "0")
    # Reference from documentation:
    # -9 = Blank
    elif "-00009" in diagnoses_code:
        return ""

    # The prefix “1” preceding the 3-digit diagnostic codes represents
    # diagnoses 001-999, e.g. ‘1381’=’381’=otitis media. And “138100”=”381.00”
    if diagnoses_code.startswith("1"):
        diagnoses_code = diagnoses_code.lstrip("1")

    # The prefix “2” preceding the 3 - digit diagnostic codes represents "V"
    # code diagnoses VO1 - V82, e.g., ‘2010’=’V10’ and “201081” = “V10.81”
    elif diagnoses_code.startswith("2"):
        if diagnoses_code.startswith("20"):
            diagnoses_code = "V{}".format(diagnoses_code[2:])
        else:
            diagnoses_code = "V{}".format(diagnoses_code[1:])

    # There is an implied decimal between the third and fourth digits
    diagnoses_icd_9_code = "{}.{}".format(
        diagnoses_code[:3], diagnoses_code[3:]
    )

    return diagnoses_icd_9_code


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.MONTH_OF_VISIT.value,
            NAMCSFieldEnum.MONTH_OF_BIRTH.value
    )
)
@enforce_type(str, return_type=int, use_regex=REGEX_FOR_MONTH)
def get_month_from_date(raw_format_date):
    """
    Fetch month from date string.

    Parameters:
        raw_format_date (:class:`str`): String representation of month.

    Returns:
        :class:`str`: Month in human readable format.
    """
    date = None
    for pattern in NAMCS_DATASET_MONTH_PATTERNS:
        try:
            date = datetime.strptime(raw_format_date, pattern)
            if date:
                break
        except ValueError:
            continue

    # Numeric format for month
    month = date.strftime("%m")
    return int(month)


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.YEAR_OF_VISIT.value,
            NAMCSFieldEnum.YEAR_OF_BIRTH.value
    )
)
@enforce_type(str, return_type=int, use_regex=REGEX_FOR_YEAR)
def get_year_from_date(date_pattern=None, **kwargs):
    """
    Method to fetch year from date string.

    Parameters:
        date_pattern (:class:`str`): String representation of year.
        kwargs (:class:`dict`): Other fields used to calculate year when
            `date_pattern` is not provided in method call.

    Returns:
        :class:`int`: Year in human readable format.
    """
    if kwargs and not date_pattern:
        # Use `NAMCSFieldEnum.SOURCE_FILE_ID` to calculate year
        # Example: 2011_NAMCS so year: 2011
        source_file_id = kwargs.get(NAMCSFieldEnum.SOURCE_FILE_ID.value)
        return int(source_file_id.split("_")[0])

    date = None
    for pattern in NAMCS_DATASET_YEAR_PATTERNS:
        try:
            date = datetime.strptime(date_pattern, pattern)
            if date:
                break
        except ValueError:
            continue

    # Numeric format of year
    year = date.strftime("%Y")
    return int(year)


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(NAMCSFieldEnum.GENDER.value)
@enforce_type(str, return_type=str, use_regex=REGEX_FOR_GENDER)
def get_gender(gender):
    """
    Method to fetch gender from field code and convert it
    into human readable format.

    Parameters:
        gender (:class:`str`): Raw code for gender.

    Returns:
        :class:`str`: String representation of `gender`.
    """
    gender_long_name = {
        "1": GenderEnum.FEMALE.value,
        "2": GenderEnum.MALE.value
    }
    return gender_long_name.get(gender)


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(NAMCSFieldEnum.PATIENT_AGE.value)
@enforce_type(str, return_type=float, use_regex=REGEX_FOR_PATIENT_AGE)
def get_age_normalized_to_days(age=None, **kwargs):
    """
    Method to normalize patient age into days.

    Parameters:
        age (:class:`str`): Patient's age.
        kwargs (:class:`dict`): Other fields used to calculate age when
            `age` is not provided to method call.

    Returns:
        :class:`float`:  Patient's age normalized in days.

    Example:
        >>> get_age_normalized_to_days("10")
        3650.0
        >>> required_fields_to_calculate_age = {
        ...             NAMCSFieldEnum.MONTH_OF_VISIT.value: "June",
        ...             NAMCSFieldEnum.YEAR_OF_VISIT.value: "1974",
        ...             NAMCSFieldEnum.MONTH_OF_BIRTH.value: "May",
        ...             NAMCSFieldEnum.YEAR_OF_BIRTH.value: "1910",
        ...         }
        >>> get_age_normalized_to_days(**required_fields_to_calculate_age)
        23407.0
    """
    if kwargs and not age:
        month_of_visit = kwargs.get(NAMCSFieldEnum.MONTH_OF_VISIT.value)
        month_of_birth = kwargs.get(NAMCSFieldEnum.MONTH_OF_BIRTH.value)
        year_of_visit = str(kwargs.get(NAMCSFieldEnum.YEAR_OF_VISIT.value))
        year_of_birth = str(kwargs.get(NAMCSFieldEnum.YEAR_OF_BIRTH.value))

        # For numeric value of month less than 10 using prefix 0
        month_of_visit = "0{}".format(month_of_visit)if month_of_visit < 10 \
            else str(month_of_visit)
        month_of_birth = "0{}".format(month_of_birth)if month_of_birth < 10 \
            else str(month_of_birth)

        visit_date = datetime.strptime(month_of_visit + year_of_visit, "%m%Y")
        birth_date = datetime.strptime(month_of_birth + year_of_birth, "%m%Y")
        if visit_date < birth_date:
            year = birth_date.year - 100
            month = birth_date.month
            day = birth_date.day
            birth_date = datetime(year=year, month=month, day=day)
        age = visit_date-birth_date
        return float(age.days)
    elif age:
        # Note: Using age as stand alone data to convert it to days
        age = float(age) * 365
        return float(age)


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(NAMCSFieldEnum.VISIT_WEIGHT.value)
@enforce_type(str, return_type=float, use_regex=REGEX_FOR_PATIENT_VISIT_WEIGHT)
def get_patient_visit_weight(visit_weight):
    """
    Method to convert visit weight from record to human readable format.

    Parameters:
         (:class:`str`): Patient visit weight.

    Returns:
        :class:`float`: Converted patient visit weight.

    Reference:
        The "patient visit weight" is a vital component in the
        process of producing national estimates from sample data,
        and its use should be   clearly understood by all micro-data file
        users. The statistics contained on the micro-data
        file reflect data concerning only a sample of
        patient visits, not a complete count of all the
        visits that occurred in the United States. Each
        record on the data file represents one
        visit in the sample of 27,369 visits. In order to obtain
        national estimates from the sample,
        each record is assigned an inflation factor called the
        "patient visit weight."
        By aggregating the patient visit weights on the 27,369 sample records
        for 2000, the user  can obtain the estimated
        total of 823,541,999 office visits made in the United States.

    Note:
        `visit_weight` is a right-justified integer.

    Example:
        >>> get_patient_visit_weight("0000013479")
            13479.0
    """
    try:
        return float(visit_weight)
    except ValueError:
        raise ValueError(
            "Could not convert visit weight {}"
            "to float value".format(visit_weight)
        )
