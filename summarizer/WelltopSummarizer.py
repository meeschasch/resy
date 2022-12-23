# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 13:56:33 2022

@author: SCHWEINGRUBER.MISC
"""
import numpy as np
import pandas as pd

#TODO
class WelltopSummarizer():
    def __init__(self, welltop):
        self.welltop = welltop
        
    def summarize(self, form = 'str'):
        '''
        creates a pd.DataFramre with the welltop data
        Parameter
        -------
        form: string, optional
            return format, either "pandas" or "string". Default is "str"
        Returns
        -------
        pd.DataFrame

        '''
        mask = np.array([True if self.welltop.name is not None else False,
                True if self.welltop.z_MD is not None else False,
                True if self.welltop.z_TVD is not None else False,
                True if self.welltop.z_NN is not None else False,
                True if self.welltop.x is not None else False,
                True if self.welltop.y is not None else False])
        
        vals = np.array([self.welltop.name,
                self.welltop.z_MD,
                self.welltop.z_TVD,
                self.welltop.z_NN,
                self.welltop.x, 
                self.welltop.y])[mask]
        vals = [vals]
        
        cols = np.array(['Name', 'z_MD', 'z_TVD', 'z_NN', 'x', 'y'])[mask]
        
        result = pd.DataFrame(data = vals, columns = cols)
        
        if form == 'pandas':
            return result
        elif form == 'str':
            return result.to_string(index = False)
    
class WelltopsSummarizer():
    def __init__(self, welltops):
        self.welltops = welltops
        
    def summarize(self, form = 'str'):
        '''
        summarizes a welltops dict

        Parameters
        ----------
        form : string, optional
            if 'str', returns a string. If 'pandas', returns
            a pandas.DataFrame. The default is 'str'.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        summary = pd.DataFrame()
        
        for wt in self.welltops:
            summary = summary.append(WelltopSummarizer(self.welltops[wt])
                                     .summarize(form = 'pandas'))
        if len(summary) > 0:   
            if form == 'str':
                return summary.to_string(index = False)
            elif form == 'pandas':
                return summary
        else:
            return ('no welltops defined')