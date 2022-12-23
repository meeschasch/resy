# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:03:35 2022

@author: SCHWEINGRUBER.MISC
"""

import numpy as np
import pandas as pd

#TODO
class CasingDesignSummarizer():
    def __init__(self, casing_design):
        '''
        creates a class to summarize a casing design.

        Parameters
        ----------
        casing_design : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.casing_design = casing_design
        
    def summarize(self, form = 'str'):
        '''
        Parameter
        -------
        form: string, optional
            return format, either "pandas" or "string". Default is "str"        

        Returns
        -------
        string
            table representation of the casing design.

        '''
        result = pd.DataFrame(data = np.array([self.casing_design.ls, 
                                               self.casing_design.ids, 
                                               self.casing_design.ods,
                                               self.casing_design.wgs,
                                               self.casing_design.descr]).T,
                              columns = ['ls', 'ids', 'ods', 'wgs', 'descr'])
        if form == 'str':
           return result.to_string(index = False)
        elif form == 'pandas':
            return result
