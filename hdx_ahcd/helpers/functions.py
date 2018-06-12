# -*- coding: utf-8 -*-
"""
Helper file for all useful functions
"""
# Python modules
import os
from copy import deepcopy
from datetime import datetime

# Other modules
from hdx_ahcd.namcs.config import (
    BASE_FILE_NAME,
    EXTRACTED_DATA_DIR_PATH,
    NAMCS_FILE_NAME,
    NAMCS_PUBLIC_FILE_EXTENSIONS,
    NAMCS_PUBLIC_FILE_URL,
    log
)
from hdx_ahcd.namcs.constants import ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS
from hdx_ahcd.utils.context import try_except
from hdx_ahcd.utils.decorators import (
    catch_exception,
    create_path_if_does_not_exists,
    CONVERSION_METHOD_MAPPING
)

# 3rd party modules
# -N/A

# Global vars
# -N/A

# Lambda function to get normalized hdx_ahcd file name
get_normalized_namcs_file_name = lambda year: "{}_NAMCS".format(year)
get_iterable = lambda parameter: [parameter] \
    if not isinstance(parameter, (list, tuple)) else parameter


@catch_exception()
def get_string_representations_of_date(year=1, month=1, day=1):
    """
    Method to get year, month, day from date in desired format.

    Parameters:
          year (:class:`int`): Integer indicating year default value 1.
          month (:class:`int`): Integer indicating month default value 1.
          day (:class: `int`): Integer indicating day default value 1.

    Returns:
        :class:`dict` : Dict containing various string representation of date.
    """
    date = datetime(year=year, month=month, day=day)
    return {
        "year_short": date.strftime("%y"),
        "year_long": date.strftime("%Y"),
        "month_numeric": date.strftime("%m"),
        "month_short": date.strftime("%b"),
        "month_long": date.strftime("%B"),
        "day_numeric": date.strftime("%d"),
        "date_time_object": date
    }


def populate_missing_fields(headers, field_codes_for_single_record):
    """
    Method to clean out all the fields present in `write_line_dict`
    and only populate `CONVERTED_CSV_FIELDS` discarding rest of fields.

    Parameters:
        headers (:class:`list`): List containing required fields in
            mapped output csv file.
        field_codes_for_single_record (:class:`dict`): Dict containing mapped
            data for single row in input raw file.

    Returns:
        :class:`dict`: Modified dict containing ONLY `CONVERTED_CSV_FIELDS`.
    """
    data_dict = deepcopy(field_codes_for_single_record)
    missing_field_value = None

    # Filtering missing fields from headers
    for missing_field in filter(
            lambda key: True if key not in data_dict else False, headers):
        missing_field_mapped_function = get_conversion_method(missing_field)
        if missing_field_mapped_function:
            with try_except(method_name=missing_field_mapped_function,
                            reraise=True):
                missing_field_value = missing_field_mapped_function(**data_dict)
            data_dict[missing_field] = missing_field_value

    extra_fields = list(filter(
        lambda key: True if key not in headers else False, data_dict))

    # Keeping ONLY `CONVERTED_CSV_FIELDS` in dict and deleting the rest
    with try_except():
        for extra_field in extra_fields:
            del data_dict[extra_field]

    return data_dict


def get_customized_file_name(*names, separator="_", extension=None):
    """
    Method to get file name in customized way using `separator` and `extension`.

    Parameters:
        names (:class:`tuple` or :class:`str`): Names need to be combined by
            `separator` and with `extension`.
        separator (:class:`str`): Desired name separator.
        extension (:class:`str`): Desired file extension.

    Returns:
        :class:`str`: Customized file name.
    """
    names = names[0] if isinstance(names[0], (list, tuple)) else names
    names = list(
        map(lambda name: name if isinstance(name, str) else str(name), names)
    )
    custom_file_name = \
        separator.join([name for name in names]) if len(names) > 1 else names[0]

    return "{}.{}".format(custom_file_name, extension) if extension else \
        custom_file_name


@catch_exception()
@create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
def get_namcs_datset_path_for_year(year):
    """
    Method to return full file path for specified year.

    Parameters:
        year (:class:`int`): Year in integers.

    Returns:
        :class:`str`: A str containing file path of data set for provided year
            if file path exists else none.
    """
    year_value = get_string_representations_of_date(year=year).get("year_long")
    file_path = os.path.join(
        EXTRACTED_DATA_DIR_PATH,
        get_normalized_namcs_file_name(year_value)
    )

    if os.path.exists(file_path):
        return file_path

    log.error("For year {}, raw data set file not found".format(year_value))
    return None


@create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
def rename_namcs_dataset_for_year(year):
    """
    Method to rename NAMCS file for specified year.

    Parameters:
        year (:class:`int`): Year in integers.

    Returns:
        :class:`str`: Renamed file name for specified year.

    """
    new_file_name = None
    date_details = get_string_representations_of_date(year=year)
    year_value = date_details.get("year_short")
    year_value_long = date_details.get("year_long")

    for namcs_file in NAMCS_FILE_NAME[year]:
        if os.path.exists(
                os.path.join(
                    EXTRACTED_DATA_DIR_PATH,
                    get_customized_file_name(namcs_file,
                                             year_value, separator = "")
                )
        ):
            file_name = \
                os.path.join(
                    EXTRACTED_DATA_DIR_PATH, get_customized_file_name(
                        namcs_file, year_value, separator = ""
                    )
                )
            new_file_name = os.path.join(
                EXTRACTED_DATA_DIR_PATH,
                get_normalized_namcs_file_name(year_value_long)
            )

            # Renaming file
            with try_except():
                os.rename(file_name, new_file_name)
    return new_file_name


@catch_exception(reraise=True)
def get_conversion_method(field_name):
    """
    Method to get corresponding method for `field_name`.

    Parameters:
        field_name (:class:`str`): Indicating field name to be searched in
            global dict of `CONVERSION_METHOD_MAPPING` field and method
            MAPPINGS.

    Returns:
        :class:`function`: Mapped method of provided field if Mapped method
            of provided field exists else None.

    """
    with try_except():
        if not CONVERSION_METHOD_MAPPING:
            # Required to construct mapping dictionary of
            # field name vs respective functions
            __import__("hdx_ahcd.mapper.functions")

        if field_name in CONVERSION_METHOD_MAPPING:
            return CONVERSION_METHOD_MAPPING.get(field_name)

    raise Exception(
        "For '{}' corresponding mapped function not found".format(field_name)
    )


@catch_exception()
def get_icd_9_code_from_numeric_string(diagnosis_code):
    """
    Method to get convert raw `diagnosis_code` into ICD-9 format.

    Parameters:
        diagnosis_code (:class:`str`): String representation of diagnosis_code.

    Returns:
        :class:`str`: mapped representation of corresponding ICD-9 code for
            `diagnosis_code`.
    Note:
        - `diagnosis_code` is currently 'a numeric format'.
        - Reference from documentation: 'From 1999, the ICD-9-CM codes are
            provided in two formats, the true ICD-9-CM code in character format,
            and a numeric recode found at the end of the record format'.
        - Example:
            numeric format: '20700'
            character format: 'V700'
    """
    if diagnosis_code in ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS:
        diagnosis_icd_9_code = \
            ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS.get(diagnosis_code)
        if diagnosis_icd_9_code in \
                ("Blank", "Blank diagnosis", "Diagnosis of 'none'",
                 "Noncodable diagnosis", "Noncodable", "Illegible diagnosis"):
            return ""
        return diagnosis_icd_9_code

    # 1975-76 - Instead of a "Y" to prefix codes in the supplementary
    # classification, an ampersand (&) was used
    # 1977 - 78 - Same as above, except that the prefix character is a dash(-)
    if diagnosis_code.startswith("&") or diagnosis_code.startswith("-"):
        diagnosis_code = "Y{}".format(diagnosis_code[1:])

    # The prefix “1” preceding the 3-digit diagnostic codes represents
    # diagnoses 001-999, e.g. ‘1381’=’381’=otitis media. And “138100”=”381.00”
    if diagnosis_code.startswith("1"):
        diagnosis_code = diagnosis_code.lstrip("1")

    # The prefix “2” preceding the 3 - digit diagnostic codes represents "V"
    # code diagnoses VO1 - V82, e.g., ‘2010’=’V10’ and “201081” = “V10.81”
    elif diagnosis_code.startswith("2"):
        if diagnosis_code.startswith("20"):
            diagnosis_code = "V{}".format(diagnosis_code[2:])
        else:
            diagnosis_code = "V{}".format(diagnosis_code[1:])

    # There is an implied decimal between the third and fourth digits
    diagnosis_icd_9_code = "{}.{}".format(
        diagnosis_code[:3], diagnosis_code[3:]
    )

    return diagnosis_icd_9_code


@catch_exception()
def get_icd_9_code_from_database(diagnosis_icd_9_code):
    """
    Method to get corresponding ICD-9 code for `diagnosis_code`.

    Parameters:
        diagnosis_icd_9_code (:class:`str`): String representation of
            diagnosis_code.

    Returns:
        :class:`str`: String representation of corresponding ICD-9 code for
            `diagnosis_code`.
    """
    # TODO : Fetch corresponding ICD-9 code for `diagnosis_code` from database
    icd_9_code = diagnosis_icd_9_code
    return icd_9_code


def get_field_code_from_record(line, field_name, slice_object):
    """
    Method to get corresponding field code for `field_name` from raw dataset
    characters.

    Parameters:
        line (:class:`str`): Actual record from raw dataset file.
        field_name (:class:`str`): Actual field name.
        slice_object (:class:`slice`): Slice object for `field_name`

    Returns:
       :class:`str`: Corresponding field code for each `field_name`
            if `mapping_func` is present else raw code of `field_name`
            from dataset.
    Example:
        - Raw code : "1" ,field code : "Female" for `field_name = Gender`
    """
    raw_code = line[slice_object]
    mapping_func = get_conversion_method(field_name)
    with try_except(method_name=mapping_func, reraise=True):
        return mapping_func(raw_code) if mapping_func else raw_code


@catch_exception()
def get_slice_object(indexes):
    """
    Method to return slice object based on the `indexes` passed.

    Parameters:
        indexes (:class:`list`): List of start and stop index to build slice
            object.

    Returns:
        :class `slice`: Slice object based on `indexes`.
    """
    # Case 1: When indexes is provided as ["2", "3"]
    if len(indexes) > 1:
        return slice(int(indexes[0]) - 1, int(indexes[1]))
    # Case 2: When indexes is provided as ["3"]
    else:
        return slice(int(indexes[0]) - 1, int(indexes[0]))


@catch_exception()
def process_multiple_slice_objects(record, field_name, iterable_slice_object):
    """
    Method to get all field codes from raw record for `iterable_slice_object`.

    Parameters:
        record (:class:`str`): Actual record from raw data set file.
        field_name (:class:`str`): Actual field name.
        iterable_slice_object (:class:`list`): Tuple of `MAPPINGS`.

    Returns:
        :class:`generator`: Generator having corresponding field code for each
            `MAPPINGS`.
    """
    return [
        get_field_code_from_record(
            record, field_name, slice_object
        ) for slice_object in iterable_slice_object
    ]


@catch_exception()
def get_namcs_source_file_info(year):
    """
    Method to get public NAMCS data file name and url for provided year.

    Parameters:
        year(:class:`int`): The year for which data is requested.

    Returns:
        :class:`dict`: Dict containing string representation of year,
            public hdx_ahcd file name, url for public hdx_ahcd file name.
    """
    year_value = get_string_representations_of_date(year=year).get("year_short")
    public_file_name = \
        get_customized_file_name(BASE_FILE_NAME[year],
                                 year_value,
                                 NAMCS_PUBLIC_FILE_EXTENSIONS[year],
                                 separator=""
                                 )
    url = \
        get_customized_file_name(NAMCS_PUBLIC_FILE_URL[year],
                                 public_file_name,
                                 separator=""
                                 )
    return {
        "year": year_value,
        "zip_file_name": public_file_name,
        "url": url
    }


def get_year_from_dataset_file_name(file_name):
    """
    Method to get year from NAMCS dataset file name.

    Parameters:
        file_name(:class:`str`): NAMCS raw dataset file name in the format
            <YEAR>_NAMCS

    Returns:
        :class:`int`: Extracted year from input raw dataset file name
    """
    base_file_name = os.path.basename(file_name)

    # NAMCS file format: <YEAR>_NAMCS
    year = base_file_name.split("_")[0]

    return year


def safe_read_file(file_handle):
    """
    Method to read all records from file irrespective of errors occurred while
    reading certain record.

    Args:
        file_handle (:class:`_io.TextIOWrapper`): File that needs to be read
            completely irrespective of exception in certain record

    Returns:
        :class:`generator` : Record from file.
    """
    try:
        for line_no, line in enumerate(file_handle):
            yield line_no, line
    except Exception:
        for line_no, line in safe_read_file(file_handle):
            yield line_no, line
