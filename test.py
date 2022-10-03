#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:27:47 2022

@author: mischasch
"""

import myres as mr, numpy as np, matplotlib.pyplot as plt

# =============================================================================
# Testing casing design
# =============================================================================
# ids = [0.2, 0.3, 0.5]
ls = [600, 1000, 1200]
# cd = mr.casing_design(ls = ls, ids = ids)

ods = [5.5, 7.625 , 10.75]
wgs = [14, 59, 79.2]
cd = mr.casing_design(ls = ls, ods = ods, wgs = wgs)

#print(cd.ids)

# =============================================================================
# test welltops
# =============================================================================
mywell = mr.well(name = 'GIS1', casing_design = cd, p_res = 250, T_res = 140, S = 2000)
#mywell.add_welltop('Top Malm')

# =============================================================================
# test friction losses
# =============================================================================
q = np.arange(200)
fl = mywell.get_fl_at_q(q = q)

plt.plot(q, fl)
# ============================================================================
# create a field
# =============================================================================
# wella = mr.well('a')
# wellb = mr.well('b')

# f = mr.field('Molasse', [wella, wellb])

# for well in f.wells:
#     well.add_welltop('top reservoir', 2000)
#     well.add_welltop('surface', 0)