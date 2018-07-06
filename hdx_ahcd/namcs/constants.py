# -*- coding: utf-8 -*-
"""
Module to define constants used in package hdx_ahcd.
"""
# Other Modules
from hdx_ahcd.namcs.enums import PhysicianDiagnosesEnum

# Diagnosis code and their default string representation
ICD_9_DEFAULT_CODES_FOR_DIAGNOSIS = {
    "900000": "Blank",
    "0000": "Blank diagnosis",
    "00000": "Blank diagnosis",
    "100000": "Blank diagnosis",
    "209900": "Noncodable",
    "V9900": "Noncodable diagnosis",
    "Y998": "Noncodable diagnosis",
    "209910": PhysicianDiagnosesEnum.LEFT_BEFORE_BEING_SEEN.value,
    "V9910": PhysicianDiagnosesEnum.LEFT_BEFORE_BEING_SEEN.value,
    "209920": PhysicianDiagnosesEnum.TRANSFER_TO_ANOTHER_FACILITY.value,
    "V9920": PhysicianDiagnosesEnum.TRANSFER_TO_ANOTHER_FACILITY.value,
    "209970": "Diagnosis of 'none'",
    "V9970": "Diagnosis of 'none'",
    "Y997": "Diagnosis of 'none'",
    "Y999": "Illegible diagnosis",
    "209930": PhysicianDiagnosesEnum.HMO_WILL_NOT_AUTHORIZE_TREATMENT.value,
}
