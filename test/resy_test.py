#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:27:47 2022

@author: mischasch
"""

import resy
import numpy as np
import matplotlib.pyplot as plt

doit = False



if doit:

    #%% Test well class
    
    mywell = resy.Well('W1')
    
    
    
    # =============================================================================
    # Testing casing design
    # =============================================================================
    ods = [7.625, 9.625, 10.75]
    wgs = [41, 36, 79.2]
    ids = [0.3, 0.4, 0.5]
    ls = [1000, 1000, 1000]
    cd = resy.CasingDesign(ls = ls, ids = ids, ods = ods, wgs = wgs)
        
    testCasing = False
    if testCasing:
    
        print(cd)
        cd.add_section(section = {'l': 500, 'id': 0.6})
        print(cd)
        cd.remove_section(3)
        print(cd)
        
        cd.adjust_to_zref(1100, 'up')
        print(cd)
    
    # =============================================================================
    # test welltops
    # =============================================================================
    wt = resy.Welltop(name = 'Top Reservoir', z_MD = 1000)
    print(wt)
    # =============================================================================
    # Test well
    # =============================================================================
    testWell = True
    if testWell:
        mywell = resy.Well(uwi = 'FRH1',
                           casing_design=cd,
                           b_res=0.004,
                           c_res=0.002,
                           p_res = 250,
                           T_res = 130,
                           S = 1500,
                           k = 3e-5)
        
    print(mywell.summary('long'))
    
    mywell.welltops.add('ET', z_MD = 4000)
    mywell.welltops.add('Top Malm', z_TVD = 3500)
    
    #print(mywell.welltops)
    
    mywell.welltops.remove('ET')
    
    print(mywell.welltops)
    # =============================================================================
    # test friction losses
    # =============================================================================
    q = np.arange(0,200)
    fl = mywell.get_fl_at_q(q = q, z_ref = 2800)
    
    plt.plot(q, fl)
        
       
    # =============================================================================
    # Test loading
    # =============================================================================
    
    myfield = resy.Field('Molasse')
    myfield.refresh_from_database()
    myfield.plot('ipr', backend = 'Matplotlib')
    
    myfield['FRH1'].casing_design = cd
    q = np.arange(0,150)
    #myfield['FRH1'].get_fl_at_q(q, 0)
    
    #print(myfield.summary('short'))
    for well in myfield.wells:
        print(well.summary(sumtype = 'short'))
