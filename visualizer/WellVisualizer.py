#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:02:34 2022

@author: mischasch
"""

from abc import ABC, abstractmethod

class WellVisualizer(ABC):
    '''
    Abstract base class for any well plotters
    '''
    def __init__(self, well, savepath:str = None) -> None:
        from resy import Well #put here to avoid circular import
        self.well = well
        if savepath is not None: 
            self.dosave= True
            self.savepath = savepath
            
                
    @abstractmethod
    def plot(self):
        '''
        To be implemented in subclasses

        '''
        ...

class Well3dPathPlotter(WellVisualizer):
    '''
    Creates a 3D plot of the wellpath along with all welltops
    '''
    def plot(self):
        #TODO
        ...
        
    