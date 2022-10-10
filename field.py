#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:20:41 2022

@author: mischasch
"""
#third party imports
import pandas as pd
import numpy as np
from collections.abc import Iterable
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
import plotly

#local application import
from resy.well import Well

class Field():
    '''
    A field contains a number of wells.
    '''
    def __init__(self, name = None, wells = None):
        '''
        

        Parameters
        ----------
        name : string
            field name.
        wells : array of wells
            all the wells in the field.

        '''
        self.name = name
        
        self.wells = wells if wells is not None else []
    
    def __getitem__(self, index):
        '''
        returns the well if in list, else False.
        Identify a well by its UWI.
        '''
        if index not in self.uwis:
            return False
        else:
            getwell = None
            for well in self.wells:
                if well.uwi == index:
                    getwell = well
            return getwell
    
    def __setitem___(self, index, newwell):
        '''
        setting only allowed if well aready in field. Else, use add_well

        '''
        #check if well in field
        if index not in self.uwis:
            raise Exception('Well not in field. Use add_well to add new wells')
        else:
            for well in self.wells:
                if well.uwi == newwell.uwi:
                    well = newwell
                    
        
# =============================================================================
#Properties
# ===========================================================================
    #array of all wells
    @property
    def wells(self):
        return self._wells
    
    @wells.setter
    def wells(self, new_wells):
        if new_wells is not None:
            #type check
            if not isinstance(new_wells, Iterable):
                raise ValueError('wells must be a list or an array of wells')
            else:             
                for welli in new_wells:
                    if not isinstance(welli, Well):
                        raise ValueError('not all wells are of type well')
        
        self._wells = new_wells
    
    @property
    def uwis(self):
        if self.wells is not None:
            return [well.uwi for well in self.wells]
        else:
            return []
            
# =============================================================================
#Methods
# =============================================================================

    def add_well(self, new_well):
        '''
        adds a well to the field

        Parameters
        ----------
        well : well
            well.

        '''
        #type check
        if not isinstance(new_well, Well):
            raise ValueError('well must be of type well')
            
        self._wells.append(new_well)
        
    def refresh_from_database(self, wells = None, do_hydraulik_db = True, do_welltops = True, do_survey = True, do_casing_design = True):
        '''
        Refreshes / obtains well data from the common database. This function is hardcoded and requires a correctly formatted input file.

        Parameters
        ----------
        wells: list of strings, optional
            names of wells to refresh. If not set, all wells will be refreshed
        do_pres : bool, optional
            DESCRIPTION. The default is True.
        do_Tres : bool, optional
            DESCRIPTION. The default is True.
        do_welltops : bool, optional
            DESCRIPTION. The default is True.
        do_survey : bool, optional
            DESCRIPTION. The default is True.
        do_casing_design : bool, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        '''
        if do_hydraulik_db:
            from resy.data_loader import HydraulikDBLoader #import here to avoid circular import 
            HydraulikDBLoader(self).load()
            
        if do_welltops: 
            #TODO
            pass
        if do_survey:
            #TODO
            pass
        if do_casing_design:
            #TODO
            pass
        
    def compute_distances_welltop(self, welltop_name):
        '''
        computes a distance matrix of a welltop in all wells where the welltop is present.

        Parameters
        ----------
        welltop_name : string
            DESCRIPTION.

        Returns
        -------
        d : pd.DataFrame
            Row and column headers are all eligible wells, cell values is distance [m].

        '''
        wells_with_welltop = [] #names of well that contain this welltop
        
        for well in self.wells:
            if welltop_name in well.welltops:
                wells_with_welltop.append(well.name)
                
        d = pd.DataFrame(index = wells_with_welltop, columns = wells_with_welltop)
        
        #TODO: compute distances
        
        return d
    
    def plot(self, plot:str, savepath: str = None, backend = 'Matplotlib'):
        '''
        calls FieldVisualizer objects to plot field data.

        Parameters
        ----------
        plot : str
            plot type. Available:
                - 'ipr': plots IPR curves of all wells in the field
        backend: Matplotlib or Plotly. Default ist Matplotlib.


        '''
        if plot == 'ipr':
            if backend == 'Matplotlib':
                PyplotFieldIPRPlotter(self, savepath).plot()
            elif backend == 'Plotly':
                PlotlyFieldIPRPlotter(self, savepath).plot()
        else:
            raise ValueError(f"Plot type {plot} not available")
            
    def summary(self, sumtype: str = 'short'):
        '''
        creates a summary of all field data.

        Parameters
        ----------
        sumtype : str, optional
            'short' for a pd.DataFrame with the most 
            important well data. 'long' for a long description
            of all wells. The default is 'short'.

        '''
        if sumtype == 'long':
            s = ''
            for well in self.wells:
                s += well.summary(sumtype = 'long')
            return s
        
        elif sumtype == 'short':
            d = pd.DataFrame([])
            for well in self.wells:
                d = d.append(well.summary('short'))
            return d
        else:
            raise ValueError('Summary type not available')
            
# =============================================================================
# Classes to visualize the field            
# =============================================================================
class FieldVisualizer(ABC):
    '''
    Abstract base class for any class that visualizes a field
    '''
    def __init__(self, field: Field, savepath: str = None) -> None:
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
    
# =============================================================================
# Classes to summarize a field
# =============================================================================
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