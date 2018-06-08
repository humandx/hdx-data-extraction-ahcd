# -*- coding: utf-8 -*-
"""
Utility methods for NAMCS data model.
"""
# Python modules
import linecache
import sys
from collections import Iterable

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
        >>> range_dict[(100,105)] =5
        >>> range_dict[107] =3
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
        Method to override __missing__, if key is not present in dict,
        checking if it is present in range of particular key if yes insert new
        key with value as value of that `Iterable` key else Error

        Parameters:
            key (:class:`int`) : Key to be searched in the dict.

        Returns:
             :class:`int` or :class:`str` or :class:`tuple` or :class:`list` :
                Corresponding value for the `key`.
        """
        for _key, _value in self.items():
            if isinstance(_key, Iterable) and not isinstance(_key, str):
                left, right = _key
                if left <= key <= right:
                    self[key] = _value
                    return _value
        raise KeyError('Cannot find {} in RangeDict'.format(key))

    def get(self, key):
        """
        Method to override method get()

        Parameters:
            key (:class:`int`) : Key to be searched in the dict.

        Returns:
             :class:`int` or :class:`str` or :class:`tuple` or :class:`list` :
                Corresponding value for the `key` if key present.
        """
        if key in self:
            return self[key]
        # Key not in dict and is `str`
        elif isinstance(key, str):
            raise KeyError('Cannot find {} in RangeDict'.format(key))
        return self.__missing__(key)


class NAMCSMetaMappings(object):
    """
    Class to define the fields and field details for each column of NAMCS
    dataset, columns are nothing but identifiers for dataset.

    Example:
        - Date_of_visit, Date_of_birth, Year_of_visit, Year_of_birth
    """

    def __init__(self, field_length, field_location, field_name):
        """
        Method to construct new object of class.

        Parameters:
            field_length (:class:`str`): String indicating length of field in
                dataset.
            field_location (:class:`str`): String indicating location of field
                in dataset.
            field_name (:class:`str`): String indicating name of field in
                dataset.

        Example:
            - Mappings("2", "1-2", "Date_of_birth")
                - field_length = 2
                - field_location = "1-2" index at which field data is present
                - field_name = "Date_of_birth" field name
        """
        self.field_length = field_length
        self.field_location = field_location
        self.field_name = field_name


def detailed_exception_info(use_next_frame=False):
    """
    Method to provide detailed information about exception, details contains
    exception type, file name/module name, operation/line number
    in which exception occurred.

    Parameters:
        use_next_frame (:class:`bool`): To decide whether to use next frame
            `tb_next` of `traceback_obj`, Set to true in case of decorated
            method/context manager exception will occur in method itself not in
            decorator/context manager. Default value False.
    """
    # Exception details objects
    exception_type, exception_obj, traceback_obj = sys.exc_info()

    # Decide `traceback_frame`
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
    print('Exception occurred in : {} at line : {}\nOperation : "{}",'
          'exception_object:{}'
          .format(filename, line_no, line.strip(), exception_obj)
          )
