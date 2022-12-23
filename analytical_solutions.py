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

class Aquifer(ABC):
    '''
    ABC for any analytical aquifer solution
    '''
    def __init__(self, T, S):
        '''
        creates an Aquifer class with hydraulic aquifer characteristics

        Parameters
        ----------

        T :  float
            Transmissivity [m2/s].
        S : float
            Storativity [-].

        Returns
        -------
        None.

        '''
        self.T = T
        self.S = S
        

class Theis(Aquifer):
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
        q, r, t = vectorize_input([q, r, t])
        
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
               
aq = Theis(1e-3, 1e-6)

q = 200e-3
r = 400
t = np.linspace(0,20000000,200)

s = aq.compute_drawdown(q, r, t)

plt.plot(t, s)

