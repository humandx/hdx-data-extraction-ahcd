# -*- coding: utf-8 -*-
"""
Tests for TrackValidationError.
"""
# Python modules
from unittest import TestCase

# 3rd party modules
# -NA-

# HDx modules
from utils.exceptions import TrackValidationError


# Global vars
# -NA-


class TrackValidationErrorTest(TestCase):
    """
    Test cases for TrackValidationError.
    """

    def test_track_validation_error_update(self):
        """
        Test for TrackValidationError update method.
        """
        track_validation_error = TrackValidationError()

        # Test when validation method returns a success
        track_validation_error.update([])
        self.assertEqual(track_validation_error.errors, [])
        self.assertEqual(track_validation_error.is_valid, True)

        # Test when validation method returns a single error
        track_validation_error.update(
            ["Error occured at line 15 : HERE IS YOUR ERROR MESSAGE"])
        self.assertEqual(track_validation_error.errors, [
            "Error occured at line 15 : HERE IS YOUR ERROR MESSAGE"])
        self.assertEqual(track_validation_error.is_valid, False)

        # Test when validation method returns multiple errors
        track_validation_error.update(
            ["Error occured at line 16 : HERE IS YOUR ERROR MESSAGE",
             "Error occured at line 17 : HERE IS YOUR ERROR MESSAGE"])
        self.assertEqual(track_validation_error.errors, [
            "Error occured at line 15 : HERE IS YOUR ERROR MESSAGE",
            "Error occured at line 16 : HERE IS YOUR ERROR MESSAGE",
            "Error occured at line 17 : HERE IS YOUR ERROR MESSAGE"])
        self.assertEqual(track_validation_error.is_valid, False)

        # Test when validation method returns a success after it was already
        # set as failed validation
        track_validation_error.update([])
        self.assertEqual(track_validation_error.errors, [
            "Error occured at line 15 : HERE IS YOUR ERROR MESSAGE",
            "Error occured at line 16 : HERE IS YOUR ERROR MESSAGE",
            "Error occured at line 17 : HERE IS YOUR ERROR MESSAGE"])
        self.assertEqual(track_validation_error.is_valid, False)

    def test_track_validation_error_update_invalid_inputs(self):
        """
        Test for TrackValidationError update method with invalid input value.
        """
        track_validation_error = TrackValidationError()

        # Test when validation method has None error
        with self.assertRaises(TypeError):
            track_validation_error.update(None)

        # Test when validation method has None status
        track_validation_error.update([])
        self.assertEqual(track_validation_error.errors, [])
        self.assertTrue(track_validation_error.is_valid)

    def test_track_validation_error_add(self):
        """
        Test for TrackValidationError add method.
        """
        test_object_1 = TrackValidationError()
        test_object_2 = TrackValidationError()

        # Test when both validation method represents success
        add_result = TrackValidationError.add(test_object_1, test_object_2)
        self.assertEqual(add_result.errors, [])
        self.assertTrue(add_result.is_valid)

        # Test when one validation method represents success
        test_object_1.update(
            ["Error occured at line 15 : HERE IS YOUR ERROR MESSAGE"])
        add_result = TrackValidationError.add(test_object_1, test_object_2)
        self.assertEqual(add_result.errors, [
            "Error occured at line 15 : HERE IS YOUR ERROR MESSAGE"])
        self.assertFalse(add_result.is_valid)

        # Test when both validation method represents failure
        test_object_1.update(
            ["Error occured at line 16 : HERE IS YOUR ERROR MESSAGE"])
        test_object_2.update(
            ["Error occured at line 17 : HERE IS YOUR ERROR MESSAGE"])
        add_result = TrackValidationError.add(test_object_1, test_object_2)
        self.assertEqual(add_result.errors, [
            "Error occured at line 15 : HERE IS YOUR ERROR MESSAGE",
            "Error occured at line 16 : HERE IS YOUR ERROR MESSAGE",
            "Error occured at line 17 : HERE IS YOUR ERROR MESSAGE"])
        self.assertFalse(add_result.is_valid)

    def test_track_validation_error_add_invalid_inputs(self):
        """
        Test for TrackValidationError add method with invalid input object(s).
        """
        test_object_1 = TrackValidationError()
        test_object_2 = TrackValidationError()

        # Test when both validation method represents success
        add_result = TrackValidationError.add(test_object_1, test_object_2)
        self.assertEqual(add_result.errors, [])
        self.assertTrue(add_result.is_valid)

        # Test when one validation method represents success
        test_object_1.update(
            ["Error occured at line 15 : HERE IS YOUR ERROR MESSAGE"])
        add_result = TrackValidationError.add(test_object_1, test_object_2)
        self.assertEqual(add_result.errors, [
            "Error occured at line 15 : HERE IS YOUR ERROR MESSAGE"])
        self.assertFalse(add_result.is_valid)

        # Test when validation method sends None error
        test_object_1.errors = None
        test_object_2.update(
            ["Error occured at line 17 : HERE IS YOUR ERROR MESSAGE"])
        with self.assertRaises(TypeError):
            TrackValidationError.add(test_object_1, test_object_2)
