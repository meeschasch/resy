#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:03:45 2022

@author: mischasch
"""
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
import plotly.io
import plotly.express as px
from pathlib import Path
import os
import numpy as np
import pandas as pd


class FieldVisualizer(ABC):
    '''
    Abstract base class for any class that visualizes a field
    '''
    def __init__(self, field, savepath: str = None) -> None:
        from resy import Field #put here to avoid circular imoort
        self.field = field
        if savepath is not None: 
            self.dosave= True
            self.savepath = savepath
        else:
            self.dosave = False
            
        #set matplotlib style
        plt.style.use('seaborn')
        plotly.io.renderers.default='browser'
    
    def plot(self):
        '''
        first, runs the visualize method in the sublasses. Then, saves the figure if required.
        '''
        fig = self.visualize()
        
        if self.dosave:
            if not Path(self.savepath).exists():
                os.mkdir(self.savepath)
            
            try:
                fig.savefig(Path(self.savepath) / 'ipr.png')
            except:
                raise Exception('File could not be saved')
        
    @abstractmethod
    def visualize(self):
        '''
        To be implemented in subclasses. Must return a pyplot figure.

        '''
        ...
    
class FieldWellpathPlotter(FieldVisualizer):
    '''
    Plots the surface trajectories of all wells
    '''
    def plot(self):
        #TODO
        ...
        
    
class PlotlyFieldIPRPlotter(FieldVisualizer):
    '''
    Plots the IPR curves of all wells in the field with Plotly
    '''
    def visualize(self, q: tuple = (0,150)):
        q = np.arange(*q)
        dp = pd.DataFrame(index = q, columns = self.field.uwis)
        for well in dp.columns:
            dp[well] = self.field[well].b_res * q + self.field[well].c_res * q**2
                          
        dp['q']= q
        dp = dp.melt(id_vars = 'q', var_name = 'well', value_name = 'dP')
 
        fig = px.line(dp, x = 'q', y = 'dP', color = 'well')
        fig.show()
        
class PyplotFieldIPRPlotter(FieldVisualizer):
    # def __init__(self, field, savepath):
    #     super().__init__(self, field, savepath)
        
    def visualize(self, q: tuple = (0,150)):
        '''
        Plots the IPR curves of all wells in the field with Pyplot
        '''
        q = np.arange(*q)
        fig, ax = plt.subplots()
        for well in self.field.wells:
            ax.plot(q, well.b_res * q + well.c_res * q**2, label = well.uwi)
        
        ax.legend()
        ax.set_xlabel('q [l/s]')
        ax.set_ylabel('dP [bara]')
        
        return fig