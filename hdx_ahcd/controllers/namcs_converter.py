# -*- coding: utf-8 -*-
"""
Module to translate NAMCS patient case data into human readable form.
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
from hdx_ahcd.namcs.enums import NAMCSFieldEnum, NAMCSErrorFieldEnum
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
    Method to translate raw NAMCS patient case data for a given year.

    Parameters:
        year (:class:`int`): NAMCS year for which raw data needs to be
            translated.
        namcs_raw_dataset_file (:class:`str`): Absolute path of
            raw dataset input file. If not specified, local file path will be
            deduced on the basis of `year` specified by user.
            Note: Local (extracted) file must exists for this method to yield
                desired response.

    Returns:
        :class:`generator`: Generator object containing translated
            raw NAMCS patient case data for given year.
    """
    dataset_file = namcs_raw_dataset_file if namcs_raw_dataset_file else \
        get_namcs_dataset_path_for_year(year)
    # Constructing source file name on the basis of year specified
    source_file_id = get_normalized_namcs_file_name(year)
    # Error file name to dump the rejected data set
    error_file = os.path.join(
        ERROR_FILES_DIR_PATH, get_customized_file_name(source_file_id,
                                                       extension = "err")
    )

    # Removing existing error file to avoid confusion
    if os.path.exists(error_file):
        with try_except():
            os.remove(error_file)

    # Check if data set file exist before processing
    if os.path.exists(dataset_file):
        with open(dataset_file, "r") as dataset_file_handler:
            errors = []
            # Get the specific year class from year module
            year_class_object = vars(years).get("Year{}".format(year))
            # Get the mappings from year class
            field_mappings = year_class_object.get_field_slice_mapping()

            for line_no, line in safe_read_file(dataset_file_handler):
                converted_record = {
                    NAMCSFieldEnum.SOURCE_FILE_ID.value: source_file_id,
                    NAMCSFieldEnum.SOURCE_FILE_ROW.value: line_no + 1
                }
                try:
                    for field_name, slice_object in field_mappings.items():
                        # If slice_object is tuple evaluating all items at
                        # last to club all the results under one `field_name`
                        if isinstance(slice_object, (list, tuple)):
                            converted_code = process_multiple_slice_objects(
                                line, field_name, slice_object
                            )
                        else:
                            converted_code = get_field_code_from_record(
                                line, field_name, slice_object
                            )
                        converted_record[field_name] = converted_code

                    # Populate all the missing fields to ensure all the fields
                    # are returned in the generator
                    converted_record = \
                        populate_missing_fields(CONVERTED_CSV_FIELDS,
                                                converted_record)
                except Exception as exc:
                    detailed_exception_info(logger=log)
                    errors.append(
                        {
                            NAMCSErrorFieldEnum.RECORD_NUMBER.value:
                                line_no + 1,
                            NAMCSErrorFieldEnum.RECORD.value: line,
                            NAMCSErrorFieldEnum.EXCEPTION.value: str(exc)
                        }
                    )
                yield converted_record

            # Check if any records was rejected during NAMCS data set processing
            if errors:
                # TODO: Discard record or replace None value for erroneous field
                with open(error_file, "w") as error_file_handler:
                    # Error file headers
                    error_file_headers = (
                        NAMCSErrorFieldEnum.RECORD_NUMBER.value,
                        NAMCSErrorFieldEnum.EXCEPTION.value,
                        NAMCSErrorFieldEnum.RECORD.value
                    )
                    writer = csv.DictWriter(error_file_handler,
                                            delimiter = ',',
                                            fieldnames = error_file_headers)
                    writer.writeheader()
                    for _error in errors:
                        writer.writerow(_error)
                    log.info("Finished writing to error file {}".format(
                        error_file))


def export_to_csv(year, generator_object):
    """
    Method to export the converted NAMCS patient case data into CSV file for a
    given year.

    Parameters:
        year (:class:`int`): NAMCS year for which data is being exported to csv.
        generator_object (:class:`generator`): Generator object containing
            converted NAMCS patient case data for a given year.

    Returns:
        :class:`str`: Absolute path of exported csv file.
    """
    # Constructing source file name on the basis of year specified
    source_file_id = get_normalized_namcs_file_name(year)

    # Absolute path of file where data is exported
    converted_csv_file = os.path.join(
        NAMCS_DATA_DIR_PATH, get_customized_file_name(
            source_file_id, CONVERTED_CSV_FILE_NAME_SUFFIX, extension = "csv"
        )
    )

    with try_except():
        # Write all the converted records into CSV file
        with open(converted_csv_file, 'w') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    delimiter = ',',
                                    fieldnames = CONVERTED_CSV_FIELDS)
            writer.writeheader()
            for converted_record in generator_object:
                writer.writerow(converted_record)
            log.info("Finished writing to the file %s" % converted_csv_file)

    return os.path.realpath(converted_csv_file)


def get_year_wise_generator(year=None, namcs_dataset_file=None,
                            do_export = False):
    """
    Method to convert raw NAMCS patient case data into CSV, and return a
    dictionary containing generator of converted NAMCS patient case data for
    given year.

    Additionally you can get the converted data into a CSV file by setting
    `do_export` as True.

    Parameters:
        year (:class:`int` or :class:`tuple` or :class:`list`): NAMCS year(s)
            for which raw data needs to be converted. If year is not specified,
            the conversion will be carried out for all the years defined in
            `YEARS_AVAILABLE`.
        namcs_dataset_file (:class:`str`): Absolute path of
            raw dataset input file.
        do_export (:class:`bool`): Flag to indicate whether to dump the
            converted NAMCS patient case data into CSV file.
            **Default** :const:`False`.

    Returns:
        :class:`defaultdict`: Dictionary containing generator of converted
            NAMCS patient case data for given year along with source file info.
            Further if `do_export` is True, it returns the absolute path of csv
            file where the data is exported.
    """
    year_wise_translated_data = defaultdict(dict)

    # If year not specified, the process the data set for all available year
    year = YEARS_AVAILABLE if year is None else get_iterable(year)

    # Set the generator and source file information into the dictionary
    for _year in year:
        year_wise_translated_data[_year]["generator"] = \
            get_generator_by_year(_year, namcs_dataset_file)

        # NAMCS dataset source file info
        year_wise_translated_data[_year]["source_file_info"] = \
            get_namcs_source_file_info(_year)

    # Set the absolute path of file where converted data is exported
    if do_export and year_wise_translated_data:
        for _year in year:
            if year_wise_translated_data.get(_year).get("generator"):
                gen_object = \
                    year_wise_translated_data.get(_year).get("generator")

                year_wise_translated_data[_year]["file_name"] = \
                    export_to_csv(_year, gen_object)

    return year_wise_translated_data
