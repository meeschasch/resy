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
        
    
class FieldGeneralWellSummarizer(FieldSummarizer):
    '''
    summarize general well data
    '''
    def summarize(self):
        d = pd.DataFrame([])
        for well in self.field.wells:
            d = d.append(WellIPRSummarizerPandas(welli).summarize())
        return d
    
class FieldIPRSummarizer(FieldSummarizer):
    '''
    summarize IPR data of all wells
    '''
    def summarize(self):
        d = pd.DataFrame([])
        
        for welli in self.field.wells:
            d = d.append(WellIPRSummarizerPandas(welli).summarize())
        
        return d
    
class FieldPTASummarizer(FieldSummarizer):
    '''
    summarize PTA data of all wells
    '''
    def summarize(self):
        d = pd.DataFrame([])
        
        for welli in self.field.wells:
            d = d.append(WellPTASummarizerPandas(welli).summarize())
        
        return d 