# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 22:16:17 2022

@author: SCHWEINGRUBER.MISC
"""
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt

class MplPlotterABC(ABC):
    def __init__(self, savepath:str = None,
                 ax = None) -> None:
        '''
        initialise Visualizer class

        Parameters
        ----------

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
        #from resy import Well #put here to avoid circular import
        #self.well = well
        if savepath is not None: 
            self.dosave= True
            self.savepath = savepath 
        if ax is None:
            _, self.ax = plt.subplots()
        else:
            self.ax = ax
            
        @abstractmethod
        def plot(self, **kwargs):
            '''
            To be implemented in subclasses
            
            Parameters
            -------
            **kwargs: named arguments, will be forwarded to the ax plotting 
            function
            
            Returns
            -------
            ax: given or new ax with plotted features

            '''
            ...