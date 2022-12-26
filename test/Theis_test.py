#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 21:09:04 2022

@author: mischasch
"""
import sys
sys.path.append('/Users/mischasch/Documents/GitHub')
from resy.analytical_solutions import *

T = 1e-2
S = 1e-3
skin = 5

rw = 0.3 #well radius
boundary_distance = 1000

q = 1e-3
r = np.linspace(rw, 1000, 100000)
t = 3600*24*365

s = AnalyticalWellTestSolution('Theis', T, S, rw, 
                               boundary_distance, 'positive',
                               skin).compute_drawdown(q, r, t)