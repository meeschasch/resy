#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:00:37 2022

@author: mischasch
"""
import pandas as pd
import numpy as np
        
class Welltop():
    '''
    a welltop
    '''
    def __init__(self, name, z_MD = None, z_TVD = None, x = None, y = None):
        '''
        

        Parameters
        ----------
        name : string
            welltop name (e.g. 'top Malm'.
        z_MD : float, optional. 
            depth [m MD]. The default is None.
        z_TVD : float, optional
            depth [m TVD].. The default is None.
        x: float, optional
            x coordinate.
        y: float, optional
            y coordinate.

        Returns
        -------
        None.

        '''
            
        self.name = name
        self.z_MD = z_MD
        self.z_TVD = z_TVD
        self.x = x
        self.y = y
        
    def __repr__(self):
        return self.summary.to_string(index = False)
    
    @property
    def summary(self):
        '''
        creates a pd.DataFramre with the welltop data

        Returns
        -------
        pd.DataFrame

        '''
        mask = np.array([True if self.name is not None else False,
                True if self.z_MD is not None else False,
                True if self.z_TVD is not None else False,
                True if self.x is not None else False,
                True if self.y is not None else False])
        
        vals = np.array([self.name,
                self.z_MD,
                self.z_TVD,
                self.x, 
                self.y])[mask]
        vals = [vals]
        
        cols = np.array(['Name', 'z_MD', 'z_TVD', 'x', 'y'])[mask]
        return pd.DataFrame(data = vals, columns = cols)
                
    
        
class Welltops():
    '''
    Collection of welltops of a well
    '''
    def __init__(self):
        self.welltops = []
        
    def __repr__(self):
        return self.summary.to_string(index = False)
    
    @property
    def summary(self):
        d = pd.DataFrame([])
        for wt in self.welltops:
            d = d.append(wt.summary)
            
        return d
        
    def add(self, name: str = None, 
            z_MD: float = None, z_TVD: float = None,
            welltop: Welltop = None) -> None:
        '''
        adds a welltop

        Parameters
        ----------
        welltop : Welltop, optional
            if this parameter is set, the others will be ignored. The default is None.
        name : str, optional
            Wellltop name. The default is None.
        z_MD : float, optional
            Welltop depth [m MD]. The default is None.
        z_TVD : float, optional
            Welltop depth [m TVD]. The default is None.

        '''
        if welltop is not None:
            #typecheck
            if not isinstance(welltop, Welltop):
                raise ValueError('not a Welltop')
            else:
                self.welltops.append(welltop)
        else:
            welltop = Welltop(name = name, z_MD = z_MD, z_TVD = z_TVD)
            self.welltops.append(welltop)
            
    def remove(self, name):
        '''
        removes welltop from welltop list

        Parameters
        ----------
        name : str
            name of welltop to remove.

        '''
        if name not in [wt.name for wt in self.welltops]:
            raise ValueError('Not in welltops')
        else:
            for wt in self.welltops:
                if wt.name == name:
                    self.welltops.remove(wt)
            
        
                
                
                
                
