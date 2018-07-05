# -*- coding: utf-8 -*-
"""
Module to define decorator(s).
"""
# Python modules
from functools import wraps
import os
import re

# Other modules
from hdx_ahcd.utils.context import try_except

# 3rd party modules
# -N/A

# Global vars
CONVERSION_METHOD_MAPPING = {}  # Key value pair for field and method name


def add_method_to_mapping_dict(method_identifiers):
    """
    Decorator to associate method name with `field_name`. In the form of
    key value pair as `field_name` and method name.

    Parameters:
        method_identifiers (:class:`tuple`): Collection of `field_name` to be
            mapped to method name.

    Returns:
        :class:`function`: Decorated method with method_name mapped
            to all `field_name`, mapping stored in `CONVERSION_METHOD_MAPPING`.

    Example:
     >>> @add_method_to_mapping_dict("gender")
    ... def get_gender():
    ...     # Block of code
    ...     pass
    >>> CONVERSION_METHOD_MAPPING
        {"gender": <function get_gender at 0x7f33644db268>}
    """
    def _add_method_to_mapping_dict(method_to_decorate):
        """
        Inside wrapper to construct key value pair for `method_to_decorate`.

        Parameters:
            method_to_decorate (:class:`function`): Method object.

        Returns:
            :class:`function`: Decorated method.
        """
        nonlocal method_identifiers
        # Avoids cyclic import issue
        from hdx_ahcd.helpers.functions import get_iterable
        method_identifiers = get_iterable(method_identifiers)

        # Adding all method name identifiers
        # to global dict CONVERSION_METHOD_MAPPING
        for identifier in method_identifiers:
            CONVERSION_METHOD_MAPPING[identifier] = method_to_decorate

        @wraps(method_to_decorate)
        def wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`): Positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): Keywords arguments to
                    `method_to_decorate`.

            Returns:
                :class:`object`: Return value of `method_to_decorate`.
            """
            return method_to_decorate(*arg, **kwargs)
        return wrapper
    return _add_method_to_mapping_dict


def catch_exception(re_raise=False):
    """
    Decorator to decorate method name with try except block using `try_except`
    context manager.

    Parameters:
        re_raise (:class:`bool`): To catch exception, perform logging and
            again raise same exception which can be catch in parent block.

    Returns:
        :class:`function`: Decorated method with `try_except` context manager.
    """
    def _catch_exception(method_to_decorate):
        """
        Decorator to decorate method name with try except block using
            `try_except` context manager.

        Parameters:
            method_to_decorate (:class:`function`): Method object.

        Returns:
            :class:`function`: Decorated method with `try_except` context
                manager.
        """
        @wraps(method_to_decorate)
        def _wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`):positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): keywords arguments to
                    `method_to_decorate`.

            Returns:
                :class:`object`: Return value of `method_to_decorate`.
            """
            try:
                with try_except(
                    method_name = method_to_decorate.__name__,
                    re_raise = re_raise
                ):
                    return method_to_decorate(*arg, **kwargs)
            except Exception as exc:

                method_name = None
                # Method is already present in `CONVERSION_METHOD_MAPPING`,
                # find respective field_name
                if method_to_decorate.__name__ in map(
                        lambda method: method.__name__,
                        CONVERSION_METHOD_MAPPING.values()):
                    method_name = list(
                        filter(
                            lambda key:
                            CONVERSION_METHOD_MAPPING[key].__name__ ==
                            method_to_decorate.__name__,
                            CONVERSION_METHOD_MAPPING.keys()
                        )
                    )[0]
                exception_msg = "Exception occurred while mapping '{}' " \
                                "field".format(method_name) \
                    if method_name else str(exc)

                # Since re_raise=True, raise exception again
                raise Exception(exception_msg)
        return _wrapper
    return _catch_exception


def create_path_if_does_not_exists(paths):
    """
    Decorator to create os path(s), if does not exists.

    Parameters:
        paths (:class:`tuple` or :class:`str`): Tuple of `path` to be
            created before executing the method.

    Returns:
        :class:`function`: Decorated method which will create path as
            specified by `paths`, if `paths` does not exists.

    Example:
        >>> @create_path_if_does_not_exists("/var/tmp/temp_directory")
        ... def method_name():
        ...     pass

    """
    def _create_path_if_does_not_exists(method_to_decorate):
        """
        Inside decorator to decorate `method_to_decorate`.

        Parameters:
            method_to_decorate (:class:`function`): Method object.

        Returns:
            :class:`function`: Decorated method.
        """
        nonlocal paths

        # Avoids cyclic import issue
        from hdx_ahcd.helpers.functions import get_iterable
        paths = get_iterable(paths)
        for path in paths:
            # Creating file path if doesn't exist
            if not os.path.exists(path):
                os.makedirs(path)

        @wraps(method_to_decorate)
        def wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`): Positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): Keywords arguments to
                    `method_to_decorate`.

            Returns:
                :class:`object`: Return value of `method_to_decorate`.
            """
            return method_to_decorate(*arg, **kwargs)
        return wrapper
    return _create_path_if_does_not_exists


def enforce_type(*types, return_type=None, use_regex=None):
    """
    Decorator to decorate method to have arguments and return value in specific
    `type` like `str`, `int`, `tuple`, `dict`, also check positional
    arguments for specific regular expression pattern.

    Parameters:
        types (:class:`tuple`): Collection of `type` that needs to enforced
            against positional parameters to the method. The decorated
            method will be then called with positional parameters of
            specified type.
        return_type (:class:`type`): Expected `type` for value returned by
            method call.
        use_regex (:class:`tuple` or :class:`str`): Regular expression pattern
            that needs to be matched against positional arguments.

    Returns:
        :class:`function`: Decorated method.

    Note:
        All checks are enforced against ONLY positional parameters,
        keyword parameters are not supported.
    """
    def _strict_type(method_to_decorate):
        """
        Inside decorator that decorates `method_to_decorate`
        with parameters of specified `type`.

        Parameters:
            method_to_decorate (:class:`function`): Method object.

        Returns:
            :class:`function`: Decorated method.
        """
        @wraps(method_to_decorate)
        def _wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`): Positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): Keywords arguments to
                    `method_to_decorate`.

            Returns:
                :class:`object`: Return value of `method_to_decorate`.
            """
            nonlocal types, return_type, use_regex, method_to_decorate
            method_name = None
            if method_to_decorate.__name__ in map(
                    lambda method: method.__name__,
                    CONVERSION_METHOD_MAPPING.values()
            ):
                method_name = list(
                    filter(
                        lambda key:
                        CONVERSION_METHOD_MAPPING[key].__name__ ==
                        method_to_decorate.__name__,
                        CONVERSION_METHOD_MAPPING.keys()
                    )
                )[0]
            if types and len(arg):
                # Decorator called as @enforce_type((list, tuple))
                if isinstance(types[0], (list, tuple)):
                    types = types[0]
                if len(types) > len(arg):
                    raise Exception(
                        "More positional arguments are required to check type"
                    )

                # Zip will stop as soon as shortest iterable finishes in this
                # case iteration will stop as soon as types finishes,
                # so types will exactly mapped to argument in `arg`
                # positionally.
                for _type, _arg in zip(types, arg):
                    # Skip _arg if type object
                    if _type is not object and not isinstance(_arg, _type):
                        raise Exception(
                            "Method: {} needs positional argument of "
                            "type: {}, actual type is :{}".format(
                                method_to_decorate.__name__,
                                _type,
                                type(_arg)
                            )
                        )
            # Avoids cyclic import issue
            from hdx_ahcd.helpers.functions import get_iterable
            if use_regex is not None and len(arg):
                use_regex = get_iterable(use_regex)

                if len(use_regex) > len(arg):
                    raise Exception(
                        "More positional arguments are required"
                        "to validate against regular expression"
                    )
                if any([isinstance(_regex, int) for _regex in use_regex]):
                    raise Exception(
                        "`use_regex` can not have regex of type`int`"
                    )

                for _regex, _arg in zip(use_regex, arg):
                    # Skip blank regex
                    if _regex != "":
                        try:
                            _regex_pattern = re.compile(_regex)
                            if not re.search(_regex_pattern, str(_arg)):
                                raise Exception(
                                    "Value {} for field {} does not match "
                                    "with specified regex pattern.".format(
                                        _arg, method_name
                                    )
                                )
                        except Exception as ex:
                            raise Exception("Error: {}".format(str(ex)))

            # Call to method
            method_return_value = method_to_decorate(*arg, **kwargs)

            return_type = get_iterable(return_type)
            method_return_value = get_iterable(method_return_value)

            # Method returns less value than expected
            if len(return_type) > len(method_return_value):
                raise Exception(
                    "`return_type` contains more types "
                    "than values returned by method, expected "
                    "return types :{}, values returned by method:{}".format(
                        len(return_type), len(method_return_value)
                    )
                )

            # Zip will stop as soon as shortest iterable finishes in this
            # case iteration will stop as soon as types finishes,
            # so return_type will exactly mapped to value in
            # `method_return_value` positionally.
            for _return_type, _method_return_value in \
                    zip(return_type, method_return_value):
                # Skip _return_type if object
                if _return_type is not object and not isinstance(
                        _method_return_value, _return_type):
                    raise Exception(
                        "Method: {} needs to return value of type"
                        "type:{}, actual type of return value is :{}".format(
                            method_to_decorate.__name__,
                            _return_type,
                            type(_method_return_value)
                        )
                    )

            # Returning method value
            return method_return_value[0] if len(method_return_value) == 1 \
                else method_return_value
        return _wrapper
    return _strict_type
