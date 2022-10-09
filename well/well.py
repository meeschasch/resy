#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 14:53:08 2022

@author: mischasch
"""

class Well():
    '''
    Contains information on a well and allows for computations of derived values
    '''
    
    def __init__(self, uwi, name = None, casing_design = None, survey = None, welltops = None, c_res = None, b_res = None, c_surf = None, T_res = None, p_res = None, p_regr = None, S = None, k = 3e-5, welltype = 'prod', z_ESP = None):
        '''

        Parameters
        ----------
        name : string
            well name
        casing_design : casing_design
            casing design for friction losses. It should include all completeions from top reservoir to the surface. Optional.
        survey : survey
            final surfey of a well. Optional.
        welltops: list of welltops
            List containing welltop objects. Optional. Note: it's easiest to set welltops using the set_welltop function. Welltops should include:
                - surface
                - top reservoir
                - final depth
        c_res : float
            c-coefficient at Top Reservoir. Optional.
        b_res : float
            b-coefficient at Top Reservoir. Optional.
        c_surf : float
            c-coefficient at surface. Optional.
        T_res : float
            Reservoir temperature [°C]. Optional.
        p_res : float
            Reservoir pressure [bara]. Optional.
        p_regr: float
            Reservoir pressure [bara] according to reservoir-wide regression of p_res vs. top reservoir
        S: float, optional
            salinity [mg/l]
        k: float
            friction losses roughness parameter. Default is 3e-5.
        welltype: 'prod' or 'inj', optional
            'prod' for a production well, 'inj' for an injection well. Default is 'prod'
        z_ESP: float, optional
            depth [m TVD] of ESP intake

        '''
        self.name = name
        self.uwi = uwi
        self.c_res = c_res
        self.b_res = b_res
        self.c_surf = c_surf
        self.T_res = T_res
        self.p_res = p_res
        self.S = S
        self.k = k
        self.welltops = welltops if welltops is not None else {} #welltops: dict (name, object of class welltop)
        
        self.casing_design = casing_design
        self.survey = survey
        self.welltype = welltype
        
# =============================================================================
#Properties
# =============================================================================
    #casing design
    @property
    def casing_design(self):
        '''
        casign design as used for friction losses computation

        '''
        return self._casing_design

    @casing_design.setter
    def casing_design(self, new_casing_design):
        #type check
        if new_casing_design is not None:
            if not isinstance(new_casing_design, CasingDesign):
                raise ValueError('casing design must be of type casing_design')
            
        self._casing_design = new_casing_design
        
    #survey
    @property
    def survey(self):
        '''
        well survey

        '''
        return self._survey

    @survey.setter
    def survey(self, new_survey):
        #type check
        if new_survey is not None:
            if not isinstance(new_survey, Survey):
                raise ValueError('survey must be of type survey')
        
        self._survey = new_survey
    
    #z_ESP
    @property
    def z_ESP(self):
        return self._z_ESP
    
    @z_ESP.setter
    def z_ESP(self, new_z_ESP):
        if new_z_ESP is not None:
            if self.welltype != 'prod':
                warnings.warn('setting z_ESP in an injection well')
  
            
# =============================================================================
# Methods to complete missing data (either by computing it or loading it from a database)
# =============================================================================
        
    def compute_c_surf(self, z_ref = 0):
        '''
        
        computes the surface c-coefficient based on the reservoir c-coefficient ant the friction losses
        
        Parameters
        ---------
        z_ref: float
            reference depth to compute the coefficient at (relevant for friction losses computation) [m TVD]. Default is 0.
        
        '''
        c_res = 0
        
        #TODO
        
        self.c_res = c_res

# =============================================================================
# Methods to set attributes
# =============================================================================
    def add_welltop(self, name, z_MD = None, z_TVD = None, x = None, y = None):
        '''
        adds a welltop to the well. Given values will be used unchecked. 
        TODO: Myres will try to complete missing values using the wells survey.

        Parameters
        ----------
        z_MD : float, optional
            depth [m MD].
        z_TVD : float, optional
            DESCRIPTION. The default is None.
        x: float, optional
            x coordinate
        y: float, optional
            y coordinate
            

        '''
        #check if at least one depth is given
        if not any([z_MD, z_TVD]):
            raise Exception('At least one depth (MD or TVD) must be given')
        
        
        #TODO: ompute TVD/MD, x, y from given information and survey
        new_welltop = Welltop(name, z_MD = z_MD, z_TVD = z_TVD, x = x, y = y)
        self.welltops[new_welltop.name] = new_welltop

# =============================================================================
# Methods to compute things at certain flow rates. Those methods should be vectorized.
# =============================================================================
    def get_fl_at_q(self, q, z_ref = 0, T_wellbore = None, p_res = None, p_surf = 10, S = None):
        '''
        computes friction losses of the entire well at one or many flow rates. Friction losses are by default computed
        at surface (production well) or at top reservoir(injection wells).
        
        Temperature is assumed as homogeneous throughout the wellbore.
        
        Flow direction (hence, direction of accumulation of friction losses) is assumed upwards in production wells
        and downwards in injection wells.
        
        Production wells: If you want 
        to comopute friction losses just until ESP intake, set z_ref to z_ESP

        Parameters
        ----------
        q : float or array of floats
            flow rate(s) [l/s] at which to compute friction closses.
        z_ref: float, optional
            reference depth [m TVD] to compute friction losses at. Default = 0.
        T_wellbore: float, optional
            homogeneous fluid temperature. in wellbore. Default in production wells is reservoir temperature,
            default in injection wells is 50°C.
        p_res: float, optional
            pressure at top reservoir [bara]. Will be obtained from well properties if not given here.
        p_surf: float, optional
            surface pressure [bara]. Default is 10.
            

        Returns
        -------
        fl : array of floats
            friction losses [bar] at the given flow rates.

        '''
        
        #choose wells properties if no other values are provided
        if T_wellbore is None:
            T_wellbore = self.T_res if self.welltype == 'prod' else 50
        if p_res is None:
            p_res = self.p_res
        if S is None:
            S = self.S
        
        #TODO: code below not final, to be tested
        if z_ref != 0:
            adj_casing_design = self.get_adjusted_cd_zref(z_ref)
        else:
            adj_casing_design = self.casing_design

        if not isinstance(q, Iterable): #only one q value
            fl = res.hyd_fl_well_aux(adj_casing_design.ids, adj_casing_design.ls, k = self.k,  q = q, p =  p_res, T = T_wellbore, S = S)
        else:
            fl = [res.hyd_fl_well_aux(adj_casing_design.ids, adj_casing_design.ls, k = self.k,  q = qi, p =  p_res, T = T_wellbore, S = S) for qi in q]
            
        #TODO
        return fl
    
    def get_p_at_q(q, z_ref = 0, T_res = None):
        '''
        computes the pressure at on or specific flow rates at a specific depth. 

        Parameters
        ----------
        q : float or array of float
            flow rate(s) at which to compute the pressure.
        z_ref : float, optional
            reference depth [m TVD] at which to compute.. The default is 0.
        T_res: float, optional
            Reservoir / production temperature. If not set, the wells reservoir temperature will be used.

        Returns
        -------
        p : float or array of float
            pressure [bara] at the specified depth at the specified flow rate.

        '''
        p = np.array()
        
        #TODO
        
        return p
    
# =============================================================================
# Other methods
# =============================================================================
    def summary(self, sumtype: str = 'long'):
        '''
        

        Parameters
        ----------
        sumtype : str
            'long' for a text based comprehensive summary,
            'short' for a pd.DataFrame with the most important data.
            Default is 'long'

        '''
        if sumtype == 'long':
            return WellSummarizerLong(self).summarize()
        elif sumtype == 'short':
            return WellSummarizerShort(self).summarize()
        else:
            raise ValueError('Summary type not available')
 