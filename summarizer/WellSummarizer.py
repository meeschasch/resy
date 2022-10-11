#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:04:39 2022

@author: mischasch
"""
from abc import ABC, abstractmethod
import pandas as pd

     
class WellSummarizer(ABC):
    '''
    ABC for well summarizer classes
    '''
    def __init__(self, well):
        self.well = well
    @abstractmethod
    def summarize(self):
        '''
        to be implemented by all subclasses

        '''
        ...
        
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
    
class WellSummarizerLong(WellSummarizer):
    def summarize(self) -> str:
        '''
        summarize all well data as string

        Returns
        -------
        str
            text block with all well data.

        '''
        summary = ('UWI: {:s},'.format(self.well.uwi)
                   + ' name:'
                   +   ('{:s}'.format(self.well.name) \
                       if self.well.name is not None \
                       else 'n.a')
                   + '\n \n'
                   '##################################################\n \n'
                   'Basic resevoir properties\n'
                   '--------------------------------------------------\n'
                   'Reservoir Pressure: '
                   + ('{:.2f} [bara]'.format(self.well.p_res)
                       if self.well.p_res is not None \
                       else 'n.a')
                   + '\n'
                   + 'Reservoir Temperature: '
                   + ('{:.2f} [°C]'.format(self.well.T_res)
                       if self.well.T_res is not None \
                       else 'n.a')
                   + '\n \n'
                   + 'Geochemistry \n'
                   '--------------------------------------------------\n'
                   'Salinity: '
                   + ('{:.2f} [mg/l]'.format(self.well.S)
                       if self.well.S is not None \
                       else 'n.a')
                   + '\n \n'
                   +'Casing design (bottom up)\n'
                   '--------------------------------------------------\n'
                   + (str(self.well.casing_design) \
                       if self.well.casing_design is not None \
                       else 'n.a' )   
                   + '\n\n'
                   +'Well hyddraulics: \n'
                    '--------------------------------------------------\n'
                   + 'b-coefficient: '
                   + ('{:.3f}'.format(self.well.b_res)
                        if self.well.b_res is not None \
                        else 'n.a')
                   + '\n'
                   +'c-coefficient (at Top Reservoir): '
                   + ('{:.3f}'.format(self.well.c_res) \
                       if self.well.c_res is not None \
                       else 'n.a')
                   + '\n\n'
                  
                   )
            
        return summary