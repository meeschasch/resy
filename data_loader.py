#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:27:26 2022

@author: mischasch
"""
import pandas as pd
from abc import ABC, abstractmethod

#local application import
from resy.well import Well
from resy.field import Field

class DataLoader(ABC):
    '''
    abstractr base class for any class that loads data
    '''
    def __init__(self, field: Field) -> None:
        self.field = field
        
    @abstractmethod
    def load(self):
        ...
        
class HydraulikDBLoader(DataLoader):
    '''
    loads all data from the SWM Hydraulikdatenbank
    '''
    def load(self):
        file = '/Users/mischasch/Documents/GitHub/resy/testdata.csv'
        d = pd.read_csv(file, index_col= False)
        
        for i, di in d.iterrows():
            if di.UWI in self.field.uwis:
                self.field[d.UWI].b_res = di.b
                self.field[d.UWI].c_res = di.c
            else:
                self.field.add_well(Well(uwi = di.UWI, c_res = di.c, b_res = di.c))
  
                
class SurveyLoader(DataLoader):
    def load(self):
        '''
        #TODO: implement such that to each well a corresponding survey is looked up, loaded andconverted to a survey object.

        Returns
        -------
        field
            DESCRIPTION.

        '''
        for well in self.wells:
            pass
        
        pass