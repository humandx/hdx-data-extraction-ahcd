# -*- coding: utf-8 -*-
"""
This file contains parameters related to initialization of package.
"""
# Other modules
from hdx_ahcd.controllers.namcs_processors import NAMCSProcessor as \
    __Processor

# 3rd party modules
# -N/A


def get_cleaned_data_by_year(**kwargs):
    """
    API to process NAMCS dataset file(s).

    Args:
        **kwargs (:class:`dict`) : Following are permissible parameters.
            year (:class:`int` or :class:`tuple` or :class:`list`): NAMCS year.
            file_name (:class:`str`): NAMCS raw dataset file name.
            do_validation (:class:`bool`): Flag to indicate if perform
                validation on `year` and `file_name` default value True to
                perform validation.
            do_export (:class:`bool`) : Flag to indicate if to dump the
                converted raw NAMCS patient case data into CSV file as
                defined by `CONVERTED_CSV_FILE_NAME_SUFFIX` for
                given year default value False.
            force_download (:class:`bool`) : Whether to force download
                NAMCS raw dataset file even if it exists,Default value False.
    Returns:
        :class:`defaultdict`: Dictionary containing
            generator of converted raw NAMCS patient case data
            for given year, if any errors occurred, log errors and return
            empty dict.
    Usage:
    Case 1: Downloading NAMCS data for single year (say, 1973). If the file is
        already present in the downloaded_files then process the downloaded
        file.
    >>> import pprint
    >>> import hdx_ahcd
    >>> from hdx_ahcd.api import get_cleaned_data_by_year
    >>> pp =pprint.PrettyPrinter(indent=4)
    >>> gen =  get_cleaned_data_by_year(year=1973)
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov
    /pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe for year:1973
    >>> pp.pprint(gen)
    defaultdict(<class 'dict'>,
            {   1973: {   'generator': <generator object
            get_generator_by_year at 0x7fe4b6480150>,
                          'source_file_info': {
                          'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS
                          /namcs_public_use_files/namcs73.exe',
                          'year': '73',
                          'zip_file_name': 'namcs73.exe'}}})

    Case 2: Downloading NAMCS data for multiple years (say, 1973 and 1975).
        If the file is already present in the downloaded_files then process the
        downloaded file.
    >>> gen =  get_cleaned_data_by_year(year= (1973,1975))
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov
    /pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe for year:1975
    >>> pp.pprint(gen)
    defaultdict(<class 'dict'>,
                {   1973: {   'generator': <generator object
                get_generator_by_year at 0x7fe4b5fa9e08>,
                              'source_file_info': {
                              'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics
                              /NCHS/namcs_public_use_files/namcs73.exe',
                              'year': '73',
                              'zip_file_name': 'namcs73.exe'}},
                    1975: {   'generator': <generator object
                    get_generator_by_year at 0x7fe4b45e7e60>,
                              'source_file_info': {
                              'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics
                              /NCHS/namcs_public_use_files/namcs75.exe',
                              'year': '75',
                              'zip_file_name': 'namcs75.exe'}}})
    >>> pp.pprint(next(gen.get(1973).get('generator')))
    {   'age': 22889,
        'month_of_visit': 'June',
        'patient_visit_weight': 13479.0,
        'physician_diagnoses': ['470.0', 'V03.2', ''],
        'sex': 'Female',
        'source_file_ID': '1973_NAMCS',
        'source_file_row': 1,
        'year_of_visit': '1973'}
    >>> pp.pprint(next(gen.get(1975).get('generator')))
    {   'age': 14610,
        'month_of_visit': 'April',
        'patient_visit_weight': 3722.0,
        'physician_diagnoses': ['492.0', '', ''],
        'sex': 'Male',
        'source_file_ID': '1975_NAMCS',
        'source_file_row': 1,
        'year_of_visit': '1975'}

    Case 3: Forcefully download and then process the NAMCS data for multiple
        years (say, 1973 and 1975).
    >>> gen =  get_cleaned_data_by_year(year= (1973,1975), force_download=True)
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics
    /NCHS/namcs_public_use_files/namcs73.exe for year:1973
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics
    /NCHS/namcs_public_use_files/namcs75.exe for year:1975
    >>> pp.pprint(gen)
    defaultdict(<class 'dict'>,
                {   1973: {   'generator': <generator object
                get_generator_by_year at 0x7fe4b5fa9e08>,
                              'source_file_info': {
                              'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics
                              /NCHS/namcs_public_use_files/namcs73.exe',
                              'year': '73',
                              'zip_file_name': 'namcs73.exe'}},
                    1975: {   'generator': <generator object
                    get_generator_by_year at 0x7fe4b45e7e60>,
                              'source_file_info': {
                              'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics
                              /NCHS/namcs_public_use_files/namcs75.exe',
                              'year': '75',
                              'zip_file_name': 'namcs75.exe'}}})

    Case 4: Forcefully download and then export the processed NAMCS data for
        multiple years (say, 1973 and 1975) in separate csv files.
    >>> gen =  get_cleaned_data_by_year(year= (1973,1975), force_download=True,
        do_export=True)
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics
    /NCHS/namcs_public_use_files/namcs73.exe for year:1973
    INFO:hdx_ahcd:Finished writing to the file /home/velotio/.hdx_ahcd
    /data/1973_NAMCS_CONVERTED.csv
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics
    /NCHS/namcs_public_use_files/namcs75.exe for year:1975
    INFO:hdx_ahcd:Finished writing to the file /home/velotio/.hdx_ahcd/data/
    1975_NAMCS_CONVERTED.csv
    >>> pp.pprint(gen)
    defaultdict(<class 'dict'>,
            {   1973: {   'file_name': '/home/velotio/.hdx_ahcd/data
                            /1973_NAMCS_CONVERTED.csv',
                          'generator': <generator object
                          get_generator_by_year at 0x7fe4b6480150>,
                          'source_file_info': {
                          'url': 'ftp://ftp.cdc.gov
                          /pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe',
                          'year': '73',
                          'zip_file_name': 'namcs73.exe'}},
                1975: {   'file_name': '/home/velotio/.hdx_ahcd/data/
                            1975_NAMCS_CONVERTED.csv',
                          'generator': <generator object
                          get_generator_by_year at 0x7fe4b45e7e60>,
                          'source_file_info': {   '
                          url': 'ftp://ftp.cdc.gov/pub/Health_Statistics
                          /NCHS/namcs_public_use_files/namcs75.exe',
                          'year': '75',
                          'zip_file_name': 'namcs75.exe'}}})

    Case 5: Forcefully download and then export the processed NAMCS data for all
        years.
    >>> gen =  get_cleaned_data_by_year(force_download=True)
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe for year:1973
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe for year:1975
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs76.exe for year:1976
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs77.exe for year:1977
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs78.exe for year:1978
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs79.exe for year:1979
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs80.exe for year:1980
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs81.exe for year:1981
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs85.exe for year:1985
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs89.exe for year:1989
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs90.exe for year:1990
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs92.exe for year:1992
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs93.exe for year:1993
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs94.exe for year:1994
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs95.exe for year:1995
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs96.exe for year:1996
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs97.exe for year:1997
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs98.exe for year:1998
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs99.exe for year:1999
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS00.exe for year:2000
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS01.exe for year:2001
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS02.exe for year:2002
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS03.exe for year:2003
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS04.exe for year:2004
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS05.exe for year:2005
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS06.exe for year:2006
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS07.exe for year:2007
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS08.exe for year:2008
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS09.exe for year:2009
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2010.exe for year:2010
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2011.zip for year:2011
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2012.exe for year:2012
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2013.zip for year:2013
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2014.zip for year:2014
    INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2015.zip for year:2015
    >>> pp.pprint(gen)
    defaultdict(<class 'dict'>,
                {   1973: {   'generator': <generator object get_generator_by_year at 0x7fe4b45e7f10>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe',
                                                      'year': '73',
                                                      'zip_file_name': 'namcs73.exe'}},
                    1975: {   'generator': <generator object get_generator_by_year at 0x7fe4b45e7f68>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe',
                                                      'year': '75',
                                                      'zip_file_name': 'namcs75.exe'}},
                    1976: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab410>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs76.exe',
                                                      'year': '76',
                                                      'zip_file_name': 'namcs76.exe'}},
                    1977: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab150>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs77.exe',
                                                      'year': '77',
                                                      'zip_file_name': 'namcs77.exe'}},
                    1978: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab468>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs78.exe',
                                                      'year': '78',
                                                      'zip_file_name': 'namcs78.exe'}},
                    1979: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab4c0>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs79.exe',
                                                      'year': '79',
                                                      'zip_file_name': 'namcs79.exe'}},
                    1980: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab518>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs80.exe',
                                                      'year': '80',
                                                      'zip_file_name': 'namcs80.exe'}},
                    1981: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab570>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs81.exe',
                                                      'year': '81',
                                                      'zip_file_name': 'namcs81.exe'}},
                    1985: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab5c8>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs85.exe',
                                                      'year': '85',
                                                      'zip_file_name': 'namcs85.exe'}},
                    1989: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab620>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs89.exe',
                                                      'year': '89',
                                                      'zip_file_name': 'namcs89.exe'}},
                    1990: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab678>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs90.exe',
                                                      'year': '90',
                                                      'zip_file_name': 'namcs90.exe'}},
                    1992: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab6d0>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs92.exe',
                                                      'year': '92',
                                                      'zip_file_name': 'namcs92.exe'}},
                    1993: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab728>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs93.exe',
                                                      'year': '93',
                                                      'zip_file_name': 'namcs93.exe'}},
                    1994: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab780>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs94.exe',
                                                      'year': '94',
                                                      'zip_file_name': 'namcs94.exe'}},
                    1995: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab7d8>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs95.exe',
                                                      'year': '95',
                                                      'zip_file_name': 'namcs95.exe'}},
                    1996: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab830>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs96.exe',
                                                      'year': '96',
                                                      'zip_file_name': 'namcs96.exe'}},
                    1997: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab888>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs97.exe',
                                                      'year': '97',
                                                      'zip_file_name': 'namcs97.exe'}},
                    1998: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab8e0>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs98.exe',
                                                      'year': '98',
                                                      'zip_file_name': 'namcs98.exe'}},
                    1999: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab938>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs99.exe',
                                                      'year': '99',
                                                      'zip_file_name': 'namcs99.exe'}},
                    2000: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab990>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS00.exe',
                                                      'year': '00',
                                                      'zip_file_name': 'NAMCS00.exe'}},
                    2001: {   'generator': <generator object get_generator_by_year at 0x7fe4b45ab9e8>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS01.exe',
                                                      'year': '01',
                                                      'zip_file_name': 'NAMCS01.exe'}},
                    2002: {   'generator': <generator object get_generator_by_year at 0x7fe4b45aba40>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS02.exe',
                                                      'year': '02',
                                                      'zip_file_name': 'NAMCS02.exe'}},
                    2003: {   'generator': <generator object get_generator_by_year at 0x7fe4b45aba98>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS03.exe',
                                                      'year': '03',
                                                      'zip_file_name': 'NAMCS03.exe'}},
                    2004: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abaf0>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS04.exe',
                                                      'year': '04',
                                                      'zip_file_name': 'NAMCS04.exe'}},
                    2005: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abb48>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS05.exe',
                                                      'year': '05',
                                                      'zip_file_name': 'NAMCS05.exe'}},
                    2006: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abba0>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS06.exe',
                                                      'year': '06',
                                                      'zip_file_name': 'NAMCS06.exe'}},
                    2007: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abbf8>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS07.exe',
                                                      'year': '07',
                                                      'zip_file_name': 'NAMCS07.exe'}},
                    2008: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abc50>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS08.exe',
                                                      'year': '08',
                                                      'zip_file_name': 'NAMCS08.exe'}},
                    2009: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abca8>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/NAMCS09.exe',
                                                      'year': '09',
                                                      'zip_file_name': 'NAMCS09.exe'}},
                    2010: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abd00>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2010.exe',
                                                      'year': '10',
                                                      'zip_file_name': 'namcs2010.exe'}},
                    2011: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abd58>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2011.zip',
                                                      'year': '11',
                                                      'zip_file_name': 'namcs2011.zip'}},
                    2012: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abdb0>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2012.exe',
                                                      'year': '12',
                                                      'zip_file_name': 'namcs2012.exe'}},
                    2013: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abe08>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2013.zip',
                                                      'year': '13',
                                                      'zip_file_name': 'namcs2013.zip'}},
                    2014: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abe60>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2014.zip',
                                                      'year': '14',
                                                      'zip_file_name': 'namcs2014.zip'}},
                    2015: {   'generator': <generator object get_generator_by_year at 0x7fe4b45abeb8>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2015.zip',
                                                      'year': '15',
                                                      'zip_file_name': 'namcs2015.zip'}}})

    Case 6: Process the provided NAMCS data set file. In this case file name is
        assumed to follow "YEAR_NAMCS" format.
    >>>gen = get_cleaned_data_by_year(file_name="/var/tmp/1973_NAMCS")
    >>> pp.pprint(gen)
    defaultdict(<class 'dict'>,
                {   1973: {   'generator': <generator object get_generator_by_year at 0x7f7ba17ac8e0>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe',
                                                      'year': '73',
                                                      'zip_file_name': 'namcs73.exe'}}})
    >>> gen = get_cleaned_data_by_year(file_name="/var/tmp/2015_NAMCS")
    >>> pp.pprint(gen)
    defaultdict(<class 'dict'>,
                {   2015: {   'generator': <generator object get_generator_by_year at 0x7f7ba17acf68>,
                              'source_file_info': {   'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/namcs2015.zip',
                                                      'year': '15',
                                                      'zip_file_name': 'namcs2015.zip'}}})
    >>> pp.pprint(next(gen.get(2015).get("generator")))
    {   'age': 23725,
        'month_of_visit': 'October',
        'patient_visit_weight': 414200.0481,
        'physician_diagnoses': ['723.10', '719.41', '729.50', 'V50.80', 'V00.009'],
        'sex': 'Female',
        'source_file_ID': '2015_NAMCS',
        'source_file_row': 1,
        'year_of_visit': '2015'}

    Case 7: Attempting to process the file for which data is not available on
        CDC FTP server.
    >>> gen = get_cleaned_data_by_year(year=1991)
    ERROR:hdx_ahcd:Year 1991 is not valid year, please specify valid years,valid years are :[1973, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1985, 1989, 1990, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]

    Case 8: Attempting to process a file which does not exists in local machine.
    >>> gen = get_cleaned_data_by_year(file_name="/var/tmp/2015")
    ERROR:hdx_ahcd:NAMCS dataset file:/var/tmp/2015 doesn't exist
    """
    return __Processor().execute(**kwargs)

