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
    '''
    
    def __init__(self, uwi, name = None, casing_design = None, survey = None, 
                 welltops: Welltops = None, c_res = None, b_res = None, 
                 c_surf = None, T_res = None, p_res = None, p_regr = None, 
                 S = None, k = 3e-5, welltype = 'prod', z_ESP = None):
        '''

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
        welltype: 'prod' or 'inj', optional
            'prod' for a production well, 'inj' for an injection well. Default is 'prod'
        z_ESP: float, optional
            depth [m TVD] of ESP intake

        '''
        self.name = name
        self.uwi = uwi
        self.c_res = c_res
        self.b_res = b_res
        self.c_surf = c_surf
        self.T_res = T_res
        self.p_res = p_res
        self.S = S
        self.k = k
        self.z_ESP = z_ESP
        
        self.welltops = welltops
        self.casing_design = casing_design
        self.survey = survey
        self.welltype = welltype
        
# =============================================================================
#Properties
# =============================================================================
    #casing design
    @property
    def casing_design(self):
        '''
        casign design as used for friction losses computation

        '''
        return self._casing_design

    @casing_design.setter
    def casing_design(self, new_casing_design):
        #type check
        if new_casing_design is not None:
            if not isinstance(new_casing_design, CasingDesign):
                raise ValueError('casing design must be of type casing_design')
            
        self._casing_design = new_casing_design
        
    #survey
    @property
    def survey(self):
        '''
        well survey

        '''
        return self._survey

    @survey.setter
    def survey(self, new_survey):
        #type check
        if new_survey is not None:
            if not isinstance(new_survey, Survey):
                raise ValueError('survey must be of type survey')
        
        self._survey = new_survey
        
    @property 
    def welltops(self):
        return self._welltops
    
    @welltops.setter
    def welltops(self, new_welltops):
        #type check
        if new_welltops is not None:
            if not isinstance(new_welltops, Welltops):
                raise ValueError('not a Welltops list')
                
            else:
                self._welltops = new_welltops
        else:
            self._welltops = Welltops()
  
            
        
    def compute_c_surf(self, z_ref = 0):
        '''
        
        computes the surface c-coefficient based on the reservoir c-coefficient
        ant the friction losses
        
        Parameters
        ---------
        z_ref: float
            reference depth to compute the coefficient at (relevant for 
            friction losses computation) [m TVD]. Default is 0.
        
        '''
        c_res = 0
        
        #TODO
        
        self.c_res = c_res


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
    
# =============================================================================
# Other methods
# =============================================================================
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


            


