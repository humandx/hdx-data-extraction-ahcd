# -*- coding: utf-8 -*-
"""
Module containing useful methods for package `hdx_ahcd`.
"""
# Python modules
from copy import deepcopy
from datetime import datetime
import os

# Other modules
from hdx_ahcd.namcs.config import (
    BASE_FILE_NAME,
    EXTRACTED_DATA_DIR_PATH,
    NAMCS_FILE_NAME,
    NAMCS_PUBLIC_FILE_EXTENSIONS,
    NAMCS_PUBLIC_FILE_URL,
)
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


def get_normalized_namcs_file_name(year):
    """
    Method to get normalized dataset file name in format <YEAR>_NAMCS
    for `year`.

    Parameters:
        year (:class:`str` or :class:`int`): NAMCS year.

    Returns:
        :class:`str`: Normalized dataset file name in format <YEAR>_NAMCS
        for `year`.
    """
    return "{}_NAMCS".format(year)


def get_iterable(parameter):
    """
    Method to convert `parameter` to iterable type.
    Convert `parameter` of type `str`, `int`, `float` into iterable as `list`

    Parameters:
        parameter (:class:`str` or :class:`int` or :class:`float`): Object that
            needs to be iterable.

    Returns:
        :class:`list`: Iterable `parameter`.

    """
    return [parameter] if not isinstance(parameter, (list, tuple)) \
        else parameter


@catch_exception(re_raise=True)
def get_string_representations_of_date(year=1, month=1, day=1):
    """
    Method to get year, month, day from date in desired format.

    Parameters:
          year (:class:`int`): Numeric value of Year.
          month (:class:`int`): Numeric value of month.
          day (:class: `int`): Numeric value of day.

    Returns:
        :class:`dict`: Key value pair of String representation of date.
    """
    # Datetime object
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
    Method to clean out all the fields present in
    `field_codes_for_single_record` and only populate
    `CONVERTED_CSV_FIELDS` discarding rest of fields.

    Parameters:
        headers (:class:`tuple`): Fields required in translated record.
        field_codes_for_single_record (:class:`dict`): Dict containing
            translated data for single record in dataset.

    Returns:
        :class:`dict`: Modified dict containing values for fields defined in
        `CONVERTED_CSV_FIELDS`.

    Note:
        >>> from hdx_ahcd.namcs.config import CONVERTED_CSV_FIELDS
        >>> CONVERTED_CSV_FIELDS
        ("source_file_ID", "source_file_row", "month_of_visit", "year_of_visit"
        , "sex", "age", "physician_diagnoses", "patient_visit_weight")
    """
    code_for_records = deepcopy(field_codes_for_single_record)
    missing_field_value = None

    # Filtering missing fields from headers
    for missing_field in filter(
            lambda key: True if key not in code_for_records else False, headers
    ):

        # Finding conversion method for missing field
        missing_field_mapped_function = get_conversion_method(missing_field)
        if missing_field_mapped_function:
            with try_except(
                method_name=missing_field_mapped_function.__name__,
                re_raise=True
            ):
                missing_field_value = \
                    missing_field_mapped_function(**code_for_records)

        code_for_records[missing_field] = missing_field_value

    # Extra fields that are not required in output format.
    extra_fields = list(filter(
        lambda key: True if key not in headers else False, code_for_records))

    # Keeping ONLY `CONVERTED_CSV_FIELDS` in dict and deleting the rest
    with try_except():
        for extra_field in extra_fields:
            del code_for_records[extra_field]

    return code_for_records


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

    # Converting all `names` to `string`
    names = list(map(str, names))

    custom_file_name = separator.join(names) if len(names) > 1 else names[0]

    return "{}.{}".format(custom_file_name, extension) if extension else \
        custom_file_name


@catch_exception()
@create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
def get_namcs_dataset_path_for_year(year):
    """
    Method to return full file path for specified `year`.

    Parameters:
        year (:class:`int`): Year for which NAMCS dataset
            file path needs to be calculated.

    Returns:
        :class:`str`: Full file path of NAMCS dataset file if it exists.
    """
    if year is not None:
        year_value = \
            get_string_representations_of_date(year=year).get("year_long")
        file_path = os.path.join(
            EXTRACTED_DATA_DIR_PATH,
            get_normalized_namcs_file_name(year_value)
        )

        if os.path.exists(file_path):
            return file_path
    return None


@create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
def rename_namcs_dataset_for_year(year):
    """
    Method to rename NAMCS dataset file for specified `year`.

    Parameters:
        year (:class:`int`): Year for which NAMCS dataset
            file needs to be renamed.

    Returns:
        :class:`str`: Renamed dataset file name for `year`.
    """
    new_file_name = None

    # Get NAMCS year in desired format
    date_details = get_string_representations_of_date(year=year)
    year_value = date_details.get("year_short")
    year_value_long = date_details.get("year_long")

    for namcs_file in NAMCS_FILE_NAME[year]:
        if os.path.exists(
                os.path.join(
                    EXTRACTED_DATA_DIR_PATH,
                    get_customized_file_name(
                        namcs_file, year_value, separator=""
                    )
                )
        ):
            # Existing file
            file_name = os.path.join(
                    EXTRACTED_DATA_DIR_PATH,
                    get_customized_file_name(
                        namcs_file, year_value, separator=""
                    )
            )

            # New File name in format <YEAR>_NAMCS
            new_file_name = os.path.join(
                EXTRACTED_DATA_DIR_PATH,
                get_normalized_namcs_file_name(year_value_long)
            )

            # Renaming file
            with try_except():
                os.rename(file_name, new_file_name)
    return new_file_name


@catch_exception(re_raise=True)
def get_conversion_method(field_name):
    """
    Method to get corresponding method object for `field_name`.

    Parameters:
        field_name (:class:`str`): Field name for which corresponding conversion
            method is required.

    Returns:
        :class:`function`: Corresponding method object if `field_name` exists
            in `CONVERSION_METHOD_MAPPING`.
    Note:
         >>> import hdx_ahcd.mappers.functions
         >>> from hdx_ahcd.utils.decorators import CONVERSION_METHOD_MAPPING
    """
    with try_except():
        if not CONVERSION_METHOD_MAPPING:
            # Required to construct mapping dictionary of
            # field name vs respective functions
            __import__("hdx_ahcd.mappers.functions")

        if field_name in CONVERSION_METHOD_MAPPING:
            return CONVERSION_METHOD_MAPPING.get(field_name)

    raise Exception(
        "For '{}' corresponding mapped function not found".format(field_name)
    )


def get_field_code_from_record(record, field_name, slice_object):
    """
    Method to get corresponding field code for `field_name` from `record`.

    Parameters:
        record (:class:`str`): Actual record from raw dataset file.
        field_name (:class:`str`): Actual field name.
        slice_object (:class:`slice`): Slice object for `field_name`

    Returns:
       :class:`str`: Field code for `field_name` if conversion method for
       `field_name` is present else code of `field_name` from dataset.

    Example:
        - For `field_name = Gender`, Raw code: "1" ,field code : "Female"
    """
    # Fetching specific field code from record
    raw_code = record[slice_object]

    # Find conversion method for field name
    mapping_func = get_conversion_method(field_name)

    with try_except(method_name=mapping_func.__name__, re_raise=True):
        return mapping_func(raw_code) if mapping_func is not None else raw_code


@catch_exception()
def get_slice_object(field_location, field_length):
    """
    Method to get slice object based on the `field_location`
    and `field_length`.

    Parameters:
        field_location (:class:`int`): Start index of field in the record.
        field_length (:class:`int`): Length of field.

    Returns:
        :class `slice`: Slice object based on based on the `field_location`
        and `field_length`.

    Note:
        Records are 1 indexed and not 0 indexed.
    """
    start_index = field_location - 1

    # Case 1: When `field_length` > 1
    # Case 2: When `field_length` is 1
    end_index = start_index + field_length if field_length > 1 \
        else field_location

    return slice(start_index, end_index)


@catch_exception()
def process_multiple_slice_objects(record, field_name, iterable_slice_object):
    """
    Method to get all field codes from raw record for `field_name`.

    Parameters:
        record (:class:`str`): Actual record from raw data set file.
        field_name (:class:`str`): Actual field name.
        iterable_slice_object (:class:`list`): Collection of slice objects for
            field.

    Returns:
        :class:`list`: Field codes for `field_name`.
    """
    return [
        get_field_code_from_record(record, field_name, slice_object)
        for slice_object in iterable_slice_object
    ]


@catch_exception()
def get_namcs_source_file_info(year):
    """
    Method to get details about NAMCS data file for provided `year`.

    Parameters:
        year (:class:`int`): Year for which details about NAMCS dataset file
            are required.

    Returns:
        :class:`dict`: Details about NAMCS dataset files,
        in the form of key value pair year,zip file name of NAMCS dataset,
        public CDC url of NAMCS dataset file.
    """
    years_representations = get_string_representations_of_date(year=year)
    public_file_name = get_customized_file_name(
        BASE_FILE_NAME[year],
        years_representations.get("year_short"),
        NAMCS_PUBLIC_FILE_EXTENSIONS[year],
        separator=""
    )
    url = get_customized_file_name(
        NAMCS_PUBLIC_FILE_URL[year], public_file_name, separator=""
    )
    return {
        "year": int(years_representations.get("year_long")),
        "zip_file_name": public_file_name,
        "url": url
    }


def get_year_from_dataset_file_name(file_name):
    """
    Method to get year from NAMCS dataset file name.

    Parameters:
        file_name(:class:`str`): NAMCS raw dataset file name in the format
            <YEAR>_NAMCS.

    Returns:
        :class:`int` or :class:`NoneType`: Year of NAMCS dataset file if
        `file_name` exists.

    Note:
        Valid NAMCS dataset file name format: <YEAR>_NAMCS.
    """
    return int(os.path.basename(file_name).split("_")[0]) \
        if os.path.exists(file_name) else None


def safe_read_file(file_handle):
    """
    Method to read all records from file irrespective of errors occurred while
    reading certain record.

    Parameters:
        file_handle (:class:`_io.TextIO`): File that needs to be read
            completely irrespective of exception in certain record.

    Returns:
        :class:`generator`: Record from file and record number.
    """
    try:
        for line_no, line in enumerate(file_handle):
            line = line.strip("\n")
            yield line_no, line
    except Exception:
        # In case of exception skip current record and process
        # file for remaining records till all records are not finished
        for line_no, line in safe_read_file(file_handle):
            line = line.strip()
            yield line_no, line
