#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 14:53:08 2022

@author: mischasch
"""

import numpy as np
from collections.abc import Iterable
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass

from resy.casing_design import CasingDesign
from resy.welltop import Welltop
from resy.survey import Survey
from resy.welltop import Welltops
import resy.reseng_2101 as res
from resy.summarizer import WellSummarizer
from resy.calculator import WellCalculator

class Well():
    '''
    Contains information on a well and allows for computations of derived values


    Parameters
    ----------
    name : string
        well name
    casing_design : casing_design
        casing design for friction losses. It should include all 
        completeions from top reservoir to the surface. Optional.
    survey : survey
        final surfey of a well. Optional.
    welltops: list of welltops
        List containing welltop objects. Optional. Note: it's easiest to 
        set welltops using the set_welltop function. Welltops should include:
            - surface
            - top reservoir
            - final depth
    c_res : float
        c-coefficient at Top Reservoir. Optional.
    b_res : float
        b-coefficient at Top Reservoir. Optional.
    c_surf : float
        c-coefficient at surface. Optional.
    T_res : float
        Reservoir temperature [°C]. Optional.
    p_res : float
        Reservoir pressure [bara]. Optional.
    p_regr: float
        Reservoir pressure [bara] according to reservoir-wide regression of
        p_res vs. top reservoir
    S: float, optional
        salinity [mg/l]
    k: float
        friction losses roughness parameter. Default is 3e-5.
    z_ESP: float, optional
        depth [m TVD] of ESP intake

        '''
    uwi: str
    name: str = None
    c_res: float = None
    b_res: float = None
    T_res: float = None
    p_res: float = None
    S: float = None
    k: float = 3e-5
    z_ESP: float = None
    welltops: Welltop = None
    survey: Survey = None
    casing_design: CasingDesign = None
        

    def summary(self, sumtype: str = 'long'):
        '''
        
        Parameters
        ----------
        sumtype : str
            'long' for a text based comprehensive summary,
            'short' for a pd.DataFrame with the most important data.
            Default is 'long'

        '''
        if sumtype == 'long':
            return WellSummarizer.WellSummarizerLong(self).summarize()
        elif sumtype == 'short':
            return WellSummarizer.WellSummarizerShort(self).summarize()
        else:
            raise ValueError('Summary type not available')

#%% Methods to compute things from wells.

    def get_fl_at_q(self, q, z_ref: float = 0, flow_direction: str = 'up'):
        '''
        computes friction losses of the entire well at one or many flow rates. 
        Friction losses are by default computed
        at surface (production well) or at top reservoir(injection wells).
        
        Temperature is assumed as homogeneous throughout the wellbore.
        
        Production wells: If you want 
        to comopute friction losses just until ESP intake, set z_ref to z_ESP

        Parameters
        ----------
        
        q : float or array of floats
            flow rate(s) [l/s] at which to compute friction closses.
        z_ref: float, optional
            reference depth [m TVD] to compute friction losses at. Default = 0.
        flow_direction: string
            'up' for flow from final depth upwards, 'down' for flow
            from surface downwards. Default is 'up'.
        T: float, Optional
            Temperature to use for density computation. Default is the wells
            reservoir temperature

        Returns
        -------
        fl : array of floats
            friction losses [bar] at the given flow rates.

        '''
        
        return WellCalculator.WellFLatQCalculator(self, q = q, z_ref = z_ref,
                                   flow_direction = flow_direction).calculate()
    
    def get_p_at_q(self, q, z_ref = 0, T = None):
        '''
        computes the pressure at on or specific flow rates at a specific depth. 

        Parameters
        ----------
        q : float or array of float
            flow rate(s) at which to compute the pressure.
        z_ref : float, optional
            reference depth [m TVD] at which to compute.. The default is 0.
        T_res: float, optional
            Reservoir / production temperature. If not set, the wells 
            reservoir temperature will be used.

        Returns
        -------
        p : float or array of float
            pressure [bara] at the specified depth at the specified flow rate.

        '''
        return WellCalculator.WellPatQCalculator(self, q, z_ref).calculate()
    



            


