#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:29:23 2022

@author: mischasch
"""
from collections.abc import Iterable
import numpy as np

class Survey():
    '''
    survey of a well. Index is MD. Incl, Azim and TVD refer to this index.
    '''
    def __init__(self, md, incl, azim, tvd = None):
        '''
        

        Parameters
        ----------
        md : np.array
            measured depth [m].
        incl : np.array
            inclination (deg). Horizontal = 0.
        azim : np.array
            azimuth (deg). North = 0, clockwise.
        tvd : np.array, optional
            true vertical depth [m]. The default is None.

        Returns
        -------
        None.

        '''   
        self.md = md
        self.incl = incl
        self.azim = azim
        self.tvd = tvd
        
# =============================================================================
#Properties
# =============================================================================
   #azimuth vector
    @property
    def azim(self):
        return self._azim
    
    @azim.setter
    def azim(self, new_azim):
        #type check
        if new_azim is not None:
            if not isinstance(new_azim, Iterable):
                raise ValueError('object must be an iterable')
                
            #check length
            if len(new_azim != len(self.md)):
                raise ValueError('Azimuth array must be of equal length as the MD array')
            
        self._azim = new_azim
        
   #inclination vector
    @property
    def incl(self):
        return self._incl
    
    @incl.setter
    def incl(self, new_incl):
        if new_incl is not None:
            #type check
            if not isinstance(new_incl, Iterable):
                raise ValueError('object must be an iterable')
                
            #check length
            if len(new_incl != len(self.md)):
                raise ValueError('Inclination array must be of equal length as the MD array')
            
        self._incl = new_incl
        
# =============================================================================
# Methods
# =============================================================================
    def get_tvd_at_md(md):
        '''
        returns TVD values at one or more specific MD depths

        Parameters
        ----------
        md : float or array of floats
            MD value(s) at which TVD should be evaluated.

        Returns
        -------
        tvd : float or aray of float
            TVD value(s).

        '''
        #TODO (vectorized)
        tvd = np.array()
        
        return tvd
    
    def get_interpolated_survey(steps):
        '''
        compiles an interpolated survey from top to final depth
        

        Parameters
        ----------
        steps : float
            step width (m MD) which should be used.

        Returns
        -------
        md : array of floats
            m MD.
        tvd: array of floats
            m TVD
        incl: array of floats
            inclination [deg]
        azim: array of floats
            azimuth [deg]

        '''
        md, tvd, incl, azim = np.array()
        
        #TODO
        
        return md, tvd, incl, azim
        