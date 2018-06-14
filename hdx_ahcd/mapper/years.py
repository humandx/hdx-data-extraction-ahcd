# -*- coding: utf-8 -*-
"""
Year specific NAMCSMetaMappings for all the namcs year, all years are defined 
by `YEAR_AVAILABLE` config parameter.
"""
# Python modules
import inspect

# Other modules
from hdx_ahcd.namcs.enums import NAMCSFieldEnum
from hdx_ahcd.helpers.functions import get_slice_object
from hdx_ahcd.utils.utils import NAMCSMetaMappings

# 3rd party modules
# -N/A

# Global vars
# -N/A


class Year(object):
    """
    Base class for all classes of NAMCSMetaMappings per year,
    defines method to fetch attributes for specific year.
    """

    @classmethod
    def get_attributes(cls):
        """
        Method to get all attributes defined in class, excluding inbuilt 
        arguments.

        Returns:
            :class:`list`: All explicitly defined attributes of class
        """
        # Inspect for class methods and attributes.
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
            :class:`dict`: Key value pair of field name and corresponding 
                slice operator indicating location of field in raw record.
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
    Year 1973 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "3-4",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    month_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "5-6", 
        field_name = NAMCSFieldEnum.MONTH_OF_BIRTH.value)
    year_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "7-8",
        field_name = NAMCSFieldEnum.YEAR_OF_BIRTH.value)
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "9",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "4",
        field_location = "39-42",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "4",
        field_location = "43-46",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "4",
        field_location = "47-50",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1975(Year1973):
    """
    Year 1975 data with specified fields...

    Note:
        Year 1975 and 1973 have same `NAMCSMetaMappings`.
    """
    pass


class Year1976(Year1973):
    """
    Year 1976 data with specified fields...

    Note:
        Year 1976 and 1973 have same `NAMCSMetaMappings`.
    """
    pass


class Year1977(Year):
    """
    Year 1977 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "3-4",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    month_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "5-6",
        field_name = NAMCSFieldEnum.MONTH_OF_BIRTH.value
    )
    year_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "7-8",
        field_name = NAMCSFieldEnum.YEAR_OF_BIRTH.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "9",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "4",
        field_location = "28-31",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "4",
        field_location = "32-35",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "4",
        field_location = "36-39",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1978(Year1977):
    """
    Year 1978 data with specified fields..

    Note:
        Year 1978 and Year 1977 have same `NAMCSMetaMappings`.
    """
    pass


class Year1979(Year):
    """
    Year 1979 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "3-4",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    month_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "5-6",
        field_name = NAMCSFieldEnum.MONTH_OF_BIRTH.value
    )
    year_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "7-8",
        field_name = NAMCSFieldEnum.YEAR_OF_BIRTH.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "9",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "29-34",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)

    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "35-40",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "41-46",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1980(Year):
    """
    Year 1980 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "3-4",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    month_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "5-6",
        field_name = NAMCSFieldEnum.MONTH_OF_BIRTH.value
    )
    year_of_birth = NAMCSMetaMappings(
        field_length = "2",
        field_location = "7-8",
        field_name = NAMCSFieldEnum.YEAR_OF_BIRTH.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "9",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "40-45",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "46-51",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "52-57",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1981(Year1980):
    """
    Year 1981 data with specified fields..

    Note:
        Year 1981 and Year 1980 have same `NAMCSMetaMappings`.
    """
    pass


class Year1985(Year):
    """
    Year 1985 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "5-6",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "2",
        field_location = "7-8",
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "9",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "57-62",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "63-68",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "69-74",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1989(Year):
    """
    Year 1989 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "5-6",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "2",
        field_location = "7-8",
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "9",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "37-42",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "43-48",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "49-54",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1990(Year1989):
    """
    Year 1990 data with specified fields..

    Note:
        Year 1990 and Year 1989 have same `NAMCSMetaMappings`.
    """
    pass


class Year1991(Year):
    """
    Year 1991 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "5-6",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings(
        field_length = "2",
        field_location = "7-8",
        field_name = NAMCSFieldEnum.PATIENT_AGE.value)
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "9",
        field_name = NAMCSFieldEnum.GENDER.value)
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "39-44",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value)
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "45-50",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value)
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "51-56",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value)
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1992(Year1991):
    """
    Year 1992 data with specified fields..

    Note:
        Year 1992 and Year 1991 have same `NAMCSMetaMappings`.
    """
    pass


class Year1993(Year1991):
    """
    Year 1993 data with specified fields..

    Note:
        Year 1993 and Year 1991 have same `NAMCSMetaMappings`.
    """
    pass


class Year1994(Year1991):
    """
    Year 1994 data with specified fields..

    Note:
        Year 1994 and Year 1991 have same `NAMCSMetaMappings`.
    """
    pass


class Year1995(Year1991):
    """
    Year 1995 data with specified fields..
    """
    age = NAMCSMetaMappings(
        field_length = "3",
        field_location = "7-9",
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "10",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "5",
        field_location = "52-56",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "5",
        field_location = "57-61",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "5",
        field_location = "62-66",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1996(Year1995):
    """
    Year 1996 data with specified fields..

    Note:
        Year 1996 and Year 1995 have same `NAMCSMetaMappings`.
    """
    pass


class Year1997(Year):
    """
    Year 1997 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "4",
        field_location = "3-6",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "3",
        field_location = "8-10",
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1",
        field_location = "11",
        field_name = NAMCSFieldEnum.GENDER.value
    )
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "567-572",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "573-578",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6",
        field_location = "579-584",
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year1998(Year1997):
    """
    Year 1998 data with specified fields..

    Note:
        Year 1998 and Year 1997 have same `NAMCSMetaMappings`.
    """
    pass


class Year1999(Year):
    """
    Year 1999 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2",
        field_location = "1-2",
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value)
    year_of_visit = NAMCSMetaMappings(
        field_length = "4",
        field_location = "3-6",
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value)
    age = NAMCSMetaMappings(
        field_length = "3", 
        field_location = "8-10", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )

    # TODO: implement method convert_physician_diagnosis_code using Character
    # format
    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    # field_length = "5", 
    # field_location = "154-158", 
    # field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    # field_length = "5", 
    # field_location = "159-163", 
    # field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(f
    # field_length = "5", 
    # field_location = "164-168", 
    # field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "577-582", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "583-588", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "589-594", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2000(Year1999):
    """
    Year 2000 data with specified fields..

    Note:
        Year 2000 and Year 1999 have same `NAMCSMetaMappings`.
    """
    pass


class Year2001(Year):
    """
    Year 2001 data with specified fields..
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "4", 
        field_location = "3-6", 
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "3", 
        field_location = "8-10", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    # field_length  = "5", 
    # field_location = "126-130", 
    # field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    # field_length  = "5", 
    # field_location = "131-135", 
    # field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    # field_length  = "5", 
    # field_location = "136-140", 
    # field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "547-552", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "553-558", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "559-564", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2002(Year2001):
    """
    Year 2002 data with specified fields..

    Note:
        Year 2002 and Year 2001 have same `NAMCSMetaMappings`.
    """
    pass


class Year2003(Year2001):
    """
    Year 2003 data with specified fields..

    Note:
        Year 2003 and Year 2001 have same Character format `NAMCSMetaMappings`..
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "723-728", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "729-734", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "735-740", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2004(Year2003):
    """
    Year 2004 data with specified fields.

    Note:
        - Year 2004 and Year 2001 have same Character format `NAMCSMetaMappings`.
        - Year 2004 and Year 2003 have same Numeric format `NAMCSMetaMappings`.
    """
    pass


class Year2005(Year):
    """
    Year 2005 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "4", 
        field_location = "3-6", 
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "3", 
        field_location = "8-10", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "126-130", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "131-135", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "136-140", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "703-708", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "709-714", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "715-720", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2006(Year2005):
    """
    Year 2006 data with specified fields.

    Note:
        Year 2006 and Year 2005 have same Character format `NAMCSMetaMappings`.
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "826-831", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "832-837", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "838-843", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2007(Year):
    """
    Year 2007 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    year_of_visit = NAMCSMetaMappings(
        field_length = "4", 
        field_location = "3-6", 
        field_name = NAMCSFieldEnum.YEAR_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "3", 
        field_location = "8-10", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )
     
    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "55-59", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "60-64", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "65-69", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "909-914", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "915-920", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "921-926", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2008(Year2007):
    """
    Year 2008 data with specified fields.

    Note:
        Year 2008 and Year 2007 have same Character format `NAMCSMetaMappings`.
        Year 2008 and Year 2007 have same Numeric format `NAMCSMetaMappings`.
    """
    pass


class Year2009(Year2007):
    """
    Year 2009 data with specified fields.

    Note:
        Year 2009 and Year 2007 have same Character format `NAMCSMetaMappings`.
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "892-897", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "898-903", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "904-909", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2010(Year2007):
    """
    Year 2010 data with specified fields.

    Note:
        Year 2010 and Year 2007 have same Character format `NAMCSMetaMappings`.
    """
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "919-924", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "925-930", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "931-936", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


# Note: field `Year_of_visit` has been removed from records.
class Year2011(Year):
    """
    Year 2011 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "4-6", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "7", 
        field_name = NAMCSFieldEnum.GENDER.value
    )

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "51-55", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "56-60", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    # 	field_length = "5", 
    # 	field_location = "61-65", 
    # 	field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "919-924", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "925-930", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "931-936", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


# Note:extra field  in record `AGE RECODE`,
# `AGE IN DAYS FOR PATIENTS LESS THAN ONE YEAR OF AGE`, for year 2012
# and onwards
class Year2012(Year):
    """
    Year 2012 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "4-6", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "75-79", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "82-86", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "89-93", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )
    
    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "96-101", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "102-107", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "108-113", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
    )


class Year2013(Year):
    """
    Year 2013 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "4-6", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )
    # 
    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "75-79", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "82-86", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "89-93", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "96-101", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "102-107", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "108-113", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3
)


# Note: new diagnosis fields `DIAGNOSIS 4 ` and `DIAGNOSIS  5` in record
# for year 2014 and onwards
class Year2014(Year):
    """
    Year 2014 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "4-6", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "111-115", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "118-122", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "125-129", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )
    # __physician_diagnosis_4 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "132-136", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value
    # )
    # __physician_diagnosis_5 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "139-143", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value
    # )
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3,
    #     __physician_diagnosis_4,
    #     __physician_diagnosis_5
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "146-151", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "152-157", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "158-163", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    __physician_diagnosis_4 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "164-169", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value
    )
    __physician_diagnosis_5 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "170-175", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3,
        __physician_diagnosis_4,
        __physician_diagnosis_5
    )


class Year2015(Year):
    """
    Year 2015 data with specified fields.
    """
    month_of_visit = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "1-2", 
        field_name = NAMCSFieldEnum.MONTH_OF_VISIT.value
    )
    age = NAMCSMetaMappings(
        field_length = "2", 
        field_location = "4-6", 
        field_name = NAMCSFieldEnum.PATIENT_AGE.value
    )
    sex = NAMCSMetaMappings(
        field_length = "1", 
        field_location = "11", 
        field_name = NAMCSFieldEnum.GENDER.value
    )

    # Character format
    # __physician_diagnosis_1 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "113-117", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    # )
    # __physician_diagnosis_2 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "120-124", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    # )
    # __physician_diagnosis_3 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "127-131", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    # )
    # __physician_diagnosis_4 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "134-138", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value
    # )
    # __physician_diagnosis_5 = NAMCSMetaMappings(
    #     field_length = "5", 
    #     field_location = "141-145", 
    #     field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value
    # )
    # physician_diagnosis = (
    #     __physician_diagnosis_1,
    #     __physician_diagnosis_2,
    #     __physician_diagnosis_3,
    #     __physician_diagnosis_4,
    #     __physician_diagnosis_5
    # )

    # Numeric format
    __physician_diagnosis_1 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "148-153", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_1.value
    )
    __physician_diagnosis_2 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "154-159", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_2.value
    )
    __physician_diagnosis_3 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "160-165", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_3.value
    )
    __physician_diagnosis_4 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "166-171", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_4.value
    )
    __physician_diagnosis_5 = NAMCSMetaMappings(
        field_length = "6", 
        field_location = "172-177", 
        field_name = NAMCSFieldEnum.PHYSICIANS_DIAGNOSIS_5.value
    )
    physician_diagnosis = (
        __physician_diagnosis_1,
        __physician_diagnosis_2,
        __physician_diagnosis_3,
        __physician_diagnosis_4,
        __physician_diagnosis_5
    )
