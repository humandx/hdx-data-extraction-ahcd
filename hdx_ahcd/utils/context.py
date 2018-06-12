# -*- coding: utf-8 -*-
"""
File for all context manager.
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
def try_except(*exceptions, method_name=None, reraise=False):
    """
    Method to catch and report exceptions occurred in block of code using
    context manger.

    Parameters:
        method_name (:class:`str`): Method name for method call enclosed
            in try-except block.
        exceptions (:class: `Exception`): Exceptions that needs to be
            explicitly caught.
        reraise (:class:`bool`): To catch exception, perform logging and
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
        detailed_exception_info(method_name=method_name,
                                use_next_frame = True, logger = log)
        if reraise:
            raise Exception(str(exc))
