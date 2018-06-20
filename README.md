# hdx-data-extraction-ahcd
------
Code to convert CDC's Ambulatory Health Care Data (AHCD) (NAMCS and NHAMCS) in human readable form.
https://www.cdc.gov/nchs/ahcd/about_ahcd.htm.
  - # NAMCS
    The National Ambulatory Medical Care Survey (NAMCS) is a national survey designed to meet the need for objective, reliable information about the provision and use of ambulatory medical care services in the United States. Findings are based on a sample of visits to nonfederally employed office-based physicians who are primarily engaged in direct patient care.
  - # NHAMCS
    The National Hospital Ambulatory Medical Care Survey (NHAMCS) is designed to collect data on the utilization and provision of ambulatory care services in hospital emergency and outpatient departments, and in ambulatory surgery centers

# Code Structure
>   **hdx_ahcd** serves as base directory
```sh
hdx_ahcd
├── controllers
│   ├── __init__.py
│   ├── namcs_converter.py
│   ├── namcs_extractor.py
│   └── namcs_processors.py
├── helpers
│   ├── functions.py
│   └── __init__.py
├── mappers
│   ├── functions.py
│   ├── __init__.py
│   └── years.py
├── namcs
│   ├── config.py
│   ├── constants.py
│   ├── enums.py
│   └── __init__.py
├── scripts
│   ├── __init__.py
│   └── namcs_validators.py
└── utils
    ├── context.py
    ├── decorators.py
    ├── exceptions.py
    ├── __init__.py
    └── utils.py
```
* controllers
    - namcs_extractor.py - download and extract public NAMCS data
    - namcs_converter.py - process and convert NAMCS data in human readable format
    - namcs_processors - provide common entry point for execution
* helpers - various methods for manipulating dataset and it's details
* mappers
    - helpers - methods to translate raw data from dataset to human readable format
    - years - year wise NAMCS details like fields, their position in dataset, length etc.
* namcs - contains configurable parameters and constants
* scripts
    - namcs_validators - validation of dataset and parameters provided while invoking script controllers
* utils - contains useful decorators, context managers etc.
* namcs_test.py - script to perform regression for all namcs year(DEV purpose only).
### Fields
-----
- date_of_visit - patient date of visit
- date_of_birth - patient date of birth
- year_of_visit - patient year of visit
- year_of_birth - patient year of birth
- month_of_visit - patient month of visit
- month_of_birth - patient month of birth
- patient_age - patient age in days
- gender - patient gender
- physician_diagnoses - ICD-9-CM code (International Classification of Diseases, 9th Revision, Clinical Modification) for Diagnostic information
- visit_weight - The "patient visit weight" is a vital component in the
process of producing national estimates from sample data,
and its use should be   clearly understood by all micro-data file
users. The statistics contained on the micro-data
file reflect data concerning only a sample of
patient visits, not a complete count of all the
visits that occurred in the United States. Each
record on the data file represents one
visit in the sample of 27,369 visits. In order to obtain
national estimates from the sample,
each record is assigned an inflation factor called the
"patient visit weight."

### Installation
-----
Currently supported python version 3.6.x,
To check python version
```sh
python --version
```
Ensure pip, setuptools, and wheel are up to date
```sh
python -m pip install --upgrade pip setuptools wheel
```
If you have local copy of this repo and want to install directly from it.
```sh
pip install ${PATH_FOR_hdx-data-extraction-ahcd_REPO}
```
Similarly you can execute setup file
```sh
python3 ${PATH_FOR_hdx-data-extraction-ahcd_REPO}/setup.py install
```
for example:
```sh
pip install /var/tmp/hdx-data-extraction-ahcd/
```
and

```sh
python3 /var/tmp/hdx-data-extraction-ahcd/setup.py install
```
You can also use pip directly for Installation.
```sh
pip install hdx_ahcd
```
-----
### Usage
-----
```sh
>>> import hdx_ahcd
>>> from hdx_ahcd.api import get_cleaned_data_by_year
>>> gen =  get_cleaned_data_by_year(year=1973)
INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov
/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe for year:1973
>>> import pprint
>>> pp =pprint.PrettyPrinter(indent=4)
>>> pp.pprint(gen)
defaultdict(<class 'dict'>,
        {   1973: {   'generator': <generator object get_generator_by_year at 0x7fe4b6480150>,
                      'source_file_info': {
                      'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe',
                      'year': '73',
                      'zip_file_name': 'namcs73.exe'}}})
>>> gen =  get_cleaned_data_by_year(year= (1973,1975))
INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov
/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe for year:1975
>>> pp.pprint(gen)
defaultdict(<class 'dict'>,
            {   1973: {   'generator': <generator object get_generator_by_year at 0x7fe4b5fa9e08>,
                          'source_file_info': {
                          'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe',
                          'year': '73',
                          'zip_file_name': 'namcs73.exe'}},
                1975: {   'generator': <generator object
                get_generator_by_year at 0x7fe4b45e7e60>,
                          'source_file_info': {
                          'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe',
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
>>> gen =  get_cleaned_data_by_year(year= (1973,1975), force_download=True)
INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe for year:1973
INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe for year:1975
>>> pp.pprint(gen)
defaultdict(<class 'dict'>,
            {   1973: {   'generator': <generator object get_generator_by_year at 0x7fe4b5fa9e08>,
                          'source_file_info': {
                          'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe',
                          'year': '73',
                          'zip_file_name': 'namcs73.exe'}},
                1975: {   'generator': <generator object get_generator_by_year at 0x7fe4b45e7e60>,
                          'source_file_info': {
                          'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe',
                          'year': '75',
                          'zip_file_name': 'namcs75.exe'}}})
>>> gen =  get_cleaned_data_by_year(year= (1973,1975), force_download=True,
 do_export=True)
INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe for year:1973
INFO:hdx_ahcd:Finished writing to the file /home/velotio/.hdx_ahcd/data/1973_NAMCS_CONVERTED.csv
INFO:hdx_ahcd:Downloading file:ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs75.exe for year:1975
INFO:hdx_ahcd:Finished writing to the file /home/velotio/.hdx_ahcd/data/
1975_NAMCS_CONVERTED.csv
>>> pp.pprint(gen)
defaultdict(<class 'dict'>,
        {   1973: {   'file_name': '/home/velotio/.hdx_ahcd/data/1973_NAMCS_CONVERTED.csv',
                      'generator': <generator object get_generator_by_year at 0x7fe4b6480150>,
                      'source_file_info': {
                      'url': 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/namcs_public_use_files/namcs73.exe',
                      'year': '73',
                      'zip_file_name': 'namcs73.exe'}},
            1975: {   'file_name': '/home/velotio/.hdx_ahcd/data/1975_NAMCS_CONVERTED.csv',
                      'generator': <generator object get_generator_by_year at 0x7fe4b45e7e60>,
                      'source_file_info': {   '
                      url': 'ftp://ftp.cdc.gov/pub/Health_Statistics
                      /NCHS/namcs_public_use_files/namcs75.exe',
                      'year': '75',
                      'zip_file_name': 'namcs75.exe'}}})
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
```
### Uninstall
-----
To uninstall you can use either
```sh
easy_install -m hdx_ahcd
```
or
```sh
pip uninstall hdx_ahcd
```
### Scope
-----
 - Supported fields are
    - date_of_visit
    - date_of_birth
    - year_of_visit
    - year_of_birth
    - month_of_visit
    - month_of_birth
    - patient_age
    - gender
    - physician_diagnoses
    - visit_weight
 - Support for NHAMCS data set to be added in subsequent releases
 - Unsupported years due to missing data sets on CDC server
    - 1974, 1982, 1983, 1984, 1986, 1987, 1988, 1991
