# -*- coding: utf-8 -*-
"""
Module to expose API for processing NAMCS dataset file(s).
"""
# Other modules
from hdx_ahcd.controllers.namcs_processors import NAMCSProcessor as \
    __NAMCSProcessor


# 3rd party modules
# -N/A


def get_cleaned_data_by_year(**kwargs):
    """
    Method to get translated namcs data for `year` or `file_name`. If no
    arguments are provided data will be converted for all available years.
    Defined in `hdx_ahcd.namcs.config.YEARS_AVAILABLE`.

    Parameters:
        **kwargs (:class:`dict`) : Following are permissible parameters.
            year (:class:`int` or :class:`tuple` or :class:`list`): NAMCS year.
            file_name (:class:`str`): Absolute path of
                raw dataset input file. If not specified, local file
                path will be  deduced on the basis of `year` specified by user.
                Note:
                    Local (extracted) file must exists for this method to
                    yield desired response.
            do_validation (:class:`bool`): If to perform validation
                on `year` and `file_name`. *Default** :const:`True`.
            do_export (:class:`bool`): Output translated  data into csv file.
                *Default** :const:`False`.
            force_download (:class:`bool`): Whether to force download
                NAMCS raw dataset file even if data set file exists locally.
                *Default** :const:`False`.
    Returns:
        :class:`defaultdict`: Dictionary containing generator of converted
        NAMCS patient case data for given year along with source file info.
        Further if `do_export` is True, it returns the absolute path of csv
        file where the data is exported.

    Usage:

        Case 1: Downloading NAMCS data for single year (say, 1973). If the file
            is already present in the downloaded_files then process the
            downloaded file.
        >>> import pprint
        >>> from hdx_ahcd.api import get_cleaned_data_by_year
        >>> pp =pprint.PrettyPrinter(indent=4)
        >>> gen =  get_cleaned_data_by_year(year=1973)
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
            If the file is already present in the downloaded_files then process
            the downloaded file.
        >>> gen =  get_cleaned_data_by_year(year= (1973,1975))
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
        {   'age': 22889.0,
            'month_of_visit': 6,
            'patient_visit_weight': 13479.0,
            'physician_diagnoses': ['470.0', 'V03.2'],
            'sex': 'Female',
            'source_file_ID': '1973_NAMCS',
            'source_file_row': 1,
            'year_of_visit': 1973}
        >>> pp.pprint(next(gen.get(1975).get('generator')))
        Case 3: Forcefully download and then process the NAMCS data for multiple
            years (say, 1973 and 1975).
        >>> gen =  get_cleaned_data_by_year(year= (1973,1975), force_download=True)
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
        >>> pp.pprint(gen)
        Case 5: Forcefully download and then export the processed NAMCS data for
            all years.
        >>> gen =  get_cleaned_data_by_year(force_download=True)
        >>> pp.pprint(gen)
        Case 6: Process the provided NAMCS data set file. In this case file name
            is assumed to follow "YEAR_NAMCS" format.
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
    return __NAMCSProcessor().execute(**kwargs)
