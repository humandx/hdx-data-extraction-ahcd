# -*- coding: utf-8 -*-
"""
Methods to evaluate fields in raw data set file and convert them
in respective format.
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
from hdx_ahcd.utils.decorators import enforce_type
from hdx_ahcd.utils.decorators import (
    add_method_to_mapping_dict,
    catch_exception
)
from hdx_ahcd.namcs.enums import (
    GenderEnum,
    NAMCSFieldEnum,
)
from hdx_ahcd.helpers.functions import (
    get_icd_9_code_from_database,
    get_icd_9_code_from_raw_code,
)

# Global vars
# -N/A


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.DATE_OF_VISIT.value,
            NAMCSFieldEnum.DATE_OF_BIRTH.value
    )
)
@enforce_type(str, return_type=(str, str),
              use_regex='^(0[1-9]|1[012])([0-9]{2})$')
def get_year_and_month_from_date(raw_format_date):
    """
    Fetch year and month from provided date string.

    Parameters:
        raw_format_date (:class:`str`): Date string in format mmyy.

    Returns:
        :class:`tuple`: Year and month in human readable format.
    """
    date = datetime.strptime(raw_format_date, "%m%y")

    # Get string representation of date for year and month
    year = date.strftime("%Y")
    month = date.strftime("%B")
    return year, month


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_1.value,
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_2.value,
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_3.value,
    )
)
@enforce_type(str, return_type=str, use_regex='^([V|Y|\-|\&|0-9][0-9]{3,5}|'
                                              '[V|0-9]{1}[0-9]{2}[\-|0-9]{1,2})'
                                              '$')
def convert_physician_diagnosis_code(diagnosis_code):
    """
    Method to convert raw physician `diagnosis_code` into ICD-9 format.

    Parameters:
        diagnosis_code (:class:`str`): Raw physician diagnosis_code.

    Returns:
        :class:`str`: Corresponding ICD-9 code for physician `diagnosis_code`.
    """
    # Get ICD9 code for given diagnosis code
    diagnosis_icd_9_code = get_icd_9_code_from_raw_code(diagnosis_code)

    # Finding relative ICD-9 code for diagnosis code
    icd_9_code = get_icd_9_code_from_database(diagnosis_icd_9_code)
    return icd_9_code


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.MONTH_OF_VISIT.value,
            NAMCSFieldEnum.MONTH_OF_BIRTH.value
    )
)
@enforce_type(str, return_type=str, use_regex='^((0[1-9]|1[012])'
                                              '|([A-Z][a-z]{2,8}))$')
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

    # Get string representation of date for month
    month = date.strftime("%B")
    return month


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(
    (
            NAMCSFieldEnum.YEAR_OF_VISIT.value,
            NAMCSFieldEnum.YEAR_OF_BIRTH.value
    )
)
@enforce_type(str, return_type=str, use_regex='^([1-2][0|9])?[0-9]{2}$')
def get_year_from_date(raw_format_year=None, **kwargs):
    """
    Fetch year from date string.

    Parameters:
        raw_format_year (:class:`str`): String representation of year.
        kwargs (:class:`dict`): Other fields used to calculate year when
            `year_of_visit` is not provided.

    Returns:
        :class:`str`: Year in human readable format.
    """
    if kwargs and not raw_format_year:
        # Use `NAMCSFieldEnum.SOURCE_FILE_ID` to calculate year
        source_file_id = kwargs.get(NAMCSFieldEnum.SOURCE_FILE_ID.value)
        # Example: 2011_NAMCS so year: 2011
        year = source_file_id.split('_')[0]
        return year

    date = None
    for pattern in NAMCS_DATASET_YEAR_PATTERNS:
        try:
            date = datetime.strptime(raw_format_year, pattern)
            if date:
                break
        except ValueError:
            continue

    # Get string representation of date for year
    year = date.strftime("%Y")
    return year


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(NAMCSFieldEnum.GENDER.value)
@enforce_type(str, return_type=str, use_regex='^[1|2]$')
def get_gender(gender):
    """
    Method to fetch gender from field code into human readable format.

    Parameters:
        gender (:class:`str`): Raw code for gender.

    Returns:
        :class:`str`: Respective gender.
    """
    gender_long_name = {
        "1": GenderEnum.FEMALE.value,
        "2": GenderEnum.MALE.value
    }
    return gender_long_name.get(gender)


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(NAMCSFieldEnum.PATIENT_AGE.value)
@enforce_type(str, return_type=int, use_regex='^[0|1]{0,1}[0-9]{1,2}$')
def age_reduced_to_days(age=None, **kwargs):
    """
    Method to normalize age into human readable format.

    Parameters:
        age (:class:`str`): Person's age, default value None.
        kwargs (:class:`dict`): Other fields used to calculate age when
            `age` is not provided.

    Returns:
        :class:`int`: Age in days.

    Example:
        >>> age_reduced_to_days(10)
        3650
        >>> required_fields_to_calculate_age = {
        ...             NAMCSFieldEnum.MONTH_OF_VISIT.value: 'June',
        ...             NAMCSFieldEnum.YEAR_OF_VISIT.value: '1974',
        ...             NAMCSFieldEnum.MONTH_OF_BIRTH.value: 'May',
        ...             NAMCSFieldEnum.YEAR_OF_BIRTH.value: '1910',
        ...         }
        >>> age_reduced_to_days(**required_fields_to_calculate_age)
        23407
    """
    if kwargs and not age:
        month_of_visit = kwargs.get(NAMCSFieldEnum.MONTH_OF_VISIT.value)
        year_of_visit = kwargs.get(NAMCSFieldEnum.YEAR_OF_VISIT.value)
        month_of_birth = kwargs.get(NAMCSFieldEnum.MONTH_OF_BIRTH.value)
        year_of_birth = kwargs.get(NAMCSFieldEnum.YEAR_OF_BIRTH.value)
        visit_date = datetime.strptime(month_of_visit + year_of_visit, "%B%Y")
        birth_date = datetime.strptime(month_of_birth + year_of_birth, "%B%Y")
        if visit_date < birth_date:
            year = birth_date.year - 100
            month = birth_date.month
            day = birth_date.day
            birth_date = datetime(year=year, month=month, day=day)
        age = visit_date-birth_date
        return int(age.days)
    # Normalizing age
    elif age:
        # Note: Using age as stand alone data to convert it to days
        age = int(age) * 365
        return int(age)


@catch_exception(re_raise=True)
@add_method_to_mapping_dict(NAMCSFieldEnum.VISIT_WEIGHT.value)
@enforce_type(str, return_type=float, use_regex='^(([0-9.]{5,6})|'
                                                '([0-9.]{10,11}))$')
def get_patient_visit_weight(visit_weight):
    """
    Method to convert raw visit weight from record to human readable format.

    Parameters:
         (:class:`str`): Patient visit weight.

    Returns:
        :class:`float`: Translated patient visit weight.

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
        >>> get_patient_visit_weight('0000013479')
            13479.0
    """
    try:
        return float(visit_weight)
    except ValueError:
        raise ValueError("Could not convert visit weight {} to float "
                         "value".format(visit_weight))
