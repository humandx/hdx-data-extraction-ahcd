# -*- coding: utf-8 -*-
"""
Module for constants used by NAMCS-NAHMCS extractor
"""

# Diagnosis code and their default string representation
ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS = {
    "Y997": "Diagnosis of 'none'",
    "Y998": "Noncodable diagnosis",
    "Y999": "Illegible diagnosis",
    "0000": "Blank diagnosis",
    "00000": "Blank diagnosis",
    "100000": "Blank diagnosis",
    "209900": "Noncodable",
    "209910": "Left before being seen",
    "209920": "Transferred to another facility",
    "209930": "HMO will not authorize treatment",
    "209970": "Diagnosis of 'none'",
    "900000": "Blank",
}
