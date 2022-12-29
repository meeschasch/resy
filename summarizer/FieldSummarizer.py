#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:07:45 2022

@author: mischasch
"""
import pandas as pd
from abc import ABC

from resy.summarizer.WellSummarizer import *

class FieldSummarizer(ABC):
    '''
    ABC for all field summarizers
    '''
    def __init__(self, field):
        #from resy import Field #put here to avoid circular import...
        self.field = field
        
    def summarize(self) -> pd.DataFrame:
        '''
        returns a pd.DataFrame with all well properties
        '''
        ...  
    
#%% Long string summarizer    
class FieldWellLongSummarizer(FieldSummarizer):
    '''
    output the long string summary of each well in the field
    '''
    def summarize(self):
        s = ''
        for welli in self.field.wells:
            s += WellSummarizerLong(welli).summarize()
        
        return s
        
#%% Pandas summarizer 
class FieldWellSummarizerPandas(FieldSummarizer, ABC):
    def __init__(self, field):
        '''
        composes a pd.DataFrame of all single well pandas summaries.
        Sublasses just need to set self.summarizer to a WellSummarizerPandas
        class.

        Parameters
        ----------
        field : FIELD.
        sumtpye : str
            for available sumtypes, see documentation 
            of class WellSummarizerPandas.

        Returns
        -------
        None.

        '''
        super().__init__(field)
        
    def summarize(self):
        #get pandas one-line summary of each well and append together
        d = pd.DataFrame([])
        
        for welli in self.field.wells:
            d = d.append(self.summarizer(welli).summarize())
            
        return d
    
class FieldGeneralWellSummarizer(FieldWellSummarizerPandas):
    '''
    inherits from FieldWellSummarizerPandas, sets self.summarizer
    toWellGeneralSummarizerPandas
    '''
    def __init__(self, field):
        super().__init__(field)
        
        self.summarizer = WellGeneralSummarizerPandas
        
class FieldIPRWelllSummarizer(FieldWellSummarizerPandas):
    '''
    inherits from FieldWellSummarizerPandas, sets self.summarizer
    WellIPRSummarizerPandas
    '''
    def __init__(self, field):
        super().__init__(field)
        
        self.summarizer = WellIPRSummarizerPandas

class FieldPTAWelllSummarizer(FieldWellSummarizerPandas):
    '''
    inherits from FieldWellSummarizerPandas, sets self.summarizer
    WellPTASummarizerPandas
    '''
    def __init__(self, field):
        super().__init__(field)
        
        self.summarizer = WellPTASummarizerPandas    
