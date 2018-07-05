# -*- coding: utf-8 -*-
"""
Module to containing utility classes for  NAMCS data model.
"""
# Python modules
from collections import Iterable
import linecache
import sys

# 3rd party modules
# -N/A

# Other modules
# -N/A


class RangeDict(dict):
    """
    Defines a dictionary that can use immutable iterables such as tuples, as
    keys so that anything in the range can be queried from the dictionary.

    Example:
        >>> range_dict = RangeDict()
        >>> range_dict[(100,105)] = 5
        >>> range_dict[107] = 3
        >>> range_dict[101]
        5
        >>> range_dict.get(101)
        5
        >>> range_dict.get(107)
        3
        >>> range_dict[5]
        Traceback (most recent call last):
          File "/usr/lib/python3.5/code.py", line 91, in runcode
            exec(code, self.locals)
          File "<input>", line 1, in <module>
          File "<input>", line 17, in __getitem__
          File "<input>", line 14, in __missing__
        KeyError: 'Cannot find 5 in RangeDict'
    """
    def __missing__(self, key):
        """
        Method to override inbuilt :func:`__missing__`,
        check if `key` is part of `Iterable` range if if is insert `key`
        in the dict with value of `Iterable` range and return same value.
        .

        Parameters:
            key (:class:`int`): Key to be searched in the dict.

        Returns:
             :class:`int` or :class:`str` or :class:`tuple` or :class:`list`:
                Corresponding value for the `key`.
        Raises:
            :class:`KeyError`: If `key` is not present.
        """
        for _key, _value in self.items():
            if isinstance(_key, Iterable) and not isinstance(_key, str):
                left, right = _key
                if left <= key <= right:
                    self[key] = _value
                    return _value
        raise KeyError("Cannot find {} in RangeDict".format(key))

    def get(self, key):
        """
        Method to override :func:`get`

        Parameters:
            key (:class:`int`): Key to be searched in the dict.

        Returns:
             :class:`int` or :class:`str` or :class:`tuple` or :class:`list` :
                Corresponding value for the `key` if key present.
        Raises:
            :class:`KeyError`: If `key` is not present.
        """
        if key in self:
            return self[key]
        # Key not in dict and is of type `str`
        elif isinstance(key, str):
            raise KeyError("Cannot find key: {} in RangeDict".format(key))
        return self.__missing__(key)


class NAMCSMetaMappings(object):
    """
    Define the field details for each record of NAMCS dataset. Field
    details include field length, field name, field location.

    Example:
        - Fields can be Date_of_visit, Date_of_birth, Year_of_visit,
            Year_of_birth
    """
    def __init__(self, field_length, field_location, field_name):
        """
        Method to construct new object of class.

        Parameters:
            field_length (:class:`int`): Length of field in dataset.
            field_location (:class:`int`): Start index of location of field
                in dataset.
            field_name (:class:`str`): Field name.

        Example:
            >>> obj = NAMCSMetaMappings(2, 1, "Date_of_birth")
            >>> obj.field_location
            1
            >>> obj.field_length
            2
            >>> obj.field_name
            "Date_of_birth"
        """
        self.field_length = field_length
        self.field_location = field_location
        self.field_name = field_name


def detailed_exception_info(method_name=None, use_next_frame=False,
                            logger=None):
    """
    Method to provide detailed information about exception, detail contains
    exception type, file name/module name, operation/line number
    in which exception occurred.

    Parameters:
        use_next_frame (:class:`bool`): To decide whether to use next frame
            `tb_next` of `traceback_obj`, Set to true in case of decorated
            method or method call enclosed in  context manager
            **Default**:const:`False`.
        logger (:class:`logging.Logger`): Log errors to specific log handler.
        method_name (:class:`str`): Method name of method call for which
            exception might occur.
    """
    # Exception details objects
    exception_type, exception_obj, traceback_obj = sys.exc_info()

    # Use the `traceback_frame` based on `use_next_frame`. This will be required
    # when the method is called indirectly from decorator
    if not use_next_frame:
        _frame = traceback_obj.tb_frame
        filename = _frame.f_code.co_filename
        module_globals = _frame.f_globals
        line_no = traceback_obj.tb_lineno
    else:
        _frame = traceback_obj.tb_next
        filename = _frame.tb_frame.f_code.co_filename
        module_globals = _frame.tb_frame.f_globals
        line_no = _frame.tb_lineno

    linecache.checkcache(filename)
    line = linecache.getline(filename, line_no, module_globals)
    if method_name is not None:
        logger.error("Error in method: {}".format(method_name))

    error_msg = "Exception occurred in {} at line {}\nOperation: '{}' ," \
                "exception_object: {}"\
                .format(filename, line_no, line.strip(), exception_obj)
    if logger:
        logger.error(error_msg)
    else:
        print(error_msg)
