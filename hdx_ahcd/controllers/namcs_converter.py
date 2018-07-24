# -*- coding: utf-8 -*-
"""
Module containing methods to translate NAMCS patient case data into 
human readable form.
"""
# Python modules
from collections import defaultdict
from itertools import tee
import csv
import os

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
from hdx_ahcd.namcs.enums import (
    NAMCSErrorFieldEnum,
    NAMCSFieldEnum, 
)
from hdx_ahcd.utils.context import try_except
from hdx_ahcd.utils.decorators import create_path_if_does_not_exists
from hdx_ahcd.utils.utils import detailed_exception_info

# 3rd party modules
# -N/A

# Global vars
# -N/A


@create_path_if_does_not_exists(ERROR_FILES_DIR_PATH)
def get_generator_by_year(year, namcs_raw_dataset_file=None):
    """
    Method to translate raw NAMCS patient case data for a given year in human 
    readable form.

    Parameters:
        year (:class:`int`): NAMCS year for which raw NAMCS data needs to be
            translated.
        namcs_raw_dataset_file (:class:`str`): Absolute path of
            raw dataset input file. If not specified, local file path will be
            deduced on the basis of `year` specified by user.
            Note: Local (extracted) file must exists for this method to yield
                desired response.

    Returns:
        :class:`generator`: Generator object containing translated
        raw NAMCS patient case data for given year.

    Raises:
        :class:`Exception`: If some of attributes/fields are not
        implemented in the class for `year`, exception is raised
        For example if :class:`Year1973` doesn't implement attribute
        `gender` an exception will be raised.
    """
    dataset_file = namcs_raw_dataset_file if namcs_raw_dataset_file is not None \
        else get_namcs_dataset_path_for_year(year)
    # Constructing source file name on the basis of year specified
    source_file_id = get_normalized_namcs_file_name(year)
    # Error file name to dump the rejected data set
    error_file = os.path.join(
        ERROR_FILES_DIR_PATH, 
        get_customized_file_name(source_file_id, extension="err")
    )

    # Removing existing error file to avoid confusion
    if os.path.exists(error_file):
        with try_except():
            os.remove(error_file)

    # Check if data set file exist before processing
    if os.path.exists(dataset_file):
        with open(dataset_file, "r") as dataset_file_handler:
            errors = []
            with try_except(TypeError, re_raise=True):
                # Get the specific year class from module years                
                year_class_object = vars(years).get("Year{}".format(year))

            # Get the mappings from year class
            field_mappings = year_class_object.get_field_slice_mapping()

            for record_no, record in safe_read_file(dataset_file_handler):
                translated_record = {
                    NAMCSFieldEnum.SOURCE_FILE_ID.value: source_file_id,
                    NAMCSFieldEnum.SOURCE_FILE_ROW.value: record_no + 1
                }
                try:
                    for field_name, slice_object in field_mappings.items():
                        # Evaluate `field_name` which is collection mappings
                        if isinstance(slice_object, (list, tuple)):
                            translated_code = process_multiple_slice_objects(
                                record, field_name, slice_object
                            )
                        else:
                            translated_code = get_field_code_from_record(
                                record, field_name, slice_object
                            )
                        translated_record[field_name] = translated_code

                    # Populate all `CONVERTED_CSV_FIELDS` for `record`
                    translated_record = populate_missing_fields(
                        CONVERTED_CSV_FIELDS,
                        translated_record
                    )

                    # Case : Removing blank `physician diagnoses` codes from
                    # `translated_record`
                    # Fetching `field_name` whose `translated_code` is `list`
                    # in `translated_record`
                    for field_name in filter(
                        lambda key: isinstance(translated_record[key], list),
                        translated_record
                    ):
                        # Removing blank, empty element from `translated_code`
                        # and reassigning new value to
                        # `translated_record[field_name]`
                        translated_record[field_name] = list(
                            filter(len, translated_record[field_name])
                        )
                except Exception as exc:
                    detailed_exception_info(logger=log)
                    errors.append(
                        {
                            NAMCSErrorFieldEnum.RECORD_NUMBER.value:
                                record_no + 1,
                            NAMCSErrorFieldEnum.RECORD.value: record,
                            NAMCSErrorFieldEnum.EXCEPTION.value: str(exc)
                        }
                    )
                yield translated_record

            # Check if any records was rejected during NAMCS data set processing
            # due to erroneous field value
            if errors:
                # TODO: Discard record or replace None value for erroneous field
                with open(error_file, "w") as error_file_handler:
                    # Error file headers
                    error_file_headers = (
                        NAMCSErrorFieldEnum.RECORD_NUMBER.value,
                        NAMCSErrorFieldEnum.EXCEPTION.value,
                        NAMCSErrorFieldEnum.RECORD.value
                    )
                    writer = csv.DictWriter(
                        error_file_handler,
                        delimiter = ",",
                        fieldnames = error_file_headers
                    )
                    writer.writeheader()
                    for _error in errors:
                        writer.writerow(_error)
                    log.info("Finished writing to error file {}".format(
                        error_file))


def export_to_csv(year, generator_object):
    """
    Method to export the translated NAMCS patient case data into CSV file for a
    given year.

    Parameters:
        year (:class:`int`): Year for which translated NAMCS data will be 
            exported to csv.
        generator_object (:class:`generator`): Generator object containing
            translated NAMCS patient case data for `year`.

    Returns:
        :class:`str`: Absolute path of exported csv file.
    """
    # Constructing source file name on the basis of year specified
    source_file_id = get_normalized_namcs_file_name(year)

    # Absolute path of file where data is exported
    translated_csv_file = os.path.join(
        NAMCS_DATA_DIR_PATH, 
        get_customized_file_name(
            source_file_id, CONVERTED_CSV_FILE_NAME_SUFFIX, extension="csv"
        )
    )

    with try_except():
        # Write all the translated records into CSV file
        with open(translated_csv_file, "w") as csv_file:
            writer = csv.DictWriter(csv_file,
                                    delimiter = ",",
                                    fieldnames = CONVERTED_CSV_FIELDS)
            writer.writeheader()
            for translated_record in generator_object:
                writer.writerow(translated_record)
            log.info("Finished writing to the file %s" % translated_csv_file)

    return os.path.realpath(translated_csv_file)


def get_year_wise_generator(year=None, namcs_raw_dataset_file=None,
                            do_export = False):
    """
    Method to translated NAMCS data for `year` and/or `namcs_dataset_file`
    into human readable form,

    Parameters:
        year (:class:`int` or :class:`tuple` or :class:`list`): NAMCS year(s)
            for which raw data needs to be translated. If year is not specified,
            the conversion will be carried out for all the years defined in
            `YEARS_AVAILABLE`.
        namcs_raw_dataset_file (:class:`str`): Absolute path of
            raw dataset input file. If not specified, local file path will be
            deduced on the basis of `year` specified by user.
            Note: Local (extracted) file must exists for this method to yield
            desired response.
        do_export (:class:`bool`): Indicates whether to export translated NAMCS
            data to csv file.**Default** :const:`False`.

    Returns:
        :class:`defaultdict`: Dictionary containing generator of translated
        NAMCS patient case data for given year along with source file info.
        Further if `do_export` is True, it returns the absolute path of csv
        file where the data is exported.
    """
    year_wise_translated_data = defaultdict(dict)

    # If `year` not specified, translate data for all years `YEARS_AVAILABLE`
    year = YEARS_AVAILABLE if year is None else get_iterable(year)

    # Using integer value for `year`
    for _year in map(int, year):
        year_wise_translated_data[_year]["generator"] = \
            get_generator_by_year(_year, namcs_raw_dataset_file)
        # NAMCS dataset source file info
        year_wise_translated_data[_year]["source_file_info"] = \
            get_namcs_source_file_info(_year)
        # Export translated data to csv file
        if do_export:
            # Using :func:`tee` of module `itertools` to have copy of generator.
            gen_object = tee(
                year_wise_translated_data.get(_year).get("generator"), 1
            )[0]
            year_wise_translated_data[_year]["file_name"] = \
                export_to_csv(_year, gen_object)

    return year_wise_translated_data
