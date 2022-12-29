#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 08:33:08 2022

@author: mischasch
"""
import warnings

class PTA():
    '''
    pressure transient analysis
    '''
    def __init__(self, perm :float = None, poro:float = None,
                 aquifer_thickness:float = None,
                 transmissibility:float = None,
                 porosity_thickness:float = None, 
                 transmissivity:float = None, 
                 storativity:float= None, 
                 skin: float = None,
                 wbs_type:str = None, well_model:str = None,
                 skin_type:str = None, 
                 reservoir_model:str = None, boundary_model:str = None,
                 m_d_comp: float = None):
        '''
        

        Parameters
        ----------
        perm : float, optional
            permeability [mD]. The default is None.
        poro : float, optional
            porosity []. The default is None.
        aquifer_thickness : float, optional
            aquifer thickness [m]. The default is None.
        transmissibility : float, optional
            transmissibility [mD m]. The default is None.
        porosity_thickness : float, optional
            porosity thickness [m]. The default is None.
        transmissivity : float, optional
            transmissivity [m2/s]. The default is None.
        storativity : float, optional
            storativity [-]. The default is None.
        skin: float, optional
            skin
        wbs_type : str, optional
            wellbore storage type ('constant' or 'changing'. The default is None.
        well_model : str, optional
            well model. The default is None.
        skin_type : str, optional
            skin type. The default is None.
        reservoir_model : str, optional
            reservoir model. The default is None.
        boundary_model : str, optional
            boundary model. The default is None.
        m_d_comp: float, optonal
            M = D for composite reservoirs.
            kh_outer_reservoir = kh_inner_reservoir / M

        Returns
        -------
        None.

        '''
        self.perm = perm
        self.poro = poro
        self.aquifer_thickness = aquifer_thickness
        self.transmissibility = transmissibility
        self.transmissivity = transmissivity
        self.porosity_thickness = porosity_thickness
        self.storativity = storativity
        self.wbs_type = wbs_type
        self.well_model = well_model
        self.skin_type = skin_type
        self.skin = skin
        self.reservoir_model = reservoir_model
        self.boundary_model = boundary_model
        self.m_d_comp = m_d_comp
        
        
class IPR():
    def __init__(self, b: float = None , c: float = None, 
                 measurement_depth = None,
                 range_certain: tuple = None, 
                 range_uncertain: tuple = None,
                 description: str = None,
                 origin: str = None):
        '''
        class representing an inflow performance relationship (IPR)

        Parameters
        ----------
        b : float
            b-coefficient
        c : float
            c-coefficient.
        measurement_depth: str or float
            either one of the following strings: 'surface', 'top reservoir',
            'esp'
            or float depicting the measurement depth (m MD) 
        range_certain : tuple (ascending), optional
            certain flow rate range. The default is None.
        range_uncertain : tuple (ascending), optional
            uncertain flow rate range. The default is None.
        description : str, optional
            description, e.g. 'PV/BDS/w Liner/Prod. The default is None.
        origin : str, optional
            origin of measurement, e.g: 'Aus Förderstufentest BDS'. The default is None.

        Returns
        -------
        None.

        '''
        self.b = b
        self.c = c
        self.range_certain = range_certain
        self.range_uncertain = range_uncertain
        self.description = description
        self.origin = origin
        self.measurement_depth = measurement_depth