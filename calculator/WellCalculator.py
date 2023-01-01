#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:44:21 2022

@author: mischasch
"""
from abc import ABC, abstractmethod
from collections.abc import Iterable
import sys



class WellCalculator(ABC):
    '''
    ABC for all calculator classes
    '''
    def __init__(self, well):
        #get location of reslib from config and import module
        from resy.config import config
        sys.path.append(config.get('Packages', 'reslib'))
        import reseng_2101
        
        #avoid circular import (TODO: solve this more elegantly...)
        from resy import Well 
        self.well = well
        

    @abstractmethod
    def calculate(self):
        ...
        return object #something MUST be returned
        
class WellFLatQCalculator(WellCalculator):
        '''
        see documentation in Well.get_fl_at_q()

        '''
        def __init__(self, well, q, z_ref: float, flow_direction: str = 'up'):
            super().__init__(well)
            
            self.q = q
            self.z_ref = z_ref
            self.flow_direction = flow_direction
            
        def calculate(self):
            if self.z_ref != 0:
                adj_casing_design = self.well.casing_design.adjust_to_zref(self.z_ref,
                                                            self.flow_direction)
            else:
                adj_casing_design = self.well.casing_design

            if not isinstance(self.q, Iterable):
                self.q = [self.q]
                #only one q value
            fl = [res.hyd_fl_well_aux(adj_casing_design.ids,
                                     adj_casing_design.ls, k = self.well.k,
                                     q = qi, p =  self.well.p_res,
                                     T = self.well.T_res,
                                     S = self.well.S)
                  for qi in self.q]
            
            if len(fl) == 1:
                fl = fl[0]
            return fl
    
class WellPatQCalculator(WellCalculator):
    '''
    computes pressure at a given depth in a well
    '''
    
    def __init__(self, well, q, z_ref, flow_direction = 'up', T = None):
        super().__init__(well)
        
        self.q = q
        self.z_ref = z_ref
        self.flow_direction = flow_direction
        
        if T is None:
            T = self.well.T_res
    
    def calculate(self):
        if self.z_ref != 0:
            adj_casing_design = self.well.casing_design.adjust_to_zref(self.z_ref,
                                                        self.flow_direction)
        else:
            adj_casing_design = self.well.casing_design
            
        if not isinstance(self.q, Iterable):
            self.q = [self.q]
            
        #TODO: h in TVD above Top Reservoir
        h = 500 #temporary, remove!
        
        if self.flow_direction == 'up':
            p = [res.hyd_p_prod_well(q = qi, 
                                      p_res = self.well.p_res,
                                      T = self.T, 
                                      k = self.well.k,
                                      h = h,
                                      ls = adj_casing_design.ls,
                                      ids = adj_casing_design.ids,
                                      b = self.well.b_res,
                                      c = self.well.c_res,
                                      S = self.well.S, p_int = 0)
                 for qi in self.q]