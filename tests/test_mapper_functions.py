# -*- coding: utf-8 -*-
"""
Tests for mappers.functions module.
"""
# Python modules
from unittest import TestCase

# Third party modules
# -N/A

# Other modules
from hdx_ahcd.mappers.functions import (
    get_age_normalized_to_days,
    convert_physician_diagnoses_code,
    get_gender,
    get_month_from_date,
    get_patient_visit_weight,
    get_year_and_month_from_date,
    get_year_from_date,
)
from hdx_ahcd.namcs.enums import (
    GenderEnum,
    NAMCSFieldEnum
)


class MapperFunctionsTest(TestCase):
    """
    TestCase class for mappers functions.
    """
    def test_get_year_and_month_from_date(self):
        """
        Test to check valid year and month from date.
        """
        # Case 1: When numeric code for year and month is provided in
        # correct format
        # Setup
        date = "0197"
        expected_year = 1997
        expected_month = 1

        # Call to func :func:`get_year_and_month_from_date`
        actual_year, actual_month = get_year_and_month_from_date(date)

        # Assert to check for correct year and month
        self.assertEqual(expected_year, actual_year)
        self.assertEqual(expected_month, actual_month)

        # Case 2: When numeric code for year and month is provided in
        # incorrect format
        # Setup
        date = "0000"

        # Asserting for wrong date format
        with self.assertRaises(expected_exception=(ValueError, Exception)):
            # Call to func :func:`get_year_and_month_from_date`
            actual_year, actual_month = get_year_and_month_from_date(date)

        # Validating decorator enforce_type
        # Setup
        date = 1297

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_year_and_month_from_date`
            actual_year, actual_month = get_year_and_month_from_date(date)

        # Validating use_regex parameter of decorator enforce_type
        # Setup
        date = "1497"  # 14 is invalid month

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_year_and_month_from_date`
            actual_year, actual_month = get_year_and_month_from_date(date)

    def test_convert_physician_diagnosis_code(self):
        """
        Test to validate correct ICD-9 code for raw physician `diagnosis_code`.
        """
        # TODO: this test will change when method get_icd_9_code_from_database
        # will be implemented
        # Setup
        # Case 1: `diagnosis_code` is constant
        diagnosis_code = "Y997"
        expected_icd_9_code = ""

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(expected_icd_9_code, actual_icd_9_code)

        # Case 2: `diagnosis_code` is of 4 length and starts with 1
        diagnosis_code = "1381"
        expected_icd_9_code = "381."

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(expected_icd_9_code, actual_icd_9_code)

        # Case 3: `diagnosis_code` is of 6 length and starts with 1
        diagnosis_code = "138100"
        expected_icd_9_code = "381.00"

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(expected_icd_9_code, actual_icd_9_code)

        # Case 4: `diagnosis_code` is of 4 length and starts with 2
        diagnosis_code = "2010"
        expected_icd_9_code = "V10."

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(expected_icd_9_code, actual_icd_9_code)

        # Case 5: `diagnosis_code` is of 6 length and starts with 2
        diagnosis_code = "201081"
        expected_icd_9_code = "V10.81"

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(expected_icd_9_code, actual_icd_9_code)

        # Case 6: `diagnosis_code` starts with "-"
        diagnosis_code = "-00009"
        expected_icd_9_code = "V00.009"

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(expected_icd_9_code, actual_icd_9_code)

        # Case 7: validating decorator enforce_type
        diagnosis_code = 1111

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`convert_physician_diagnoses_code`
            actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Case 8: validating decorator enforce_type for parameter use_regex
        # Setup
        diagnosis_code = "test_code"  # Invalid diagnosis code

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`convert_physician_diagnoses_code`
            actual_icd_9_code = convert_physician_diagnoses_code(diagnosis_code)

        # Case 9: `diagnosis_code` has fifth digit as "-"
        diagnosis_code = "0010-"
        expected_icd_9_code = "001.00"

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = \
            convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_icd_9_code, actual_icd_9_code
        )

        # Case 10: `diagnosis_code` has fourth digit as "-"
        diagnosis_code = "082-9"
        expected_icd_9_code = "082.09"

        # Call to func :func:`convert_physician_diagnoses_code`
        actual_icd_9_code = \
            convert_physician_diagnoses_code(diagnosis_code)

        # Assert for valid ICD-9 code
        self.assertEqual(
            expected_icd_9_code, actual_icd_9_code
        )

    def test_get_month_from_date(self):
        """
        Test to check valid month from date.
        """
        # Case 1: when numeric code for month is correct
        # Setup
        date = "03"
        expected_month = 3

        # Call to func :func:`get_month_from_date`
        actual_month = get_month_from_date(date)

        # Assert to check for correct month
        self.assertEqual(expected_month, actual_month)

        # Case 2: when numeric code for month is wrong
        # Setup
        date = "00"

        # Asserting for wrong date format
        with self.assertRaises(expected_exception=(ValueError, Exception)):
            # Call to func :func:`get_month_from_date`
            actual_month = get_month_from_date(date)

        # Validating decorator enforce_type
        # Setup
        date = 12

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_month_from_date`
            actual_month = get_month_from_date(date)

        # Validating use_regex parameter of decorator enforce_type
        # Setup
        date = "14"  # 14 is invalid month

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_month_from_date`
            actual_month = get_month_from_date(date)

    def test_get_year_from_date(self):
        """
        Test to check valid month from date.
        """
        # Case 1: when numeric code for year is correct
        # Setup
        date = "97"
        expected_year = 1997

        # Call to func :func:`get_year_from_date`
        actual_year = get_year_from_date(date)

        # Assert to check for correct year
        self.assertEqual(expected_year, actual_year)

        # Case 2: When year needs to be calculated from source_file_id
        required_fields_to_calculate_age = {
            NAMCSFieldEnum.SOURCE_FILE_ID.value: "2011_NAMCS",
        }
        expected_year = 2011

        # Call to func :func:`get_year_from_date`
        actual_year = get_year_from_date(**required_fields_to_calculate_age)

        # Assert to check for correct year
        self.assertEqual(expected_year, actual_year)

        # Validating use_regex parameter of decorator enforce_type
        # Setup
        date = "-10"  # -10 is invalid year

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_year_from_date`
            actual_month = get_year_from_date(date)

        # Validating decorator enforce_type
        # Setup
        date = 12

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_year_from_date`
            actual_month = get_year_from_date(date)

    def test_get_gender(self):
        """
        Test to validate correct gender name for integer representing gender.
        """
        # Setup
        gender = "1"
        expected_gender_value = GenderEnum.FEMALE.value

        # Call to func :func:`get_gender`
        actual_gender_value = get_gender(gender)

        # Assert to check correctness of gender value
        self.assertEqual(expected_gender_value, actual_gender_value)

        # Setup
        gender = "2"
        expected_gender_value = GenderEnum.MALE.value

        # Call to func :func:`get_gender`
        actual_gender_value = get_gender(gender)

        # Assert to check correctness of gender value
        self.assertEqual(expected_gender_value, actual_gender_value)

        # Validating decorator enforce_type
        # Setup
        gender = 12

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_gender`
            actual_gender_value = get_gender(gender)

        # Validating use_regex parameter of decorator enforce_type
        # Setup
        gender = "5"  # Gender "5" is invalid gender

        # Assert for exception raised from decorator
        with self.assertRaises(Exception):
            # Call to func :func:`get_gender`
            actual_gender_value = get_gender(gender)

    def test_get_age_normalized_to_days(self):
        """
        Test to validate age normalized to days.
        """
        # Case 1: When age is numeric value
        # Setup
        age = "33"
        expected_age_in_days = 12045.0

        # Call to func :func:`get_age_normalized_to_days`
        actual_age_in_days = get_age_normalized_to_days(age)

        # Assert to check correctness of age in days
        self.assertEqual(expected_age_in_days, actual_age_in_days)

        # Case 2: When age needs to be calculated from date of visit and
        # date of birth
        required_fields_to_calculate_age = {
            NAMCSFieldEnum.MONTH_OF_VISIT.value: 6,
            NAMCSFieldEnum.YEAR_OF_VISIT.value: 1974,
            NAMCSFieldEnum.MONTH_OF_BIRTH.value: 5,
            NAMCSFieldEnum.YEAR_OF_BIRTH.value: 1910,
        }
        expected_age_in_days = 23407.0

        # Call to func :func:`get_age_normalized_to_days`
        actual_age_in_days = \
            get_age_normalized_to_days(**required_fields_to_calculate_age)

        # Assert to check correctness of age in days
        self.assertEqual(expected_age_in_days, actual_age_in_days)

    def test_get_patient_visit_weight(self):
        """
        Test to validate patient visit weight.
        """
        # Case 1: When visit weight is integer value of length 10.
        # Setup
        visit_weight = "0000019129"
        expected_visit_weight = 19129.0

        # Call to func :func:`get_patient_visit_weight`
        actual_visit_weight = get_patient_visit_weight(visit_weight)

        # Assert to check patient visit weight
        self.assertEqual(expected_visit_weight, actual_visit_weight)

        # Case 2: When visit weight is integer value of length 11.
        # Setup
        visit_weight = "00000191129"
        expected_visit_weight = 191129.0

        # Call to func :func:`get_patient_visit_weight`
        actual_visit_weight = get_patient_visit_weight(visit_weight)

        # Assert to check patient visit weight
        self.assertEqual(expected_visit_weight, actual_visit_weight)

        # Case 3: When visit weight is float value of length 5.
        # Setup
        visit_weight = "15.62"
        expected_visit_weight = 15.62

        # Call to func :func:`get_patient_visit_weight`
        actual_visit_weight = get_patient_visit_weight(visit_weight)

        # Assert to check patient visit weight
        self.assertEqual(expected_visit_weight, actual_visit_weight)

        # Case 4: When visit weight is float value of length 6.
        # Setup
        visit_weight = "152.62"
        expected_visit_weight = 152.62

        # Call to func :func:`get_patient_visit_weight`
        actual_visit_weight = get_patient_visit_weight(visit_weight)

        # Assert to check patient visit weight
        self.assertEqual(expected_visit_weight, actual_visit_weight)

        # Case 5: When visit weight is invalid
        # Setup
        visit_weight = "000..19129"

        # Assert for exception
        with self.assertRaises((ValueError, Exception)):
            # Call to func :func:`get_patient_visit_weight`
            actual_visit_weight = get_patient_visit_weight(visit_weight)



