#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:07:45 2022

@author: mischasch
"""
import pandas as pd

class FieldSummarizer():
    '''
    summarize a field (typically: overview of well properties)
    '''
    def __init__(self, field):
        from resy import Field #put here to avoid circular import...
        self.field = field
        
    def summarize(self) -> pd.DataFrame:
        '''
        returns a pd.DataFrame with all well properties
        '''
        summary = pd.DataFrame([])
        for well in self.wells:
            summary.append(well.summary_short)
            
        return summary    