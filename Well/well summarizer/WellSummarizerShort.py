#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:16:48 2022

@author: mischasch
"""

class WellSummarizerShort(WellSummarizer):
    def summarize(self):
        
        summary = pd.DataFrame(index = [self.well.uwi])
        
        #compose dataframe
        summary.loc[self.well.uwi, 'p_res [bara]'] = self.well.p_res
        summary.loc[self.well.uwi, 'T_res [°C]'] = self.well.T_res
        summary.loc[self.well.uwi, 'b_res'] = self.well.b_res
        summary.loc[self.well.uwi, 'c_res'] = self.well.c_res
        summary.loc[self.well.uwi, 'S [mg/l]'] = self.well.S
        
        return summary
        