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

class AnalyticalWellTestSolution1DABC(ABC):
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
        
        #make sure distance is float if given as int
        if boundary_distance is not None:
            self.boundary_distance = float(boundary_distance)
        else:
            self.boundary_distance = None
        
    @abstractmethod
    def compute_drawdown(self, q, r, t) -> float : 
        #vectorize input
        q, r, t = vectorize_input([q, r, t])
        
class Boundary1D(ABC):
    '''
    ABC for 1D boundary conditions
    '''
    def __init__(self, analytical_solution, distance):
        '''
        create 1d boundary class. It requires the AnalyticalWellTestSolution1DABC
        that is applied at the pumping well.

        Parameters
        ----------
        analytical_solution: AnalyticalWellTestSolution1DABC
            the solution applied at the pumping well
        distance : float
            distance of the boundary to the pumping well [m]. The distance value must
            be contained in the r array.

        Returns
        -------
        None.

        '''
        self.analytical_solution = analytical_solution
        self. d = distance
        
        
    @abstractmethod
    def compute_boundary_effect(self, q, r, t):
        '''
        adds the effect of the boundary condition onto the 
        previously computed drawdowns
        
        Parameter
        -------
        
        q: float
            flow rate [m3/s]
        r: list or np.array
            list of radius at which to compute the boundary effect
        t: float
            time [s] at which to compute the boundary effect
            
        Returns
        -------
        The drawdown at the specified radius (r) and flow rate (q)

        '''
        image_dist = 2 * self.d - r
        self.abs_boundary_effect = self.analytical_solution.compute_drawdown(q, 
                                                                        image_dist,
                                                                        t)
        
        
class AnalyticalWellTestSolution():
    '''
    factory class for all kind of solutions and boundaries
    '''
    def __init__(self, 
                 solution: str,
                 T: float, S: float, rw:float = None,
                 boundary_distance:float = None, boundary_type:str = None,
                 skin_factor: float = 0,
                 Ts: float = None, rs: float = None):
        '''
        create a child object of AnalyticalWellTestSolution1DABC
        according to the selected inputs

        Parameters
        ----------
        solution : str, optional
            solution. Available: 'Theis'.
        T : float
            transmissivity [m2/s].
        S : sfloat
            storativity [-]
        rw: float
            well radius [m]
        boundary_distance : str, optional
            distnace [m] to the boundary.
        boundary_type : str
            'positive' (constant head boundary) or 
            'negative' (no flux boundary).
        skin_factor : float, optional
            skin factor (sigma). If this parameter is set, the following
            parameters will be ignored.
        Ts : float
            transmissivity [m2/s] of the skin zone. Only used if skin_factor = None
        rs: float
            well screen radius [m]. Only used if skin_factor is None
            

        Returns
        -------
        None.

        '''
        self.T = T
        self.S = S
        self.skin_factor = skin_factor

        #register new solutios here
        available_solutions = {'Theis': TheisBase(self.T, self.S)}
        
        
        if solution not in available_solutions:
            raise ValueError('Solution ' + str(solution) + ' not available')
        else:
            self.solution = available_solutions[solution]
            
        #register new boundaries here
        available_boundaries = {'positive': PositiveBoundary(self.solution,
                                                             boundary_distance),
                                'negative': NegativeBoundary(self.solution,
                                                             boundary_distance)}
        
        if boundary_type is not None:
            self.boundary = available_boundaries[boundary_type]
            
            if boundary_distance is not None:
                self.boundary_distance = boundary_distance
            else:
                raise ValueError('Boundary distance must be set')
        else:
            self.boundary = None
                
    def compute_drawdown(self, q, r, t):
        '''
        see super() for parameter documentation.
        '''
        q, r, t = vectorize_input([q, r, t])
        
        s_own = self.solution.compute_drawdown(q, r, t)
        if self.boundary is not None:
            s_bound = self.boundary.compute_boundary_effect(q, r, t)
        else:
            s_bound = 0
            
        if self.skin_factor != 0:
            s_skin = Skin(self.T, 
                          sigma = self.skin_factor).compute_drawdown(q)
        else:
            s_skin = 0
        
        #superposition principle
        s = s_own + s_bound + s_skin
        
        return s
        
class TheisWithBoundary(AnalyticalWellTestSolution1DABC):
    def compute_drawdown(self, q, r, t):
        #drawdown of pumping well
        s_own = TheisBase(self.T, self.S).compute_drawdown(q, r, t)
        
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
                
            s_image = TheisBase(self.T, self.S).compute_drawdown(q_image, image_dist, t)
        else: #no boundary
            s_image = 0
            
        #total drawdown computed by superposition

        return s_own + s_image
    
class Skin():
    '''
    class for Skin drawdown effects to be added to any analytical solution.
    
    Skin is computed according to Agarwal et al. (1970) and ASSUMES STEADY STATE.
    
    ATTENTION: neagtive values are not treated properly (their effect is highly exaggerated)
    TODO: transient skin
    '''
    def __init__(self, T: float, sigma: float = None, T_s: float = None,rs: float = None, rw: float = None):
        
        '''
        create Skin object. Sigma (Skin factor) can either be given directly or it will be
        computed.
        
        Parameters
        ----------
        T: float
            reservoir transmissivity [m2/s]
        sigma: float, optional
            skin factor (> 0 for additional drawdown created through skin zone). If this
            parameter is set, all following parameters will be ignored.
        T_s : float, optional
            transmissivity [m2/s] of the skin zone.
        rs : float, optional
            radius of the skin zone.
        rw : float, optional
            radius of the well screen.

        Returns
        -------
        None.

        '''
        
        self.T = T
        
        if sigma is not None:
            self.sigma = sigma
        else:
            self.T_s = T_s
            self.rs = rs
            self.rw = rw
            
            #compute skin factor
            self.sigma = (self.analytical_solution.T - self.T_s) / self.analytical_solution.T \
               * np.log(self.rs / self.rw)
           
    def compute_drawdown(self, q):
        '''
        computes the additional drawdown by the skin effect

        Parameters
        ----------
        q : float
            flow rate [m3/s].

        Returns
        -------
        drawdown [m]

        '''
        return q / (2 * np.pi * self.T) * self.sigma
    
class TheisBase(AnalyticalWellTestSolution1DABC):
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
    
class PositiveBoundary(Boundary1D):
    '''
    constant pressure boundary
    '''
    def compute_boundary_effect(self, q, r, t):
        
        super().compute_boundary_effect(q, r, t)
        return - self.abs_boundary_effect
    
class NegativeBoundary(Boundary1D):
    '''
    no flow boundary
    '''
    def compute_boundary_effect(self, q, r, t):
        
        super().compute_boundary_effect(q, r, t)
        return self.abs_boundary_effect
        

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

