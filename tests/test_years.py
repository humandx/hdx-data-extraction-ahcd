# -*- coding: utf-8 -*-
"""
Test for `mappers.years` module.
"""
# Python modules
from unittest import TestCase

# Other modules
from hdx_ahcd.mappers.years import (Year1973, Year)
from hdx_ahcd.namcs.enums import NAMCSFieldEnum

# 3rd party modules
# -N/A


class TestYear1973(TestCase):
    """
    Test class for :class:`Year1973`
    """
    def test_get_attributes(self):
        """
        Test for verify method `get_attributes`.
        """
        # Expected attributes
        expected_field_name = [
            NAMCSFieldEnum.MONTH_OF_VISIT.value,
            NAMCSFieldEnum.YEAR_OF_VISIT.value,
            NAMCSFieldEnum.MONTH_OF_BIRTH.value,
            NAMCSFieldEnum.YEAR_OF_BIRTH.value,
            NAMCSFieldEnum.GENDER.value,
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_1.value,
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_2.value,
            NAMCSFieldEnum.PHYSICIANS_DIAGNOSES_3.value,
            NAMCSFieldEnum.VISIT_WEIGHT.value,
        ]

        # Call to func :func:`get_attributes` for Year1973
        actual_attributes = Year1973.get_attributes()
        actual_field_name = []
        for _attr in actual_attributes:
            if type(_attr) in (list, tuple):
                for __attr in _attr:
                    actual_field_name.append(__attr.field_name)
            else:
                actual_field_name.append(_attr.field_name)

        # Asserting :class:`NAMCSMetaMappings` field names
        self.assertSetEqual(set(expected_field_name), set(actual_field_name))

    def test_get_field_slice_mapping(self):
        """
        Test for verify method `get_field_slice_mapping`.
        """
        # Expected slice objects
        expected_slice_objects = {
            "month_of_birth":
                {
                    "start": 4,
                    "stop": 6
                },
            "patient_visit_weight":
                {
                    "start": 70,
                    "stop": 80
                },
            "physician_diagnoses":
                [
                    {
                        "start": 38,
                        "stop": 42,
                    },
                    {
                        "start": 42,
                        "stop": 46,

                    },
                    {
                        "start": 46,
                        "stop": 50
                    }
                ],
            "year_of_visit":
                {
                    "start": 2,
                    "stop": 4,
                },
            "month_of_visit":
                {
                    "start": 0,
                    "stop": 2
                },
            "year_of_birth":
                {
                    "start": 6,
                    "stop": 8
                },
            "sex":
                {
                    "start": 8,
                    "stop": 9
                }
        }
        # Call to func :func:`get_field_slice_mapping` for Year1973
        actual_slice_mappings = Year1973.get_field_slice_mapping()

        actual_slice_objects = {}

        for _attr, actual_slice_object in actual_slice_mappings.items():

            if type(actual_slice_object) in (list, tuple):
                actual_slice_objects[_attr] = \
                    [
                        {
                            "start": _actual_slice_object.start,
                            "stop": _actual_slice_object.stop
                        } for _actual_slice_object in actual_slice_object
                    ]
            else:
                actual_slice_objects[_attr] = \
                    {
                        "start": actual_slice_object.start,
                        "stop": actual_slice_object.stop
                    }

        # Asserting start and stop index for :class:`NAMCSMetaMappings` fields
        self.assertDictEqual(expected_slice_objects, actual_slice_objects)


class TestYear(TestCase):
    """
    Test class for :class:`Year`
    """
    def test_abstract_methods(self):
        """
        Test to validate an exception is raised when subclass of :class:`Year`
        don't implement a abstract attributes.

        Note:
            Abstract attributes are: `gender`, `physician_diagnoses`,
            `visit_weight`, `month_of_visit`.
        """
        # Setup
        # Subclass of :class:`Year`
        class TestClass(Year):
            """
            Class to implement abstract attributes of the :class:`Year`.

            Note:
                This class don't implement abstract attribute:
                `physician_diagnoses`.
            """
            # Using test values for abstract attributes
            gender = "test_gender"
            visit_weight = "test_visit_weight"
            month_of_visit = "test_month_of_visit"

        # Assert for exception is raised when trying to instantiate object of
        # :class:`TestClass`
        with self.assertRaises(TypeError):
            TestClass()

