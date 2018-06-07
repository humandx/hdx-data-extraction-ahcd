# -*- coding: utf-8 -*-
"""
This module consists of utility classes and methods.
"""
# Python modules
# - N/A

# 3rd party modules
from namcs.config import log

# Other modules
# - N/A

# Global vars
# - N/A


class TrackValidationError(object):
    """
    This class tracks NAMCS dataset validations.
    It contains :class:`list` validation errors and :class:`bool` is_valid
    property to indicate validation pass or failed.
    """

    def __init__(self):
        self.errors = []

    @property
    def is_valid(self):
        """
        This is a property of :class:`TrackValidationError`. It specifies if
        validation is Successful or not by checking :class:`list` errors.

        Returns:
            :class:`bool`: True if there are no errors and False if there are
            errors.
        """
        return not bool(self.errors)

    def update(self, errors):
        """
        This method updates error messages of an object of
        :class:`TrackValidationError`.
        """
        self.errors.extend(errors)

    @classmethod
    def add(cls, validation_obj1, validation_obj2):
        """
        This method combines error message of two validation objects and
        returns a new one.

        Parameters:
            validation_obj1 (:class:`TrackValidationError`): Validation object
            which contains errors.
            validation_obj2 (:class:`TrackValidationError`): Validation object
            which contains errors.

        Returns:
            :class:`TrackValidationError`: Object having combined error messages
            if any.
        """
        validation_obj = TrackValidationError()
        validation_obj.update(
            validation_obj1.errors + validation_obj2.errors
        )

        return validation_obj

    def show_errors(self):
        """
        Logs validation error messages if any.
        """
        log.error("\n".join(error for error in self.errors))
