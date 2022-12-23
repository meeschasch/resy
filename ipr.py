# -*- coding: utf-8 -*-
import warnings

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
        
        # #try to find measurement depth from string
        # allowed_measurement_str  =['surface', 'top reservoir']
        # if isinstance(measurement_depth, str):
        #     if measurement_depth not in allowed_measurement_str:
        #         raise ValueError(measurement_depth + ' is not a  \
        #                           valid input string')
           
        #     if measurement_depth == 'surface':
        #         self.measurement_depth = 0
                
        #     #if well is provided, extract depth from there
        #     if self.well is not None:
        #         try:
        #             if measurement_depth == 'top reservoir':
        #                 self.measurement_depth = self.well.welltops['top reservoir'].z_MD
        #         except:
        #             warnings.warn('no welltop for top reservoir could be found.  \
        #                           Measurement depth will be set to 0.')

               
                                  
                                  
        
        