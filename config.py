#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 20:46:41 2023

@author: mischasch
"""

# =============================================================================
# Do not alter this.
# Actual configuration settings are stored in the config.ini file (editable 
# without any python knowledge).
# 
# In here, the variable "config" will contain an ConfigParser object which can
# be imported from other subpackages using:
# from resy.config import config
# =============================================================================

import configparser
import os
from pathlib import Path

config = configparser.ConfigParser()

#get containing directory of config.py
path_to_ini = Path(os.path.abspath(__file__)).parent / 'config.ini'

print('Im running!')
#print('CWD: ', os.path.abspath(__file__))
config.read(path_to_ini)
print(config.sections())