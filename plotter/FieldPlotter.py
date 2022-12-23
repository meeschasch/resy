#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:03:45 2022

@author: mischasch
"""
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm

import numpy as np
import copy

from resy.plotter.Plotter import MplPlotterABC
from resy.plotter.WellPlotter import *


class FieldWellSelector():
    '''
    selects wells from a field based on a lsit of UWI
    '''
    def __init__(self, field, well_list: list = None):
        self.field = copy.deepcopy(field) #deepcopy to avoid loosing wells by selections
        self.well_list = well_list
        
        from resy.field import Field #avoid circular import
    
    def select(self):
        
        '''
        removes wells from a field that are not within a selection list

        Returns
        -------
        a Field containing only the wells that are selected

        '''
        
        #remove wells from field that should not be plotted
        if self.well_list is not None:
            missing_wells = np.isin(np.array(self.field.uwis),
                                    np.array(self.well_list),
                                    invert = True)
            
            missing_wells = np.array(self.field.uwis)[missing_wells]
        
            self.field.remove_wells(missing_wells)  
        
        return self.field
        
class MplFieldPlotterABC(MplPlotterABC, ABC):
    '''
    Abstract base class for any class that visualizes a field
    '''
    def __init__(self, field = None, savepath:str = None,
                 ax = None, plotwells = None) -> None:
        '''
        initialise WellVisualizer class

        Parameters
        ----------
        well : Well
            Well.
        savepath : str, optional
            Path to save plot to. The default is None.
        ax : matpotlib.pyplot.axes, optional
            ax to plot on. If None, a new ax will be create.
            The default is None.
        plotwells: list, optional
            If not None, plots only the wells corresponding to the UWIs in the 
            provided list. If None, all wells are plotted.
    
        

        Returns
        -------
        None
            DESCRIPTION.

        '''
        super().__init__(ax = ax, savepath = savepath)
        from resy import Field #put here to avoid circular import
        
        #remove wells from field that should not be plotted
        self.field = FieldWellSelector(field, plotwells).select()
                

class MplFieldIPRPlotter(MplFieldPlotterABC):
    '''
    plot all IPR of wells in a field
    '''
    def plot(self, **kwargs):
        '''
        plots IPR for the selected wells

        Parameters
        ----------
        **kwargs : named arguments
            forwarded to the pyplot plotting function.

        Returns
        -------
        None.

        '''
        #_, ax = plt.subplots()
        color = iter(cm.rainbow(np.linspace(0, 1, len(self.field.wells))))
        
        for well in self.field.wells:
            if any([well.ipr.b, well.ipr.c]):
                (MplWellIPRPlotter(well = well, ax = self.ax)
                    .plot(color = next(color), 
                    alpha = 0.5, **kwargs))

#class MplFieldWellPropertyCorrelator(MplFieldPlotterABC)            
        #plt.show()
# class FieldWellpathPlotter(FieldVisualizer):
#     '''
#     Plots the surface trajectories of all wells
#     '''
#     def plot(self):
#         #TODO
#         ...
        
# class FieldWellpathPlotter(FieldVisualizer):
#     '''
#     Plots the surface trajectories of all wells
#     '''
#     def plot(self):
#         #TODO
#         ...
        
    
# class PlotlyFieldIPRPlotter(FieldVisualizer):
#     '''
#     Plots the IPR curves of all wells in the field with Plotly
#     '''
#     def visualize(self, q: tuple = (0,150)):
#         q = np.arange(*q)
#         dp = pd.DataFrame(index = q, columns = self.field.uwis)
#         for well in dp.columns:
#             dp[well] = self.field[well].b_res * q + self.field[well].c_res * q**2
                          
#         dp['q']= q
#         dp = dp.melt(id_vars = 'q', var_name = 'well', value_name = 'dP')
 
#         fig = px.line(dp, x = 'q', y = 'dP', color = 'well')
#         fig.show()
        
# class PyplotFieldIPRPlotter(FieldVisualizer):
#     # def __init__(self, field, savepath):
#     #     super().__init__(self, field, savepath)
        
#     def visualize(self, q: tuple = (0,150)):
#         '''
#         Plots the IPR curves of all wells in the field with Pyplot
#         '''
#         q = np.arange(*q)
#         fig, ax = plt.subplots()
#         for well in self.field.wells:
#             ax.plot(q, well.b_res * q + well.c_res * q**2, label = well.uwi)
        
#         ax.legend()
#         ax.set_xlabel('q [l/s]')
#         ax.set_ylabel('dP [bara]')
        
#         return fig