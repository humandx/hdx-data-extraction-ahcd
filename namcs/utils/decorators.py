# -*- coding: utf-8 -*-
"""
Decorator file containing all decorators.
"""
# Python modules
import os

# HDx modules
from .context import try_except

# 3rd party modules
# -N/A


# Global vars
CONVERSION_METHOD_MAPPING = {}  # Dict to for field name and method MAPPINGS


def add_method_to_mapping_dict(method_identifiers):
    """
    Decorator to associate method name with `field_name`.

    Parameters:
        method_identifiers (:class:`tuple`): Tuple of `field_name` to be
            mapped to method name.

    Returns:
        :class:`function`: Decorated method with method_name mapped
            to all `field_name`, mapping stored in `CONVERSION_METHOD_MAPPING`.

    Example:
            @add_method_to_mapping_dict("age")
            def age(*arg, **kargs):
                "
                    Block of code
                "
                return
    """

    def _add_method_to_mapping_dict(method_to_decorate):
        """
        Inside decorator to decorate `method_to_decorate`.

        Parameters:
            method_to_decorate (:class:`function`): Method object.

        Returns:
            :class:`function`: Decorated method.
        """
        if isinstance(method_identifiers, (list, tuple)):
            # Adding all method name identifiers to global dict of MAPPINGS
            for identifier in method_identifiers:
                CONVERSION_METHOD_MAPPING[identifier] = method_to_decorate
        elif isinstance(method_identifiers, str):
            CONVERSION_METHOD_MAPPING[method_identifiers] = method_to_decorate

        def wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`): Positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): Keywords arguments to
                    `method_to_decorate`.

            Returns:
                :class:`function`: Wrapper method.
            """
            return method_to_decorate(*arg, **kwargs)

        return wrapper

    return _add_method_to_mapping_dict


def catch_exception(reraise=False):
    """
    Decorator to decorate method name with try except block using `try_except`
    context manager.

    Parameters:
        reraise (:class:`bool`): Set False to handle the exception.

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

        def _wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`):positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): keywords arguments to
                    `method_to_decorate`.

            Returns:
                class:`function`: Wrapper method.
            """
            if reraise:
                try:
                    return method_to_decorate(*arg, **kwargs)
                except Exception as exc:
                    if method_to_decorate.__name__ in CONVERSION_METHOD_MAPPING:
                        raise \
                            Exception(
                                "Exception occurred while mapping '{}' field".
                                    format(
                                        list(
                                            filter(
                                                lambda key:
                                                CONVERSION_METHOD_MAPPING[key]
                                                == method_to_decorate.__name__,
                                                CONVERSION_METHOD_MAPPING.keys()
                                            )
                                        )[0]
                                    )
                            )
                    else:
                        raise Exception(str(exc))
            with try_except(method_name=method_to_decorate.__name__):
                return method_to_decorate(*arg, **kwargs)

        return _wrapper

    return _catch_exception


def create_path_if_does_not_exists(paths):
    """
    Decorator to create os path, if does not exists.

    Parameters:
        paths (:class:`tuple` or :class:`str`): Tuple of `path` to be
            created before executing the method.

    Returns:
        :class:`function`: Decorated method which will create path as
        specified by `paths`, if does not exists.

    Example:
            @create_path_if_does_not_exists(EXTRACTED_DATA_DIR_PATH)
            def read_all_data(*arg, **kargs):
                "
                    Block of code
                "
                return
    """

    def _create_path_if_does_not_exists(method_to_decorate):
        """
        Inside decorator to decorate `method_to_decorate`.

        Parameters:
            method_to_decorate (:class:`function`): Method object.

        Returns:
            :class:`function`: Decorated method.
        """
        # Creating file path if doesn't exist
        if isinstance(paths, (list, tuple)):
            for path in paths:
                if not os.path.exists(path):
                    os.makedirs(path)
        elif isinstance(paths, str):
            if not os.path.exists(paths):
                os.makedirs(paths)

        def wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`): Positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): Keywords arguments to
                    `method_to_decorate`.

            Returns:
                :class:`function`: Wrapper method.
            """
            return method_to_decorate(*arg, **kwargs)

        return wrapper

    return _create_path_if_does_not_exists


def enforce_type(*types, return_type=None):
    """
    Decorator to decorate method to have arguments and return value in specific
    `type` like `str`, `int`, `tuple`, `object`

    Parameters:
        types (:class:`tuple`): Collection of `type` that needs to enforced
            against positional parameters to the method. The decorated
            method will be then called with positional parameters with
            specified type.
        return_type (:class:`type`): expected `type` for value returned by
            method call.

    Returns:
        :class:`function`: Decorated method.
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
        def _wrapper(*arg, **kwargs):
            """
            Inside wrapper.

            Parameters:
                arg (:class:`tuple`):positional arguments to
                    `method_to_decorate`.
                kwargs (:class:`dict`): keywords arguments to
                    `method_to_decorate`.

            Returns:
                class:`function`: Wrapper method.
            """
            nonlocal types
            if types:
                # Decorator called as @enforce_type((list, tuple))
                if isinstance(types[0], (list, tuple)):
                    types = types[0]
                if len(types) > len(arg):
                    raise Exception('More positional arguments are required '
                                    'to type cast')

                # Zip will stop as soon as shortest iterable finishes in this
                # case iteration will stop as soon as types finishes,
                # so types will exactly mapped to argument in `arg`
                # positionally.
                for _type, _arg in zip(types, arg):
                    # Skip _arg if type object
                    if _type is not object:
                        if not isinstance(_arg, _type):
                            raise Exception(
                                'Method: {} needs positional argument of '
                                'type:{}, actual type is :{}'.format(
                                    method_to_decorate.__name__,
                                    _type,
                                    type(_arg)
                                )
                            )

            # Call to method
            method_return_value = method_to_decorate(*arg, **kwargs)

            if return_type is not object:
                if not isinstance(method_return_value, return_type):
                    raise Exception(
                        'Method: {} needs to return value of type'
                        'type:{}, actual type of return value is :{}'.format(
                            method_to_decorate.__name__,
                            return_type,
                            type(method_return_value)
                        )
                    )
            return method_return_value
        return _wrapper
    return _strict_type