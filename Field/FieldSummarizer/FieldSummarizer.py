#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:26:18 2022

@author: mischasch
"""

class FieldSummarizer():
    '''
    summarize a field (typically: overview of well properties)
    '''
    def __init__(self, field: Field):
        self.field = field
        
    def summarize() -> pd.DataFrame:
        '''
        returns a pd.DataFrame with all well properties
        '''
        summary = pd.DataFrame([])
        for well in self.wells:
            summary.append(well.summary_short)