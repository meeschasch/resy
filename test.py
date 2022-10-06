#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:27:47 2022

@author: mischasch
"""

import myres as mr, numpy as np, matplotlib.pyplot as plt

#=============================================================================
#Testing casing design
#=============================================================================
# ids = [0.2, 0.3, 0.5]
ls = [1000, 1000, 1000]
# cd = mr.casing_design(ls = ls, ids = ids)

ods = [7.625, 9.625, 10.75]
wgs = [41, 36, 79.2]
ids = [0.3, 0.4, 0.5]
cd = mr.CasingDesign(ls = ls, ids = ids, ods = ods, wgs = wgs)
print(cd)
cd.adjust_to_zref(1500, 'down')
print(cd)

fig, ax = plt.subplots()

#cd.remove_section(2)

#cd.add_section(2, l = 400, id = 9.4)
#print(cd.ids)

# # =============================================================================
# # test welltops
# # =============================================================================
# mywell = mr.well(name = 'GIS1', casing_design = cd, p_res = 250, T_res = 140, S = 2000, welltype = 'inj')
# #mywell.add_welltop('Top Malm')

# print(mywell.find_containing_section(1100))
# # =============================================================================
# # test friction losses
# # =============================================================================
# q = np.arange(1100)
# fl = mywell.get_fl_at_q(q = q)

#plt.plot(q, fl)

# =============================================================================
# test p at q
# =============================================================================
# ============================================================================
# create a field
# =============================================================================
# wella = mr.well('a')
# wellb = mr.well('b')

# f = mr.field('Molasse', [wella, wellb])

# for well in f.wells:
#     well.add_welltop('top reservoir', 2000)
#     well.add_welltop('surface', 0)

# from abc import ABC, abstractmethod
# class test(ABC):
#     def __init__(self, attr):
#         self.attr = attr
    
#     def print_not_abstract(self):
#         print('printed from the abc')
        
#     @abstractmethod
#     def print_abstract(self):
#         pass
    
# class subtest(test):
#     def __init(self, attr):
#         super().__init__(attr)
#         self.attr = attr
        
#     def print_abstract(self):
#         print('printed from the subclass')


# t = subtest('sdf')
# t.print_not_abstract()
# t.print_abstract()