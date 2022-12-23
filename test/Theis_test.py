#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 21:09:04 2022

@author: mischasch
"""
import sys
sys.path.append('/Users/mischasch/Documents/GitHub')
from resy.analytical_solutions import *

r_well = 0.3 #well radius

aqn = TheisWithBoundary(1e-3, 1e-3, None, 1000)
aqp = TheisWithBoundary(1e-3, 1e-3, 'positive', 1000)
aqne = TheisWithBoundary(1e-3, 1e-3, 'negative', 1000)


q = 200e-3
r = np.linspace(r_well, 1000)
t = 3600*24*365

sn = aqn.compute_drawdown(q, r, t)
sp = aqp.compute_drawdown(q, r, t)
sne = aqne.compute_drawdown(q, r, t)



_, ax = plt.subplots()
ax.plot(r, sn, label = 'no boundary')
ax.plot(r, sp, label = 'positive boundary')
ax.plot(r, sne, label = 'negative boundary')
ax.set_xlim([0, 1000])
ax.legend()