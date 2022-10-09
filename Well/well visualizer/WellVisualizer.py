#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:17:53 2022

@author: mischasch
"""

class WellVisualizer(ABC):
    '''
    Abstract base class for any well plotters
    '''
    def __init__(self, well: Well, savepath:str = None) -> None:
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