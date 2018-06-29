# coding=utf-8
"""
Module containing methods to initiate NAMCS dataset file processing.
"""
# Python modules
from collections import defaultdict
from functools import reduce

# 3rd party modules
# -N/A

# Other modules
from hdx_ahcd.controllers.namcs_converter import get_year_wise_generator
from hdx_ahcd.controllers.namcs_extractor import initiate_namcs_dataset_download
from hdx_ahcd.helpers.functions import get_year_from_dataset_file_name
from hdx_ahcd.scripts.namcs_validators import (
    validate_arguments,
    validate_dataset_records
)
from hdx_ahcd.utils.exceptions import TrackValidationError

# Global vars
# -N/A


class NAMCSProcessor(object):
    """
    Class to validate and process NAMCS dataset file(s).
    """
    def execute(self, year=None, file_name=None, do_validation=True,
                do_export=False, force_download=False):
        """
        Method to process NAMCS raw dataset file(s).

        Parameters:
            year (:class:`int` or :class:`tuple` or :class:`list`): NAMCS year.
            file_name (:class:`str`): NAMCS dataset file name.
            do_validation (:class:`bool`): If to perform validation
                on `year` and `file_name`. *Default** :const:`True`.
            do_export (:class:`bool`): Output translated  data into csv file.
                *Default** :const:`False`.
            force_download (:class:`bool`): Whether to force download
                NAMCS raw dataset file even if data set file exists locally.
                *Default** :const:`False`.

        Returns:
            :class:`defaultdict`: Dictionary containing generator of converted
            NAMCS patient case data for given year along with source file
            info Further if `do_export` is True, it returns
            the absolute path of csv file where the data is exported.
        """
        year_wise_translated_data = defaultdict(dict)

        # Skip validation if neither year nor filename is specified.
        if year is None and file_name is None:
            do_validation = False

        if do_validation:
            is_validation_success, validation_object = \
                self.validate(year, file_name)

            # Validation failed.
            if not is_validation_success:
                # Log all the validation errors
                validation_object.show_errors()

                return year_wise_translated_data

        if file_name and year is None:
            year = int(year or get_year_from_dataset_file_name(file_name))

        # Case 1: Data set file not provided.
        # Case 1: `year` is None
        # In this case method `initiate_namcs_dataset_download` and
        # `get_year_wise_generator` will process data for all NAMCS years
        # defined by parameter `YEARS_AVAILABLE`
        # Case 2: `year` = 1973
        # Case 3: `year` = (1973,1975,1977)
        # In case 2 and 3 method `initiate_namcs_dataset_download` will
        # download dataset file if it doesn't exists locally or
        # `force_download` set to True
        # Download and extract files for `year`
        if file_name is None:
            initiate_namcs_dataset_download(year=year,
                                            force_download = force_download)
            # Translate dataset for all files
            year_wise_translated_data = get_year_wise_generator(
                year = year, do_export = do_export
            )
        # Case 2: Year and dataset file name provided.
        # Processing `file_name` for `year`
        elif year and file_name:
            year_wise_translated_data = \
                get_year_wise_generator(
                    year,
                    namcs_dataset_file = file_name,
                    do_export = do_export
                )

        return year_wise_translated_data

    def validate(self, year, file_name):
        """
        Method to validate NAMCS raw dataset files.

        Parameters:
            year (:class:`int`): NAMCS year.
            file_name (:class:`str`): NAMCS raw dataset file name.

        Returns:
            :class:`tuple`: With elements as
                :class:`bool`: Flag to indicate if any errors occurred
                    during execution.
                :class:`TrackValidationError`: TrackValidationError
                    object having errors, if any.
        """
        # Tuple of methods to invoke when performing validation
        methods_to_call = (validate_arguments, validate_dataset_records)

        # Call to :func:`validate_arguments` and
        # :func:`validate_dataset_records`
        validation_objects = \
            [method(year, file_name) for method in methods_to_call]

        # Reduce :class:`TrackValidationError` object into single object
        validation_obj = reduce(TrackValidationError.add, validation_objects)

        return validation_obj.is_valid, validation_obj
