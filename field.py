#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:20:41 2022

@author: mischasch
"""
#third party imports
import pandas as pd
from collections.abc import Iterable

#local application import
from resy.well import Well
from resy.visualizer import FieldVisualizer

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
                FieldVisualizer.PyplotFieldIPRPlotter(self, savepath).plot()
            elif backend == 'Plotly':
                FieldVisualizer.PlotlyFieldIPRPlotter(self, savepath).plot()
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
            