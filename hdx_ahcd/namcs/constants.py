# -*- coding: utf-8 -*-
"""
Module to define constants used in package hdx_ahcd.
"""
# Diagnosis code and their default string representation
ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS = {
    "900000": "Blank",
    "0000": "Blank diagnosis",
    "00000": "Blank diagnosis",
    "100000": "Blank diagnosis",
    "209900": "Noncodable",
    "V9900": "Noncodable diagnosis",
    "Y998": "Noncodable diagnosis",
    "209910": "Left before being seen",
    "V9910": "Left before being seen",
    "209920": "Transferred to another facility",
    "V9920": "Transferred to another facility",
    "209970": "Diagnosis of 'none'",
    "V9970": "Diagnosis of 'none'",
    "Y997": "Diagnosis of 'none'",
    "Y999": "Illegible diagnosis",
    "209930": "HMO will not authorize treatment",
}
