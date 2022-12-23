#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 22:39:36 2022

@author: mischasch
"""
from scipy.special import exp1
import numpy as np
from collections.abc import Iterable
import numbers
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt

class AnalyticalWellTestSolution1D(ABC):
    '''
    ABC for any analytical aquifer solution
    '''
    def __init__(self, T, S,
                 boundary_type = None, boundary_distance = None):
        '''
        OABC for one-dimensional analytical welltest solutions
        Parameters
        ----------

        T :  float
            Transmissivity [m2/s].
        S : float
            Storativity [-].
        boundary_type: str, optional
            Either 'positive' (for constant pressure boundaries, 
            or 'negative' for no-flow boundaries). If None, no boundary will
            be applied
        boundary_distance: float, optional
            Distance of the pumping well to the voundary

        Returns
        -------
        None.

        '''
        self.T = T
        self.S = S
        self.boundary_type = boundary_type
        
        if boundary_distance is not None:
            self.boundary_distance = float(boundary_distance)
        else:
            self.boundary_distance = None
        
    @abstractmethod
    def compute_drawdown(self, q, r, t) -> float : 
        #vectorize input
        q, r, t = vectorize_input([q, r, t])
        
class TheisWithBoundary(AnalyticalWellTestSolution1D):
    def compute_drawdown(self, q, r, t):
        #drawdown of pumping well
        s_own = Theis(self.T, self.S).compute_drawdown(q, r, t)
        
        #drawdown of image well
        if self.boundary_type is not None:
            image_dist = 2 * self.boundary_distance - r
            if self.boundary_type == 'positive':
                q_image = -q
            elif self.boundary_type == 'negative':
                q_image = q
            else:
                raise ValueError('boundary type ' + str(self.boundary_type) +
                                 ' not known')
                
            s_image = Theis(self.T, self.S).compute_drawdown(q_image, image_dist, t)
        else: #no boundary
            s_image = 0
            
        #total drawdown computed by superposition

        return s_own + s_image
    
class Theis(AnalyticalWellTestSolution1D):
    '''
    analytical solution according to Theis (1935)
    '''
    def compute_drawdown(self, q, r, t):
        '''
        computes the drawdown at a specific distance from the well
        and at a specif time

        Parameters
        ----------
        q: float or array of floats
        r : float or array of floats
            distance to well [m].
        t : float or array of floats
            time since pumping started [s].

        Returns
        -------
        float or array of float containing the drawdown

        '''
        #vectorize input
        super().compute_drawdown(q, r, t)
        
        
        #compute u
        u = ((r ** 2) * self.S) / (4 * self.T * t)
        
        #compute drawdown, thank to:
        # https://scipython.com/blog/linear-and-non-linear-fitting-of-the-theis-equation/
        s = q / 4 / np.pi / self.T * exp1(u)

        return s
    
def vectorize_input(inputs):  
    '''
    vetorizes all input values or arrays to a common length.
    Inputs can be either scalars or arrays. In case of arrays, they all must 
    be of the same length.

    Parameters
    ----------
    inputs : list
        DESCRIPTION.

    Returns
    -------
    inputs as list (same order as input parameter)

    '''
    #all inputs are arrays
    if all([isinstance(i, Iterable) for i in inputs]):
        #not all arrays are of the same legnth
        if len(np.unique([len(i) for i in inputs])) != 1:
               raise ValueError('input arrays must be of the same length')
        #all input arrays same length --> ok
        else:
            return inputs
        
       
    #all inputs are scalars --> ok
    elif all([isinstance(i, numbers.Number) for i in inputs]):
        return inputs
    #some arrays, some scalars
    else:
       #compose lists of all iterables
       iterables = []
       for i in inputs:
           if isinstance(i, Iterable):
               iterables.append(i)
               
       #check if all iterables have the same length
       if len(np.unique([len(i) for i in iterables])) != 1:
           raise ValueError('input arrays must be of the same length')
       #expand scalars to common iterables length
       else:
           common_len = len(iterables[0])
           for i, inp in enumerate(inputs):
               #only change scalars
               if isinstance(inp, numbers.Number):
                   inputs[i] = np.ones(common_len) * inp

           
           return inputs

