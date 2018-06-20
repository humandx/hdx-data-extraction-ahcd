# -*- coding: utf-8 -*-
"""
This file translates raw NAMCS patient case data into converted csv file.
"""
# Python modules
import csv
import os
from collections import defaultdict

# Other modules
from hdx_ahcd.helpers.functions import (
    get_customized_file_name,
    get_field_code_from_record,
    get_iterable,
    get_namcs_dataset_path_for_year,
    get_normalized_namcs_file_name,
    get_namcs_source_file_info,
    process_multiple_slice_objects,
    populate_missing_fields,
    safe_read_file
)
from hdx_ahcd.mappers import years
from hdx_ahcd.namcs.config import (
    CONVERTED_CSV_FIELDS,
    CONVERTED_CSV_FILE_NAME_SUFFIX,
    ERROR_FILES_DIR_PATH,
    NAMCS_DATA_DIR_PATH,
    log,
    YEARS_AVAILABLE
)
from hdx_ahcd.namcs.enums import NAMCSFieldEnum
from hdx_ahcd.utils.context import try_except
from hdx_ahcd.utils.decorators import (
    create_path_if_does_not_exists
)
from hdx_ahcd.utils.utils import detailed_exception_info

# 3rd party modules
# -N/A

# Global vars
# -N/A


@create_path_if_does_not_exists(ERROR_FILES_DIR_PATH)
def get_generator_by_year(year, namcs_raw_dataset_file=None):
    """
    Method to translate raw NAMCS patient case data for given year.

    Parameters:
        year (:class:`int`): NAMCS year for which raw data needs to be
            translated.
        namcs_raw_dataset_file (:class:`str`): File path for
            raw dataset input file. Default value None, in that case will try to
            get local path for downloaded raw namcs dataset.

    Returns:
        :class:`generator`: Generator object containing converted
            raw NAMCS patient case data for given year.
    """
    year_class_object = vars(years).get("Year{}".format(year))
    dataset_file = namcs_raw_dataset_file if namcs_raw_dataset_file else \
        get_namcs_dataset_path_for_year(year)

    # Calculating `SOURCE_FILE_ID`
    source_file_id = get_normalized_namcs_file_name(year)

    # Error file name
    error_file = os.path.join(
        ERROR_FILES_DIR_PATH, get_customized_file_name(source_file_id,
                                                       extension = "err")
    )

    # Removing existing error file
    if os.path.exists(error_file):
        with try_except():
            os.remove(error_file)

    # Error file name headers
    error_file_headers = ("record_no", "exception", "record")

    errors = []

    field_mappings = year_class_object.get_field_slice_mapping()

    # Check if file exist before processing
    if os.path.exists(dataset_file):
        with open(dataset_file, "r") as dataset_file_handler:
            for line_no, line in safe_read_file(dataset_file_handler):
                write_line = {
                    NAMCSFieldEnum.SOURCE_FILE_ID.value: source_file_id,
                    NAMCSFieldEnum.SOURCE_FILE_ROW.value: line_no + 1
                }
                try:
                    for field_name, slice_object in field_mappings.items():
                        # If slice_object is tuple evaluating all items at
                        # last to club all the results under one `field_name`.
                        if isinstance(slice_object, (list, tuple)):
                            code = process_multiple_slice_objects(
                                line, field_name, slice_object
                            )
                        else:
                            code = get_field_code_from_record(
                                line, field_name, slice_object
                            )
                        write_line[field_name] = code

                    # Call to method `populate_missing_fields` to calculate
                    # all missing fields.
                    write_line = \
                        populate_missing_fields(CONVERTED_CSV_FIELDS,
                                                write_line)
                except Exception as exc:
                    detailed_exception_info(logger=log)
                    errors.append(
                        {
                            "record_no": line_no + 1,
                            "record": line,
                            "exception": str(exc)
                        }
                    )
                yield write_line
            if errors:
                # TODO: discard record or replace None value for erroneous field
                with open(error_file, "w") as error_file_handler:
                    writer = csv.DictWriter(error_file_handler,
                                            delimiter = ',',
                                            fieldnames = error_file_headers)
                    writer.writeheader()
                    for _error in errors:
                        writer.writerow(_error)
                    log.info("Finished writing to error file: {}".format(
                        error_file))


def export_to_csv(year, generator_object):
    """
    Method to dump the converted raw NAMCS patient case data into CSV file as
    defined by `CONVERTED_CSV_FILE_NAME_SUFFIX` for given year.

    Parameters:
        year (:class:`int`): NAMCS year for which raw data needs to be
            translated.
        generator_object (:class:`generator`): Generator object containing
            converted raw NAMCS patient case data for given year.

    Returns:
        :class:`str`: File path for `CONVERTED_CSV_FILE_NAME_SUFFIX`.
    """
    # Calculating `SOURCE_FILE_ID`
    source_file_id = get_normalized_namcs_file_name(year)

    # Output csv file converting the initial dataset into mapped data
    converted_csv_file = os.path.join(
        NAMCS_DATA_DIR_PATH, get_customized_file_name(
            source_file_id, CONVERTED_CSV_FILE_NAME_SUFFIX, extension = "csv"
        )
    )

    with try_except():
        with open(converted_csv_file, 'w') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    delimiter = ',',
                                    fieldnames = CONVERTED_CSV_FIELDS)
            writer.writeheader()
            for write_line in generator_object:
                writer.writerow(write_line)
            log.info("Finished writing to the file %s" % converted_csv_file)

    return os.path.realpath(converted_csv_file)


def get_year_wise_generator(year=None, namcs_raw_dataset_file=None,
                            do_export = False):
    """
    Method to convert raw NAMCS patient case data into CSV, and return a
    dictionary containing generator of converted raw NAMCS patient case data for
    given year if `do_export` is false else dump the converted raw NAMCS
    patient case data into CSV file as defined by
    `CONVERTED_CSV_FILE_NAME_SUFFIX` for given year.

    Parameters:
        year (:class:`int` or :class:`tuple` or :class:`list`): NAMCS year(s)
            for which raw data needs to be translated. Default None , in
            case of None for all years defined in `YEARS_AVAILABLE`, this method
            will be executed.
        namcs_raw_dataset_file (:class:`str`): File path for
            raw dataset input file, Default value None, in that case will try to
            get local path for downloaded raw namcs dataset.
        do_export (:class:`bool`): Flag to indicate if to dump the converted
            raw NAMCS patient case data into CSV file as defined by
            `CONVERTED_CSV_FILE_NAME_SUFFIX` for given year default value False.

    Returns:
        :class:`defaultdict`: Dictionary containing generator of converted
            NAMCS patient case data for given year along with source file info.
            Further if `do_export` is True, it returns the absolute path of csv
            file where the data is exported.
    """
    year_wise_mld = defaultdict(dict)

    # If year not specified, run this for all available year
    if year is None:
        year = YEARS_AVAILABLE

    year = get_iterable(year)
    for _year in year:
        year_wise_mld[_year]["generator"] = \
            get_generator_by_year(_year, namcs_raw_dataset_file)
        year_wise_mld[_year]["source_file_info"] = \
            get_namcs_source_file_info(_year)

    if do_export and year_wise_mld:
        for _year in year:
            year_wise_mld[_year]["file_name"] = \
                export_to_csv(_year, year_wise_mld[_year]["generator"])

    return year_wise_mld
