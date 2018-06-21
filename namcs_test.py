# -*- coding: utf-8 -*-
"""
Module to test extraction and conversion process of NAMCS dataset(s) for all
NAMCS year.
"""
# Python modules
import csv
import logging
import os

# Other modules
from hdx_ahcd.helpers.functions import (
    get_customized_file_name,
    get_normalized_namcs_file_name,
)
from hdx_ahcd.namcs.config import (
    CONVERTED_CSV_FIELDS,
    ERROR_FILES_DIR_PATH,
    YEARS_AVAILABLE,
)
from hdx_ahcd.api import get_cleaned_data_by_year

# 3rd party modules
# -N/A

# Global vars
logging.basicConfig(level=logging.INFO)  # Configure logger
LOG = logging.getLogger("NAMCS_regression_test")

# Output file path
TSV_FILE_PATH = "/tmp/namcs_data_for_all_years.tsv"


def namcs_regression_test():
    """
    Invoke method `get_cleaned_data_by_year` for all NAMCS years configured
    by parameter `YEARS_AVAILABLE` and report errors occurred during execution
    for any NAMCS year it includes reporting of errors occurred while accessing
    `generator` returned by `get_cleaned_data_by_year`.If no errors are occurred
    append all the records for in the output file denoted by `TSV_FILE_PATH`.
    On successful execution file `TSV_FILE_PATH` will contain all records for
    for all NAMCS years.

    Note:
        This is strictly for dev  purpose, no actual test case or test suite
        are used to perform regression.
    """
    with open(TSV_FILE_PATH, "w") as file_handle:
        tsv_writer = csv.DictWriter(file_handle,
                                    fieldnames = CONVERTED_CSV_FIELDS,
                                    delimiter = '\t')
        tsv_writer.writeheader()

        LOG.info("Processing namcs data "
                 "for all years:{}\n".format(YEARS_AVAILABLE))

        namcs_data_all_years = get_cleaned_data_by_year()
        for year in YEARS_AVAILABLE:
            LOG.debug("Processing year:{}".format(year))
            namcs_data_year = namcs_data_all_years.get(year)
            try:
                LOG.debug("Using generator for year:{}".format(year))
                translated_data_gen_obj = namcs_data_year.get('generator')
            except Exception as exc:
                LOG.error("Error:'{}', while "
                          "processing generator "
                          "for year:{}, moving "
                          "to next year".format(str(exc), year))
                continue
            LOG.debug("Writing data to tsv file.")
            for record_no, record in enumerate(translated_data_gen_obj):
                try:
                    tsv_writer.writerow(record)
                except Exception as exc:
                    LOG.error("Error:'{}' in writing "
                              "record\n[{}]"
                              "\nRecord no:[{}] "
                              "\nFor year:[{}]".format(str(exc), record,
                                                       record_no+1, year))
            else:
                LOG.info("Total records:[{}] "
                         "written for year:[{}]".format(record_no+1, year))

            source_file_id = get_normalized_namcs_file_name(year)
            # Error file path
            error_file = os.path.join(
                ERROR_FILES_DIR_PATH,
                get_customized_file_name(source_file_id, extension="err")
            )
            if os.path.exists(error_file):
                LOG.error("Error: error file "
                          "for year:{} is generated.".format(error_file))
    LOG.info("Data for all namcs years:[{}]".format(TSV_FILE_PATH))


if __name__ == '__main__':
    namcs_regression_test()
