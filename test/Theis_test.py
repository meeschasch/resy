#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 21:09:04 2022

@author: mischasch
"""
import sys
sys.path.append('/Users/mischasch/Documents/GitHub')
from resy.analytical_solutions import *

import numpy as np
from matplotlib import pyplot as plt

T = 1e-5
S = 1e-3
skin = 5

rw = 0.3 #well radius
boundary_distance = 1000

q = 1e-3
r = np.linspace(rw, 1000, 100000)
t = 3600*24*365

s_new = AnalyticalWellTestSolution('Theis', T, S, rw, 
                               boundary_distance, 'negative',
                               skin_factor = 0).compute_drawdown(q, r, t)

#s_old = TheisWithBoundary(T, S, 'negative', boundary_distance).compute_drawdown(q, r, t)
_, ax = plt.subplots()

s_skin = AnalyticalWellTestSolution('Theis', T, S, rw, 
                                    boundary_distance, 'positive', 
                                    skin_factor= 5).compute_drawdown(q, r, t)
#ax.plot(r, s_new, color = 'blue')
#ax.plot(r, s_old, color = 'green')
#ax.plot(r, s_skin, color = 'green')

q = np.linspace(0, 1.5e-3, 1000)
skin = Skin(T, 5).compute_drawdown(q)
s_own = AnalyticalWellTestSolution('Theis', T, S, rw, 
                               boundary_distance, 'negative',
                               skin_factor = 0).compute_drawdown(q, rw, t)
ax.plot(q, skin, color = 'red')
ax.plot(q, s_own, color = 'blue')