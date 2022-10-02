#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:27:47 2022

@author: mischasch
"""

import myres as mr

# =============================================================================
# Testing casing design
# =============================================================================
ids = [0.2, 0.3, 0.5]
ls = [600, 1000, 1200]
cd = mr.casing_design_fl(ls = ls, ids = ids)

# =============================================================================
# create a field
# =============================================================================
wella = mr.well('a')
wellb = mr.well('b')

f = mr.field('Molasse', [wella, wellb])

for well in f.wells:
    well.add_welltop('top reservoir', 2000)
    well.add_welltop('surface', 0)