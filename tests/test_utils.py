# -*- coding: utf-8 -*-
"""
Utility methods for NAMCS data model.
"""
# Python modules
from unittest import TestCase, main

# 3rd party modules
# -N/A

# Other modules
from hdx_ahcd.utils.utils import (
    RangeDict,
    NAMCSMetaMappings
)


class RangeDictTest(TestCase):
    """
    Test cases for class RangeDict.
    """
    def test_verify_new_object(self):
        """
        Test for verify correctness of new object.
        """
        # Expected attributes
        expected_keys = \
            [(100, 105), (106, 120), (121, 130), "key_1", "key_2", "key_3"]
        expected_values = \
            ["value_1", "value_2", "value_3", "value_4", "value_5", "value_6"]
        expected_items = [
            ((100, 105), "value_1"),
            ((106, 120), "value_2"),
            ((121, 130), "value_3"),
            ("key_1", "value_4"),
            ("key_2", "value_5"),
            ("key_3", "value_6"),
        ]

        # Creating object of RangeDict and inserting keys in dictionary
        range_dict = RangeDict(
            {
                (100, 105): "value_1",
                (106, 120): "value_2",
                (121, 130): "value_3",
                "key_1": "value_4",
                "key_2": "value_5",
                "key_3": "value_6",
            }
        )

        # Checking operation : "key" is present in dict
        for _key in expected_keys:
            self.assertIn(_key, range_dict)

        # TODO :set
        # Checking operation : get all keys from dict
        self.assertSetEqual(set(expected_keys), set(range_dict.keys()))

        # Checking operation : get all values from dict
        self.assertSetEqual(set(expected_values), set(range_dict.values()))

        # Checking operation : get all items from dict
        self.assertSetEqual(set(expected_items), set(range_dict.items()))

        # Checking operation : get value of key is key is present
        self.assertEqual("value_1", range_dict.get(101))

        # Checking operation : exception is raised if key is not present
        with self.assertRaises(KeyError):
            range_dict.get("value_5")

    def test_verify_new_object_with_iterable_key(self):
        """
        Test for verify correctness of new object when keys are iterable.
        """
        # Expected attributes
        expected_keys = [(100, 105), (106, 120), (121, 130)]
        expected_values = ["value_1", "value_2", "value_3"]
        expected_items = [
            ((100, 105), "value_1"),
            ((106, 120), "value_2"),
            ((121, 130), "value_3")
        ]

        # Creating object of RangeDict and inserting keys in dictionary
        range_dict = RangeDict(
            {
                (100, 105): "value_1",
                (106, 120): "value_2",
                (121, 130): "value_3",
            }
        )

        # Checking operation : "key" is present in dict
        for _key in expected_keys:
            self.assertIn(_key, range_dict)

        # Checking operation : get all keys from dict
        self.assertSetEqual(set(expected_keys), set(range_dict.keys()))

        # Checking operation : get all values from dict
        self.assertSetEqual(set(expected_values), set(range_dict.values()))

        # Checking operation : get all items from dict
        self.assertSetEqual(set(expected_items), set(range_dict.items()))

        # Checking operation : get value of key is key is present
        self.assertEqual("value_1", range_dict.get(101))

        # Checking operation : exception is raised if key is not present
        with self.assertRaises(KeyError):
            range_dict.get("value_5")

    def test_verify_object_with_non_iterable_keys(self):
        """
        Test for verify correctness of new object when non iterable keys are
        inserted.
        """
        # Expected attributes
        expected_dict = {
            "key_1": "value_1",
            "key_2": "value_2",
            "key_3": "value_3",
        }

        expected_keys = ["key_1", "key_2", "key_3"]
        expected_values = ["value_1", "value_2", "value_3"]
        expected_items = \
            [("key_1","value_1"), ("key_2","value_2"), ("key_3","value_3")]

        # Creating object of RangeDict and inserting keys in dictionary
        range_dict = RangeDict(
            {
                "key_1": "value_1",
                "key_2": "value_2",
                "key_3": "value_3",
            }
        )

        # Checking if both dict contains same keys and values
        self.assertDictEqual(expected_dict, range_dict)

        # Checking operation : "key" is present in dict
        for _key in expected_keys:
            self.assertIn(_key, range_dict)

        # Checking operation : get all keys from dict
        self.assertSetEqual(set(expected_keys), set(range_dict.keys()))

        # Checking operation : get all values from dict
        self.assertSetEqual(set(expected_values), set(range_dict.values()))

        # Checking operation : get all items from dict
        self.assertSetEqual(set(expected_items), set(range_dict.items()))

        # Checking operation : get value of key is key is present
        self.assertEqual("value_1", range_dict.get("key_1"))

        # Checking operation : exception is raised if key is not present
        with self.assertRaises(KeyError):
            range_dict.get("key_5")


class NAMCSMetaMappingsTest(TestCase):
    """
    Test cases for class NAMCSMetaMappings.
    """
    def test_verify_new_object(self):
        """
        Test for verify correctness of new object.
        """
        # Expected attributes
        expected_attributes = {
            "test_field_length": "10",
            "test_field_location": "5-6",
            "test_field_name": "test"
        }

        # Creating `NAMCSMetaMappings` object
        namcs_meta_mappings_object = NAMCSMetaMappings(
            field_length = expected_attributes.get("test_field_length"),
            field_location = expected_attributes.get("test_field_location"),
            field_name = expected_attributes.get("test_field_name"),
        )

        # Checking for object attributes
        self.assertEqual(
            expected_attributes.get("test_field_name"),
            namcs_meta_mappings_object.field_name
        )
        self.assertEqual(
            expected_attributes.get("test_field_length"),
            namcs_meta_mappings_object.field_length
        )
        self.assertEqual(
            expected_attributes.get("test_field_location"),
            namcs_meta_mappings_object.field_location
        )

    def test_verify_field_location_without_hyphen(self):
        """
        Test to verify correctness of new object when filed location is
        provided without hyphen.
        """
        # Expected attributes
        expected_attributes = {
            "test_field_length": "10",
            "test_field_location": "5",
            "test_field_name": "test"
        }

        # Creating `NAMCSMetaMappings` object
        namcs_meta_mappings_object = NAMCSMetaMappings(
            field_length = expected_attributes.get("test_field_length"),
            field_location = expected_attributes.get("test_field_location"),
            field_name = expected_attributes.get("test_field_name"),
        )

        # Assert `NAMCSMetaMappings` attributes
        self.assertEqual(
            expected_attributes.get("test_field_name"),
            namcs_meta_mappings_object.field_name
        )
        self.assertEqual(
            expected_attributes.get("test_field_length"),
            namcs_meta_mappings_object.field_length
        )
        self.assertEqual(
            expected_attributes.get("test_field_location"),
            namcs_meta_mappings_object.field_location
        )


if __name__ == '__main__':
    main()