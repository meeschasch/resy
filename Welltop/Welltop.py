#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:33:41 2022

@author: mischasch
"""

class Welltop():
    '''
    a welltop
    '''
    def __init__(self, name, z_MD = None, z_TVD = None, x = None, y = None):
        '''
        

        Parameters
        ----------
        name : string
            welltop name (e.g. 'top Malm'.
        z_MD : float, optional. 
            depth [m MD]. The default is None.
        z_TVD : float, optional
            depth [m TVD].. The default is None.
        x: float, optional
            x coordinate.
        y: float, optional
            y coordinate.

        Returns
        -------
        None.

        '''
            
        self.name = name
        self.z_MD = z_MD
        self.z_TVD = z_TVD
        self.x = x
        self.y = y