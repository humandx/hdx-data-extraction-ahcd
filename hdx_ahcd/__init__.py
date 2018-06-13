# -*- coding: utf-8 -*-
"""
This file contains parameters related to initialization of package
"""
# Other modules
from hdx_ahcd.scripts.controllers import NAMCSController as __Controller

# 3rd party modules
# -N/A
name = "hdx_ahcd"
get_cleaned_data_by_year = __Controller().execute
