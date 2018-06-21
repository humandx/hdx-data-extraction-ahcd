# -*- coding: utf-8 -*-
"""
Module to define context manager(s).
"""
# Python modules
from contextlib import contextmanager

# 3rd party modules
# -N/A

# Other modules
from hdx_ahcd.namcs.config import log
from hdx_ahcd.utils.utils import detailed_exception_info

# Global vars
# -N/A


@contextmanager
def try_except(*exceptions, method_name=None, re_raise=False):
    """
    Method to catch and report exceptions occurred in block of code using
    context manger with try except block.

    Parameters:
        exceptions (:class: `Exception`): Collection of exceptions that
            needs to be explicitly caught.
        method_name (:class:`str`): Method name for method call enclosed
            in try-except block.
        re_raise (:class:`bool`): If true catch exception, perform logging and
            again raise same exception in order to catch in parent block.

    Return:
        :class:`generator`: Generator object for method `try_except`.

    Usage:
        with try_except() as handle:
            ""
              Block of code for which exceptions needs to be handled.
            ""
        Block of exception safe code.

    Example:
        >>> with try_except() as handle:
        ...     print("Inside try-exception block")
        ...     print(10/0)
        ... print("Out of Exception block")
        ...
        >>> with try_except(method = method_to_catch_exception) as handle:
        ...     method_to_catch_exception()
        ...
    """
    exceptions = exceptions if exceptions else Exception
    try:
        yield
    except exceptions as exc:
        # Provide details about exception using method `detailed_exception_info`
        # use_next_frame set to true since exception is raised inside method not
        # in context manger itself
        detailed_exception_info(method_name=method_name,
                                use_next_frame = True, logger = log)
        if re_raise:
            # Since re_raise=True, raise exception again
            raise Exception(str(exc))
