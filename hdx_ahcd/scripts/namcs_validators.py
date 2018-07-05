# coding=utf-8
"""
Module containing methods for validation.
"""
# Python modules
from functools import reduce
from random import randint
import os

# 3rd party modules
# -N/A

# Other modules
from hdx_ahcd.helpers.functions import (
    get_iterable,
    get_normalized_namcs_file_name,
    safe_read_file,
    get_year_from_dataset_file_name,
)
from hdx_ahcd.namcs.config import (
    YEARS_AVAILABLE,
    NAMCS_PUBLIC_FILE_RECORD_LENGTH_BY_YEAR
)
from hdx_ahcd.utils.exceptions import TrackValidationError
from hdx_ahcd.utils.context import try_except

# Global vars
# -N/A


##################################################################
# NAMCS dataset record validator  | Record level Validation
##################################################################
def validate_dataset_records(year, file_name):
    """
    Method to validate records in NAMCS dataset file for provided `year`.

    Parameters:
        year (:class:`int`): Year for which dataset files needs to be
            validated.
        file_name (:class:`str`): NAMCS raw dataset file name.

    Returns:
        :class:`TrackValidationError`: Object of :class:`TrackValidationError`
        having errors if any.
    """
    validation_obj = TrackValidationError()

    if not file_name or isinstance(year, (tuple, list)):
        return validation_obj

    # Check if file exists or not .
    _validation_object = _check_if_file_exists(file_name)
    if not _validation_object.is_valid:
        return _validation_object
    with try_except():
        with open(file_name, "r") as file_handle:
            random_records = list(map(lambda record: record[1],
                                      safe_read_file(file_handle)))
            random_record_choice = randint(0, 4)
            random_record = random_records[random_record_choice]
            random_record_length = len(random_record)
        if random_record_length != \
                NAMCS_PUBLIC_FILE_RECORD_LENGTH_BY_YEAR[year]:
            validation_obj.errors.append(
                "NAMCS dataset file <{}> has record length <{}> whereas <{}> is"
                "expected.".format(
                    file_name, random_record_length,
                    NAMCS_PUBLIC_FILE_RECORD_LENGTH_BY_YEAR[year]
                )
            )

    return validation_obj


##################################################################
# General validators
##################################################################
def validate_arguments(year, file_name):
    """
    Method to validate arguments passed through management command.

     Parameters:
        year (:class:`int`): Year for which dataset files needs to be
            validated.
        file_name (:class:`str`): NAMCS raw dataset file name.

    Returns:
        :class:`TrackValidationError`: Object of :class:`TrackValidationError`
        having errors if any.
    """
    validation_objects = []

    if isinstance(year, (tuple, list)) and file_name is not None:
        return TrackValidationError().errors.append(
            "With multiple NAMCS years: {} as argument,"
            "file_name argument is not supported".format(year)
        )

    # Dataset year provided
    if year:
        validation_objects.append(_validate_namcs_year(year))

    # Dataset file name provided
    if file_name:
        validation_objects.append(_validate_dataset_file_name(file_name))
        validation_objects.append(
            _validate_year_from_dataset_file_name(file_name)
        )

    validation_obj = reduce(TrackValidationError.add, validation_objects)
    return validation_obj


##################################################################
# Helpers - NAMCS file validator | File level validation
##################################################################
def _check_if_file_exists(file_name):
    """
    Method to validate if specified NAMCS dataset file exists.

    Parameters:
        file_name (:class:`str`): NAMCS raw dataset file name.

    Returns:
        :class:`TrackValidationError`: Object of :class:`TrackValidationError`
        having errors if any.
    """
    validation_obj = TrackValidationError()

    # NAMCS dataset file provided for specific year
    if not os.path.exists(file_name):
        validation_obj.errors.append(
            "NAMCS dataset file: {} doesn't exist".format(file_name)
        )

    return validation_obj


def _validate_dataset_file_name_format(file_name):
    """
    Method to validate if the file name specified by user is per format
    <YEAR>_NAMCS.

    Parameters:
        file_name (:class:`str`): NAMCS dataset file name.

    Returns:
        :class:`TrackValidationError`: Object of :class:`TrackValidationError`
        having errors if any.
    """
    validation_obj = TrackValidationError()
    base_file_name = os.path.basename(file_name)

    expected_file_name = (
        get_normalized_namcs_file_name(year) for year in YEARS_AVAILABLE
    )
    if base_file_name not in expected_file_name:
        validation_obj.errors.append(
            "NAMCS dataset file name <{}> failed validation, expected "
            "file name in format <YEAR>_NAMCS".format(file_name)
        )

    return validation_obj


def _validate_year_from_dataset_file_name(file_name):
    """
    Method to validate if year can be extracted from the filename specified.

    Parameters:
        file_name (:class:`str`): NAMCS raw dataset file name.

    Returns:
        :class:`TrackValidationError`: Object of :class:`TrackValidationError`
        having errors if any.
    """
    validation_obj = TrackValidationError()
    year = get_year_from_dataset_file_name(file_name)

    # Validating year from NAMCS file
    if not _validate_namcs_year(year).is_valid:
        validation_obj.errors.append(
            "Unable to extract year from file name <{}>. Please specify "
            "file name in format <YEAR>_NAMCS".format(file_name)
        )

    return validation_obj


def _validate_dataset_file_name(file_name):
    """
    Method to validate name of NAMCS dataset file.

    Parameters:
        file_name (:class:`str`): NAMCS raw dataset file name.

    Returns:
        :class:`TrackValidationError`: Object of :class:`TrackValidationError`
        having errors if any.
    """
    # Check if file exists and Validate file name format
    validation_objects = [
        _check_if_file_exists(file_name),
        _validate_dataset_file_name_format(file_name)
    ]

    # Reduce list of `TrackValidationError` object into single object
    validation_obj = reduce(TrackValidationError.add, validation_objects)
    return validation_obj


def _validate_namcs_year(year):
    """
    Method to validate year of NAMCS dataset file.

    Parameters:
        year (:class:`str` or :class:`int`): Year for NAMCS raw dataset.

    Returns:
        :class:`TrackValidationError`: Object of :class:`TrackValidationError`
        having errors if any.
    """
    validation_obj = TrackValidationError()
    year = get_iterable(year)
    for _year in map(int, year):
        if _year not in YEARS_AVAILABLE:
            validation_obj.errors.append(
                "Year {} is not valid year, please specify valid years"
                ",valid years are: {}".format(_year, YEARS_AVAILABLE)
            )
    return validation_obj
