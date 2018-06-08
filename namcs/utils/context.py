# -*- coding: utf-8 -*-
"""
File for all context manager.
"""
# Python modules
from contextlib import contextmanager

# 3rd party modules
# -N/A

# Other modules
from namcs.namcs.config import log
from namcs.utils.utils import detailed_exception_info

# Global vars
# -N/A


@contextmanager
def try_except(*exceptions, method_name=None):
    """
    Method to catch and report exceptions occurred in block of code using
    context manger.

    Parameters:
        method_name (:class:`str`): Method name if trying to enclose method call
         in try-except block
        exceptions (:class: `Exception`): Exceptions that needs to be
            explicitly caught.

    Return:
        :class:`generator`: Generator object for method `try_except`.

    Usage:
        with try_except() as handle:
            ""
              Block of code for which exceptions needs to be handled.
            ""
        Block of exception safe code.

    Example:
            # Exception occurred
            with try_except() as handle:
                print("Inside try-exception block")
                print(10/0)
            print("Out of Exception block")

            # Exception not occurred
            with try_except() as handle:
                print("Inside try-exception block")
                print(10/1)
            print("Out of Exception block")

            # Enclosing method call in try except
            with try_except(method = method_to_catch_exception) as handle:
                method_to_catch_exception()
    """
    if not exceptions:
        exceptions = Exception
    try:
        yield
    except exceptions as exc:
        detailed_exception_info(use_next_frame=True)
        if method_name:
            log.error(
                "{} exception encountered while executing {} : {}".format(
                    exc.__class__.__name__, method_name, str(exc))
            )
        else:
            log.error(
                "{} exception encountered : {}".format(
                    exc.__class__.__name__, str(exc))
            )
