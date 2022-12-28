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
        
class FieldWellSummarizerPandas(FieldSummarizer):
    '''
    collects a summary from all wells (as pd.DataFrames 
    and joines them into one DataFrame
    '''
    def summarize(self, sumtype):
        summarizers = {'general': WellSummarizerPandas,
                       'ipr': WellIPRSummarizerPandas}
        
        if sumtype not in summarizers:
            raise ValueError('Summary type ' + sumtype + ' not available')
        
        #get summary from all wells and join them together
        d = pd.DataFrame([])
        for well in self.field.wells:
            summarizer = summarizers[sumtype](well)
            
            d = d.append(summarizer.summarize())
            
        return d
    
class FieldGeneralWellSummarizer(FieldSummarizer):
    '''
    summarize general well data
    '''
    def summarize(self):
        d = pd.DataFrame([])
        for well in self.field.wells:
            d = d.append(well.summary('short'))
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