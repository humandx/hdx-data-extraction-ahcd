# -*- coding: utf-8 -*-
"""
Utility methods for NAMCS data model.
"""
# Python modules
from unittest import TestCase

# Other modules
from hdx_ahcd.mapper.years import Year1973
from hdx_ahcd.namcs.enums import NAMCSFieldEnum


# 3rd party modules
# -N/A


class Year1973Test(TestCase):
    """
    Test cases for class Year1973.
    """

    def test_get_attributes(self):
        """
        Test for verify method get_attributes.
        """
        # Expected attributes
        expected_field_name = \
            [
                NAMCSFieldEnum.MONTH_OF_VISIT.value,
                NAMCSFieldEnum.YEAR_OF_VISIT.value,
                NAMCSFieldEnum.MONTH_OF_BIRTH.value,
                NAMCSFieldEnum.YEAR_OF_BIRTH.value,
                NAMCSFieldEnum.GENDER.value,
                NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value,
                NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value,
                NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value,
                NAMCSFieldEnum.VISIT_WEIGHT.value,
            ]

        # Calling method  `get_attributes` for Year1973
        actual_attributes = Year1973.get_attributes()
        actual_field_name = []
        for _attr in actual_attributes:
            if type(_attr) in (list, tuple):
                for __attr in _attr:
                    actual_field_name.append(__attr.field_name)
            else:
                actual_field_name.append(_attr.field_name)

        # Asserting `NAMCSMetaMappings` field names
        self.assertSetEqual(set(expected_field_name), set(actual_field_name))

    def test_get_field_slice_mapping(self):
        """
        Test for verify method get_field_slice_mapping.
        """
        # Expected slice objects
        expected_slice_objects = {
            'month_of_birth': {
                'start': 4,
                'stop': 6
            },
            'patient_visit_weight': {
                'start': 70,
                'stop': 80
            },
            'physician_diagnosis': [
                {
                    'start': 38,
                    'stop': 42,
                },
                {
                    'start': 42,
                    'stop': 46,

                },
                {
                    'start': 46,
                    'stop': 50
                }
            ],
            'year_of_visit': {
                'start': 2,
                'stop': 4,
            },
            'month_of_visit': {
                'start': 0,
                'stop': 2
            },
            'year_of_birth': {
                'start': 6,
                'stop': 8
            },
            'sex': {
                'start': 8,
                'stop': 9
            }
        }
        # Calling method  `get_field_slice_mapping` for Year1973
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

        # Asserting start and stop index for `NAMCSMetaMappings` fields
        self.assertDictEqual(expected_slice_objects, actual_slice_objects)
