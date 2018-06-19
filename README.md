# HDX-data-extraction-AHCD
------
Code to parse and clean the CDC's Ambulatory Health Care Data (AHCD) (NAMCS and NHAMCS): https://www.cdc.gov/nchs/ahcd/about_ahcd.htm.
  - # NAMCS
    The National Ambulatory Medical Care Survey (NAMCS) is a national survey designed to meet the need for objective, reliable information about the provision and use of ambulatory medical care services in the United States. Findings are based on a sample of visits to nonfederally employed office-based physicians who are primarily engaged in direct patient care.
  - # NHAMCS
    The National Hospital Ambulatory Medical Care Survey (NHAMCS) is designed to collect data on the utilization and provision of ambulatory care services in hospital emergency and outpatient departments, and in ambulatory surgery centers

# Code Structure
>   **hdx_ahcd** serves as base directory
```sh
hdx_ahcd
├── general
│   ├── __init__.py
│   ├── namcs_converter.py
│   └── namcs_extractor.py
├── helpers
│   ├── functions.py
│   └── __init__.py
├── mapper
│   ├── functions.py
│   ├── __init__.py
│   └── years.py
├── namcs
│   ├── config.py
│   ├── constants.py
│   ├── enums.py
│   └── __init__.py
├── scripts
│   ├── controllers.py
│   ├── __init__.py
│   └── validation.py
└── utils
    ├── context.py
    ├── decorators.py
    ├── exceptions.py
    ├── __init__.py
    └── utils.py
```
* general
    - namcs_extractor.py - download and extract public NAMCS data
    -  namcs_converter.py - process and convert NAMCS data in human readable format
* helpers - various methods for manipulating dataset and it's details
* mappers
    - helpers - methods to translate raw data from dataset to human readable format
    - years - year wise NAMCS details like fields, their position in dataset, length etc.
* namcs - contains configurable parameters and constants
* scripts
    - controllers - provide common entry point for execution
    - validation - validation of dataset and parameters provided while invoking script controllers
* utils - contains useful decorators, context managers etc.
* namcs_test.py - script to perfrom regression for all namcs year(DEV purpose only).

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
pip install ${PATH_FOR_HDX-data-extraction-AHCD_REPO}
```
Similarly you can execute setup file
```sh
python3 ${PATH_FOR_HDX-data-extraction-AHCD_REPO}/setup.py install
```
for example:
```sh
pip install /var/tmp/HDX-data-extraction-AHCD/
```
and
for example:
```sh
python3 /var/tmp/HDX-data-extraction-AHCD/setup.py install
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
>>> from hdx_ahcd import get_cleaned_data_by_year
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
### TODO
-----
 - Support for more fields
    - supported fields are
        - date_of_visit
        - date_of_birth
        - year_of_visit
        - year_of_birth
        - month_of_visit
        - month_of_birth
        - patient_age
        - gender
        - physician_diagnosis
        - visit_weight
 - Support for NHAMCS
    - currently only NAMCS supported.
 ---
License
----
To be discussed.
