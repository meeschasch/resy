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
from resy.plotter.FieldPlotter import *
from resy.summarizer.FieldSummarizer import *

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
        
    def remove_wells(self, uwis):
        '''
        removes wells from the field
        
        Paramters
        -------
        wells: one UWI as string or list of UWIs as strings
        '''
        #make array if only one value provided
        if isinstance(uwis, str):
            uwis = [uwis]
        
        #remve wells
        for uwi in uwis:
            if uwi not in self.uwis:
                raise ValueError('Well ' + uwi + ' not in field')
            else:
                self.wells.remove(self[uwi])
        
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
            from resy.data_loader import CasingDesignLoader
            CasingDesignLoader(self).load()
        
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
    
    def plot_mpl(self, plottype, plotwells = None, savepath: str = None, **kwargs):
        '''
        plots a well in a defined way.

        Parameters
        ----------
        plottype : str
            one of the following options:
            'IPR'
        plotwells: well uwi or list those, these wells will be plotted
        savepath: str or Path
            path to save figure to. If None, figure is not saved.
        **kwargs: named arguments are forwareded to the plotter object

        Returns
        -------
        None.

        '''
        #define ax (functionality to plot field plots on an existing ax is not
        #implemented)
        _, ax = plt.subplots()
        
        #register new plotters here
        plotters = {'IPR': MplFieldIPRPlotter(ax = ax, 
                                              field = self,
                                              plotwells = plotwells,
                                              savepath = savepath)}
        

        plotter = plotters[plottype]
        
        plotter.plot(**kwargs)
        
        return ax
            
    def summary(self, sumtype: str = 'general'):
        '''
        creates a summary of all field data.

        Parameters
        ----------
        sumtype : str, optional
            'general' for a pd.DataFrame with the most 
            important well data.
            'ipr' for IPR data
            TODO 'pta' for PTA data
            of all wells. The default is 'short'.

        '''
        summaries = {'general': FieldGeneralWellSummarizer,
                     'ipr': FieldIPRSummarizer}
        
        if sumtype not in summaries:
            raise ValueError('Summary type ' + sumtype + ' not available')
        
        summarizer = summaries[sumtype](self)
        
        return summarizer.summarize()