# -*- coding: utf-8 -*-
"""
Script to perform regression for extraction and conversion for all namcs year.
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
    To extract and translate namcs data for all years, and report errors
    during same.
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
            LOG.info("Processing year:{}".format(year))
            namcs_data_year = namcs_data_all_years[year]
            try:
                LOG.info("Using generator for year:{}".format(year))
                translated_data_gen = namcs_data_year['generator']
            except Exception as e:
                LOG.error("Error:'{}', while "
                          "processing generator "
                          "for year:{}, moving "
                          "to next year".format(str(e), year))
                continue
            LOG.info("Writing data to tsv file.....\n")
            for record_no, record in enumerate(translated_data_gen):
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

            # Error file name
            source_file_id = get_normalized_namcs_file_name(year)
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
