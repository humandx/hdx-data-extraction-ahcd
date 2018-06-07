# coding=utf-8
"""
Controller file to initiate NAMCS processing.
"""
# Python modules
from functools import reduce

# 3rd party modules
# -N/A

# Other modules
from general.namcs_convertor import (
    get_year_wise_generator
)
from general.namcs_extractor import (
    extract_data_zipfile,
    download_namcs_zipfile,
    initiate_namcs_dataset_download,
)
from helpers.functions import (
    get_namcs_datset_path_for_year,
    get_year_from_dataset_file_name,
    rename_namcs_dataset_for_year,
)
from scripts.validation import (
    validate_arguments,
    validate_dataset_records
)
from utils.exceptions import TrackValidationError

# Global vars
# -N/A


class NAMCSController(object):
    """
    Class to validate and process NAMCS raw dataset files.
    """
    def execute(self, year=None, file_name=None, do_validation=True,
                do_export=False, force_download=True):
        """
        Method to process NAMCS raw dataset files.

        Parameters:
            year (:class:`int` or :class:`tuple` or :class:`list`): NAMCS year.
            file_name (:class:`str`): NAMCS raw dataset file name.
            do_validation (:class:`bool`): Flag to indicate if perform
                validation on `year` and `file_name` default value True to
                perform validation.
            do_export (:class:`bool`) : Flag to indicate if to dump the
                converted raw NAMCS patient case data into CSV file as
                defined by `CONVERTED_CSV_FILE_NAME_SUFFIX` for
                given year default value False.
            force_download (:class:`bool`) : Whether to force download
                NAMCS raw dataset file even if it exists,Default value True.
        
        Returns:
            :class:`defaultdict` : Dictionary containing generator of
                converted raw NAMCS patient case data for given year.
        """
        year_wise_mld = dict()

        if year or file_name:
            if not isinstance(year, (tuple, list)):
                year = int(year or get_year_from_dataset_file_name(file_name))
                file_name = file_name or get_namcs_datset_path_for_year(year)
            # Do validation if multiple years are specified to
            # check each year is present in `YEARS_AVAILABLE`
        else:
            # Skip validation if neither year nor filename is specified
            do_validation = False

        if do_validation:
            if not self.validate(year, file_name):
                return TrackValidationError()

        # Process file
        # Case 1: when file_name is not given and year = 1973
        # Case 2: when file_name is not given and year = (1973,1975,1977)
        if year:
            if not isinstance(year, (tuple, list)):
                year = [year]
            for _year in year:
                # Checking if NAMCS dataset file already exists in the
                # `EXTRACTED_DATA_DIR_PATH`
                if get_namcs_datset_path_for_year(_year) is None or \
                        force_download:
                    # Download and process file for year
                    full_file_name = download_namcs_zipfile(_year)
                    # Extract downloaded zipped file
                    extract_data_zipfile(_year, full_file_name)
                    # Renaming NAMCS file
                    rename_namcs_dataset_for_year(_year)
                # Processing file for year
                year_wise_mld.update(
                    get_year_wise_generator(_year, do_export = do_export)
                )

        elif not (year and file_name):
            # Download and extract files for all years
            initiate_namcs_dataset_download(force_download = force_download)
            # Translate dataset for all files
            year_wise_mld = get_year_wise_generator()

        elif year and file_name:
            # Processing file for year
            year_wise_mld = \
                get_year_wise_generator(
                    year,
                    namcs_raw_dataset_file = file_name,
                    do_export = do_export
                )

        return year_wise_mld

    @staticmethod
    def validate(year, file_name):
        """
        Method to validate NAMCS raw dataset files.

        Parameters:
            year (:class:`int`): NAMCS year.
            file_name (:class:`str`): NAMCS raw dataset file name.
        """
        validation_objs = []

        # Tuple of methods to invoke when performing validation
        methods_to_call = (
            validate_arguments,
            validate_dataset_records
        )
        for method in methods_to_call:
            validation_objs.append(method(year, file_name))

        # Reduce TrackValidationError object into single object
        validation_obj = reduce(TrackValidationError.add, validation_objs)

        # Log all the validation errors
        if not validation_obj.is_valid:
            validation_obj.show_errors()

        return validation_obj.is_valid
