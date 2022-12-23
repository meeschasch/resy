#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:04:39 2022

@author: mischasch
"""
from abc import ABC, abstractmethod
import pandas as pd
from resy.summarizer.WelltopSummarizer import *
from resy.summarizer.CasingDesignSummarizer import CasingDesignSummarizer

     
class WellSummarizer(ABC):
    '''
    ABC for well summarizer classes
    '''
    def __init__(self, well):
        self.well = well
    @abstractmethod
    def summarize(self, dodislplay = False):
        '''
        to be implemented by all subclasses

        '''
        ...
        
class WellSummarizerShort(WellSummarizer):
    def summarize(self, dodisplay = False):
        
        summary = pd.DataFrame(index = [self.well.uwi])
        
        #compose dataframe
        summary.loc[self.well.uwi, 'p_res [bara]'] = self.well.p_res
        summary.loc[self.well.uwi, 'T_res [°C]'] = self.well.T_res
        summary.loc[self.well.uwi, 'b'] = self.well.ipr.b
        summary.loc[self.well.uwi, 'c'] = self.well.ipr.c
        summary.loc[self.well.uwi, 'S [mg/l]'] = self.well.S
        
        if 'surface' in self.well.welltops:
            summary.loc[self.well.uwi, 'GOK [mNN]'] = (self.well
            .welltops['surface'].z_NN)
        
        if 'top reservoir' in self.well.welltops:
            summary.loc[self.well.uwi, 'Top Reservoir [m TVD]'] = (self.well
            .welltops['top reservoir'].z_TVD)
            
        if dodisplay:
            display(summary)
        else:
            return summary
    
class WellSummarizerLong(WellSummarizer):
    def summarize(self, dodisplay = False) -> str:
        '''
        summarize all well data as string
        
        Parameters
        -------
        dodisplay: bool
            If True, a well summary will be displayed mixed with strings and 
            pandas dataframes (uses display, so only works in a Jupyter environment.
            If false, a string containing the entire 
            summary will be returned. Default is False.

        Returns
        -------
        str
            text block with all well data.

        '''
        summary_0 = ('##################################################\n'
                   +'UWI: {:s},'.format(self.well.uwi)
                   + ' Name: '
                   +   ('{:s}'.format(self.well.name) \
                       if self.well.name is not None \
                       else 'n.a')
                   + '\n'
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
                   + '\n \n')
            
        summary_1 = ('Casing design (bottom up)\n'
                   '--------------------------------------------------\n'
                   + (str(self.well.casing_design) \
                       if self.well.casing_design is not None \
                       else 'n.a' )   
                   + '\n\n')
            
        summary_2 = ('Well hydraulics: \n'
                    '--------------------------------------------------\n'
                   + 'b-coefficient: '
                   + ('{:.3f}'.format(self.well.ipr.b)
                        if self.well.ipr.b is not None \
                        else 'n.a')
                   + '\n'
                   + 'c-coefficient: '
                   + ('{:.3f}'.format(self.well.ipr.c)
                        if self.well.ipr.c is not None \
                        else 'n.a')
                   + '\n'
                   +'measurement depth: '
                   + ('{:.3f}'.format(self.well.ipr.measurement_depth) \
                       if self.well.ipr.measurement_depth is not None \
                       else 'n.a')
                   + '\n\n')
            
        summary_3 = ('Welltops: \n'
                    '--------------------------------------------------\n')
        
        summary_4 = WelltopsSummarizer(self.well.welltops).summarize(form = 'str')
        summary_5 = '\n\n'
        
        if dodisplay:
            print(summary_0)
            print(('Casing design (bottom up)\n'
                       '--------------------------------------------------'))
            
            if self.well.casing_design is not None:
                display(CasingDesignSummarizer(self.well.casing_design)
                        .summarize(form = 'pandas'))
            else:
                print('No Casing Design available')
            
            print(summary_2)
            print('Welltops: \n'
                        '--------------------------------------------------')
            
            display(WelltopsSummarizer(self.well.welltops)
                    .summarize(form = 'pandas'))
            
            print(summary_6)
              
        else:
            return summary_0 + summary_1 + summary_2 + summary_3 + \
                summary_4 + summary_5
