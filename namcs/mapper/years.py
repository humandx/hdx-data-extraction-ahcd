# -*- coding: utf-8 -*-
"""
Module containing year specific NAMCSMetaMappings for all the years in
`YEAR_AVAILABLE` config parameter.
"""
# Python modules
import inspect

# Other modules
from namcs.enums import NAMCSFieldEnum
from helpers.functions import get_slice_object
from utils.utils import NAMCSMetaMappings


# 3rd party modules
# -N/A


# Global vars
# -N/A


class Year(object):
    """
    Base class for all classes of NAMCSMetaMappings per year
    """

    @classmethod
    def get_attributes(cls):
        """
        Method to get all class attributes

        Returns:
            :class:`tuple`: tuple containing all class variables
        """
        attributes = dict(inspect.getmembers(cls,
                                             lambda attribute: not (
                                                 inspect.isroutine(attribute))))
        return [
            attributes.get(attr) for attr in attributes if not (
                    attr.endswith('_') or attr.startswith('_')
            )
        ]

    @classmethod
    def get_field_slice_mapping(cls):
        """
        Method to get mappings for field of year and corresponding
        slice operator

        Returns:
            :class:`dict`: dict containing mappings as field name
            and corresponding slice operator
        """
        mappings_dict = {}
        for mapping in cls.get_attributes():
            if type(mapping) in (list, tuple):
                """
                Unpacking the tuple to create individual key in `mappings_dict`
                Example:
                    physician_diagnosis = (
                      __physician_diagnosis_1,
                      __physician_diagnosis_2,
                      __physician_diagnosis_3,
                    )
                """

                # Removing fields those already present in `mappings_dict`
                for clubbed_mapping in mapping:
                    if clubbed_mapping.field_name in mappings_dict:
                        del mappings_dict[clubbed_mapping.field_name]

                mappings_dict[mapping[0].field_name] = [
                    get_slice_object(
                        clubbed_mapping.field_location.split("-")
                    )
                    for clubbed_mapping in mapping
                ]
            else:
                indexes = mapping.field_location.split("-")

                # Avoiding over writing the value of existing key
                if mapping.field_name not in mappings_dict:
                    mappings_dict[mapping.field_name] = \
                        get_slice_object(indexes)
        return mappings_dict


class Year1973(Year):
    """
    Year 1973 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("2", "3-4",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    month_of_birth = NAMCSMetaMappings("2", "5-6",
                                       NAMCSFieldEnum.MONTH_OF_BIRTH.value)
    year_of_birth = NAMCSMetaMappings("2", "7-8",
                                      NAMCSFieldEnum.YEAR_OF_BIRTH.value)
    sex = NAMCSMetaMappings("1", "9", NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "4", "39-42", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "4", "43-46", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "4", "47-50", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1975(Year1973):
    """
    Year 1975 data with specified fields

    Note:
        Year 1975 and 1973 have same `NAMCSMetaMappings`
    """
    pass


class Year1976(Year1973):
    """
    Year 1976 data with specified fields

    Note:
        Year 1976 and 1973 have same `NAMCSMetaMappings`
    """
    pass


class Year1977(Year):
    """
    Year 1977 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("2", "3-4",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    month_of_birth = NAMCSMetaMappings("2", "5-6",
                                       NAMCSFieldEnum.MONTH_OF_BIRTH.value)
    year_of_birth = NAMCSMetaMappings("2", "7-8",
                                      NAMCSFieldEnum.YEAR_OF_BIRTH.value)
    sex = NAMCSMetaMappings("1", "9", NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "4", "28-31", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "4", "32-35", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "4", "36-39", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1978(Year1977):
    """
    Year 1978 data with specified fields

    Note:
        Year 1978 and Year 1977 have same `NAMCSMetaMappings`
    """
    pass


class Year1979(Year):
    """
    Year 1979 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("2", "3-4",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    month_of_birth = NAMCSMetaMappings("2", "5-6",
                                       NAMCSFieldEnum.MONTH_OF_BIRTH.value)
    year_of_birth = NAMCSMetaMappings("2", "7-8",
                                      NAMCSFieldEnum.YEAR_OF_BIRTH.value)
    sex = NAMCSMetaMappings("1", "9", NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "29-34", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "35-40", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "41-46", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1980(Year):
    """
    Year 1980 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("2", "3-4",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    month_of_birth = NAMCSMetaMappings("2", "5-6",
                                       NAMCSFieldEnum.MONTH_OF_BIRTH.value)
    year_of_birth = NAMCSMetaMappings("2", "7-8",
                                      NAMCSFieldEnum.YEAR_OF_BIRTH.value)
    sex = NAMCSMetaMappings("1", "9", NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "40-45", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "46-51", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "52-57", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1981(Year1980):
    """
    Year 1981 data with specified fields

    Note:
        Year 1981 and Year 1980 have same `NAMCSMetaMappings`
    """
    pass


class Year1985(Year):
    """
    Year 1985 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("2", "5-6",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "7-8", "age")
    sex = NAMCSMetaMappings("1", "9", NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "57-62", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "63-68", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "69-74", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1989(Year):
    """
    Year 1989 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("2", "5-6",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "7-8", "age")
    sex = NAMCSMetaMappings("1", "9", NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "37-42", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "43-48", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "49-54", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1990(Year1989):
    """
    Year 1990 data with specified fields

    Note:
        Year 1990 and Year 1989 have same `NAMCSMetaMappings`
    """
    pass


class Year1991(Year):
    """
    Year 1991 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("2", "5-6",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "7-8", "age")
    sex = NAMCSMetaMappings("1", "9", NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "39-44", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "45-50", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "51-56", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1992(Year1991):
    """
    Year 1992 data with specified fields

    Note:
        Year 1992 and Year 1991 have same `NAMCSMetaMappings`
    """
    pass


class Year1999(Year):
    """
    Year 1999 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("4", "3-6",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings("3", "8-10", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # TODO: implement method convert_physician_diagnosis_code using Character
    # format
    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "154-158", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "159-163", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "164-168", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "577-582", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "583-588", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "589-594", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2000(Year1999):
    """
    Year 2000 data with specified fields

    Note:
        Year 2000 and Year 1999 have same `NAMCSMetaMappings`
    """
    pass


class Year2001(Year):
    """
    Year 2001 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("4", "3-6",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings("3", "8-10", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "126-130", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "131-135", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "136-140", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "547-552", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "553-558", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "559-564", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2002(Year2001):
    """
    Year 2002 data with specified fields

    Note:
        Year 2002 and Year 2001 have same `NAMCSMetaMappings`
    """
    pass


class Year2003(Year2001):
    """
    Year 2003 data with specified fields

    Note:
        Year 2003 and Year 2001 have same Character format `NAMCSMetaMappings`
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "723-728", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "729-734", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "735-740", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2004(Year2003):
    """
    Year 2004 data with specified fields

    Note:
        - Year 2004 and Year 2001 have same Character format `NAMCSMetaMappings`
        - Year 2004 and Year 2003 have same Numeric format `NAMCSMetaMappings`
    """
    pass


class Year2005(Year):
    """
    Year 2005 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("4", "3-6",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings("3", "8-10", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "126-130", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "131-135", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "136-140", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "703-708", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "709-714", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "715-720", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2006(Year2005):
    """
    Year 2006 data with specified fields

    Note:
        Year 2006 and Year 2005 have same Character format `NAMCSMetaMappings`
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "826-831", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "832-837", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "838-843", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2007(Year):
    """
    Year 2007 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings("4", "3-6",
                                      NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings("3", "8-10", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "55-59", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "60-64", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "65-69", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "909-914", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "915-920", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "921-926", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2008(Year2007):
    """
    Year 2008 data with specified fields

    Note:
        Year 2008 and Year 2007 have same Character format `NAMCSMetaMappings`
        Year 2008 and Year 2007 have same Numeric format `NAMCSMetaMappings`
    """
    pass


class Year2009(Year2007):
    """
    Year 2009 data with specified fields

    Note:
        Year 2009 and Year 2007 have same Character format `NAMCSMetaMappings`
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "892-897", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "898-903", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "904-909", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2010(Year2007):
    """
    Year 2010 data with specified fields

    Note:
        Year 2010 and Year 2007 have same Character format `NAMCSMetaMappings`
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "919-924", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "925-930", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "931-936", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


# Note: field `Year_of_visit` in document  NOT present
class Year2011(Year):
    """
    Year 2011 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "4-6", "age")
    sex = NAMCSMetaMappings("1", "7", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "51-55", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "56-60", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "61-65", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "919-924", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "925-930", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "931-936", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


# Note:extra field  in document `AGE RECODE`,
# `AGE IN DAYS FOR PATIENTS LESS THAN ONE YEAR OF AGE` onwards
class Year2012(Year):
    """
    Year 2012 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "4-6", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "75-79", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "82-86", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "89-93", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "96-101", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "102-107", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "108-113", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2013(Year):
    """
    Year 2013 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "4-6", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "75-79", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "82-86", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "89-93", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "96-101", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "102-107", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "108-113", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


# Note: new diagnosis fields `DIAGNOSIS 4 ` and `DIAGNOSIS  5` onwards
class Year2014(Year):
    """
    Year 2014 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "4-6", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "111-115", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "118-122", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "125-129", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    # __physician_diagnosis_4 = NAMCSMetaMappings(
    #     "5", "132-136", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value)
    # __physician_diagnosis_5 = NAMCSMetaMappings(
    #     "5", "139-143", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value)
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3,
    #     __physician_diagnosis_4,
    #     __physician_diagnosis_5
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "146-151", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "152-157", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "158-163", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    __physician_diagnosis_4 = NAMCSMetaMappings(
        "6", "164-169", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value)
    __physician_diagnosis_5 = NAMCSMetaMappings(
        "6", "170-175", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3,
        __physician_diagnosis_4,
        __physician_diagnosis_5
    )


class Year2015(Year):
    """
    Year 2015 data with specified fields
    """
    month_of_visit = NAMCSMetaMappings("2", "1-2",
                                       NAMCSFieldEnum.MONTH_OF_VISIT.value)
    age = NAMCSMetaMappings("2", "4-6", "age")
    sex = NAMCSMetaMappings("1", "11", NAMCSFieldEnum.GENDER.value)

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     "5", "113-117", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     "5", "120-124", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     "5", "127-131", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    # __physician_diagnosis_4 = NAMCSMetaMappings(
    #     "5", "134-138", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value)
    # __physician_diagnosis_5 = NAMCSMetaMappings(
    #     "5", "141-145", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value)
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3,
    #     __physician_diagnosis_4,
    #     __physician_diagnosis_5
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        "6", "148-153", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        "6", "154-159", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        "6", "160-165", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    __physician_diagnosis_4 = NAMCSMetaMappings(
        "6", "166-171", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value)
    __physician_diagnosis_5 = NAMCSMetaMappings(
        "6", "172-177", NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3,
        __physician_diagnosis_4,
        __physician_diagnosis_5
    )
