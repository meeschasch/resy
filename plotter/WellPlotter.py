#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:02:34 2022

@author: mischasch
"""
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

from resy.plotter.Plotter import MplPlotterABC

class MplWellPlotterABC(MplPlotterABC, ABC):
    '''
    Abstract base class for any well plotters
    '''
    def __init__(self, well = None, savepath:str = None,
                 ax = None) -> None:
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

        Returns
        -------
        None
            DESCRIPTION.

        '''
        super().__init__(savepath = savepath, ax = ax)
        
        from resy import Well #put here to avoid circular import
        self.well = well
        
class MplWellIPRPlotter(MplWellPlotterABC):
    '''
    plot a well IPR in matplotlib. 
    '''
    
    def plot(self, q: tuple = (0,150), **kwargs):
        '''
        

        Parameters
        ----------
        q : tuple, optional
            DESCRIPTION. The default is (0,150).
        **kwargs : named arguments
            the following named arguments are forwarded to the pyplot plotting
            function: 'color'.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        if not any([self.well.ipr.b, self.well.ipr.c]):
            raise ValueError('Well has no ipr to base plot on')
        q = np.arange(*q)
        
        
        dp = self.well.ipr.b * q + self.well.ipr.c * q**2
        
        #no ranges are set
        if all([self.well.ipr.range_certain is None,
                    self.well.ipr.range_uncertain is None]):
            
            self.ax.plot(q, dp, **kwargs)
            
        #ranges are given
        else:
            #create filters for lower and higher uncertain range and for the
            #certain range
            
            filter_uncertain_low = (q >= self.well.ipr.range_uncertain[0]) & \
                              (q <= self.well.ipr.range_certain[0])
                              
            filter_uncertain_high = (q >= self.well.ipr.range_certain[1]) & \
                              (q <= self.well.ipr.range_uncertain[1])
                              
            filter_certain = (q >= self.well.ipr.range_certain[0]) & \
                              (q <= self.well.ipr.range_certain[1])
            
            #plot 
            self.ax.plot(q[filter_uncertain_low], dp[filter_uncertain_low],
                         ls = '--', **kwargs)
            self.ax.plot(q[filter_uncertain_high], dp[filter_uncertain_high],
                         ls = '--', **kwargs)
            self.ax.plot(q[filter_certain], dp[filter_certain],
                         ls = '-', label = self.well.uwi, **kwargs)
        
        
        #prettify plot
        self.ax.set_xlabel('q [l/s')
        self.ax.set_ylabel('dP [bar]')
        self.ax.grid(ls = '--')
        
        if 'legend' in kwargs:
            if kwargs['legend']:
                self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        return self.ax
    

    