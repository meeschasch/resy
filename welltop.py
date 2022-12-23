#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:00:37 2022

@author: mischasch
"""
import pandas as pd
import numpy as np
from resy.summarizer import WelltopSummarizer
        
class Welltop():
    '''
    a welltop
    '''
    def __init__(self, name, z_MD = None, z_TVD = None, z_NN = None, x = None, y = None):
        '''
        

        Parameters
        ----------
        name : string
            welltop name (e.g. 'top Malm'.
        z_MD : float, optional. 
            depth [m MD]. The default is None.
        z_TVD : float, optional
            depth [m TVD].. The default is None.
        z_NN : float, optional
                depth [m NN]. The default is None.
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
        self.z_NN = z_NN
        self.x = x
        self.y = y
        
    def __repr__(self):
        return self.summary
    
    @property
    def summary(self):
        return WelltopSummarizer(self).summarize(form = 'str')
