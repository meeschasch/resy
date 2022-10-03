#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 17:29:52 2022

@author: mischasch
"""
from collections.abc import Iterable
import pandas as pd, numpy as np, reseng_2101 as res

class survey():
    '''
    survey of a well. Index is MD. Incl, Azim and TVD refer to this index.
    '''
    def __init__(self, md, incl, azim, tvd = None):
        '''
        

        Parameters
        ----------
        md : np.array
            measured depth [m].
        incl : np.array
            inclination (deg). Horizontal = 0.
        azim : np.array
            azimuth (deg). North = 0, clockwise.
        tvd : np.array, optional
            true vertical depth [m]. The default is None.

        Returns
        -------
        None.

        '''   
        self.md = md
        self._incl = incl
        self._azim = azim
        self._tvd = tvd
        
# =============================================================================
#Properties
# =============================================================================
   #azimuth vector
    @property
    def azim(self):
        return self._azim
    
    @azim.setter
    def azim(self, new_azim):
        #type check
        if not isinstance(new_azim, Iterable):
            raise ValueError('object must be an iterable')
            
        #check length
        if len(new_azim != len(self.md)):
            raise ValueError('Azimuth array must be of equal length as the MD array')
            
        self._azim = new_azim
        
   #inclination vector
    @property
    def incl(self):
        return self._incl
    
    @incl.setter
    def incl(self, new_incl):
        #type check
        if not isinstance(new_incl, Iterable):
            raise ValueError('object must be an iterable')
            
        #check length
        if len(new_incl != len(self.md)):
            raise ValueError('Inclination array must be of equal length as the MD array')
            
        self._incl = new_incl
        
# =============================================================================
# Methods
# =============================================================================
    @np.vectorize
    def get_tvd_at_md(md):
        '''
        returns TVD values at one or more specific MD depths

        Parameters
        ----------
        md : float or array of floats
            MD value(s) at which TVD should be evaluated.

        Returns
        -------
        tvd : float or aray of float
            TVD value(s).

        '''
        #TODO
        tvd = np.array()
        
        return tvd
    
    def get_interpolated_survey(steps):
        '''
        compiles an interpolated survey from top to final depth
        

        Parameters
        ----------
        steps : float
            step width (m MD) which should be used.

        Returns
        -------
        md : array of floats
            m MD.
        tvd: array of floats
            m TVD
        incl: array of floats
            inclination [deg]
        azim: array of floats
            azimuth [deg]

        '''
        md, tvd, incl, azim = np.array()
        
        #TODO
        
        return md, tvd, incl, azim
        
        
        
class casing_design():
    '''
    '''
    
    def __init__(self, ls, ids = None, ods = None, wgs = None):
        '''
        Casing design as relevant for the computation of friction losses.
        A casing design must contain the lengths of each casing section. Inner diameters
        can be defined in two ways:
            - by providing the inner diameters directly (attribute ids)
            - by providing outer diameter and weight. Inner dianeters will be completed according 
            to the API standards.

        Parameters
        ----------
        ls : np.array
            Length of each casing section from Top Reservoir to surface (ascending) [m]
        ids : array of floats, optional
            inner diameters in inch (e.g. 6.625). The default is None.
        ods : array of floats, optional
            outer diameters in inch (e.g. 6.625). The default is None.
        wgs : array of floats, optional
            weights in pounds per feet [ppf]. The default is None.

        Returns
        -------
        None.

        '''
        self._ls = ls
        self._ids = ids
        self._ods = ods
        self._wgs = wgs
        
# =============================================================================
#       Properties
# =============================================================================
        
    #casing lengths
    @property
    def ls(self):
        '''
        array of casing lengths [m]

        '''
        return self._ls
    
    @ls.setter
    def ls(self, ls):
        #check for length integrity
        if not isinstance(ls, Iterable):
            raise ValueError('object must be an iterable')
            
        self._ls = ls
    
    #inner diameters
    @property
    def ids(self):
        '''
        array of inner casing diameters [m]. If it is not explicitly given, myres tries to obtain ids values 
        according to the API casing list using outer diameters and weights. For casings where no entry in the API casing list
        can be found, ids will be set to zero.
        
        '''
        #no ids given, get ids from API standard
        if self._ids is None and (self.ods is not None and self.wgs is not None):
            self._ids = np.zeros(len(self.ls))
            for i, v in enumerate(zip(self.ods, self.wgs)):
                try:
                    idsi = res.casing_id['{0:.4g}_{1:.4g}'.format(v[0], v[1])]
                    self._ids[i] = idsi
                except: #casing not in list
                    pass
                         
        return self._ids
    
    @ids.setter
    def ids(self, ids):
        #ids given
        #type check
        if ids is not None and not isinstance(ids, Iterable):
            raise ValueError('object must be an iterable')
            
        #check length integrity
        if ids is not None and len(ids) != len(self.ls):
            raise ValueError('Number of ids must correspond to number of lengths')
            
        self._ids = ids
        
    #outer diameters
    @property
    def ods(self):
        '''
        array of inner casing diameters [m]
        
        '''
        return self._ods
    
    @ods.setter
    def ods(self, ods):
        #type check
        if ods is not None and not isinstance(ods, Iterable):
            raise ValueError('object must be an iterable')
            
        #check length integrity
        if ods is not None and len(ods) != len(self.ls):
            raise ValueError('Number of ods must correspond to number of lengths')
            
            
        self._ods = ods
        
    #weights
    @property
    def wgs(self):
        '''
        Wandstärken [pound]
        
        '''
        return self._wgs
    
    @wgs.setter
    def wgs(self, wgs):
        #type check
        if not isinstance(wgs, Iterable):
            raise ValueError('object must be an iterable')
            
        #check length integrity
        if len(wgs) != len(self.ls):
            raise ValueError('Number of wgs must correspond to number of lengths')
            
        self._wgs = wgs
        

class welltop():
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
        
        
                        
        
class well():
    '''
    Contains information on a well and allows for computations of derived values
    '''
    
    def __init__(self, name, uwi = None, casing_design = None, survey = None, welltops = None, c_res = None, b_res = None, c_surf = None, T_res = None, p_res = None, p_regr = None, S = None, k = 3e-5):
        '''

        Parameters
        ----------
        name : string
            well name
        casing_design : casing_design
            casing design for friction losses. Optional.
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
            Reservoir pressure [bara] using linear regression.
        S: float, optional
            salinity [mg/l]
        k: float
            friction losses roughness parameter. Default is 3e-5.

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
        
        self._casing_design = casing_design
        self._survey = survey
        
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
        if not isinstance(new_casing_design, casing_design):
            raise ValueError('casing design must be of type casing_design')
            
        self._casign_design = new_casing_design
        
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
        if not isinstance(new_survey, survey):
            raise ValueError('survey must be of type survey')
        
        self._survey = new_survey
            
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
        new_welltop = welltop(name, z_MD = z_MD, z_TVD = z_TVD, x = x, y = y)
        self.welltops[new_welltop.name] = new_welltop
        
        

# =============================================================================
# Methods to compute things at certain flow rates. Those methods should be vectorized.
# =============================================================================
    def get_fl_at_q(self, q, z_ref = 0, T_res = None, p_res = None, S = None):
        '''
        computes friction losses of the entire well at one or many flow rates. Temperature is assumed as homogeneous throughout the wellbore.
        

        Parameters
        ----------
        q : float or array of floats
            flow rate(s) [l/s] at which to compute friction closses.
        z_ref: float, optional
            reference depth [m TVD] to compute friction losses at. Default = 0.
        T_res: production fluid temperature. 
            

        Returns
        -------
        fl : array of floats
            friction losses [bar] at the given flow rates.

        '''
        
        #choose wells properties if no other values are provided
        if T_res is None:
            T_res = self.T_res
        if p_res is None:
            p_res = self.p_res
        if S is None:
            S = self.S
        #TODO: adjust casing_design to z_ref (also: deal with inj. vs. prod. well)
        if not isinstance(q, Iterable): #only one q value
            fl = res.hyd_fl_well_aux(self.casing_design.ids, self.casing_design.ls, k = self.k,  q = q, p =  p_res, T = T_res, S = S)
        else:
            fl = [res.hyd_fl_well_aux(self.casing_design.ids, self.casing_design.ls, k = self.k,  q = qi, p =  p_res, T = T_res, S = S) for qi in q]
            
        #TODO
        return fl
    
    @np.vectorize
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
    
class inj_well(well):
    '''
    inherits from well, adds some specifics for injection wells
    '''
    def __init__(self, name, uwi = None, casing_design = None, inj_liner_ls = None, inj_liner_id = None, survey = None, z_TR = None, c_res = None, b_res = None, c_surf = None, T_res = None, p_res = None, p_regr = None, k = 3e-5):
        '''
        

        Parameters
        ----------
        inj_liner_ls : float, optional
            injection liner length. The default is None.
        inj_liner_id: float, optional
            injection liner inner diameter [m]. The default is None.


        Returns
        -------
        None.

        '''
        super().__init__(name, uwi, casing_design, survey, z_TR, c_res, b_res, c_surf, T_res, p_res, p_regr, k)
        
        self.inj_liner_ls = inj_liner_ls
        self.inj_liner_id = inj_liner_id
        
class prod_well(well):
    '''
    inherits from well, adds some specifics for production wells
    '''
    def __init__(self, name, uwi = None, casing_design = None, z_TKP = None, prod_liner_ls = None, prod_liner_id = None, survey = None, z_TR = None, c_res = None, b_res = None, c_surf = None, T_res = None, p_res = None, p_regr = None, k = 3e-5):
        '''
        

        Parameters
        ----------
        z_TKP : float, optional
            depth of ESP intake [m TVD]
        prod_liner_ls float, optional
            production liner inner diameter [m]
        prod_liner_ls: float, optional
            production liner length [m]


        Returns
        -------
        None.

        '''
        super().__init__(name, uwi, casing_design, survey, z_TR, c_res, b_res, c_surf, T_res, p_res, p_regr, k)
        
        self.inj_liner_ls = inj_liner_ls
        self.inj_liner_id = inj_liner_id
        
        
class field():
    '''
    A field contains a number of wells.
    '''
    def __init__(self, name, wells = None):
        '''
        

        Parameters
        ----------
        name : string
            field name.
        wells : array of wells
            all the wells in the field.

        '''
        self.name = name
        self._wells = wells
        
# =============================================================================
#Properties
# =============================================================================
    #array of all wells
    @property
    def wells(self):
        return self._wells
    
    @wells.setter
    def wells(self, new_wells):
        #type check
        if not isinstance(new_wells, Iterable):
            raise ValueError('wells must be a list or an array of wells')
        else:             
            for welli in new_wells:
                if not isinstance(welli, well):
                    raise ValueError('not all wells are of type well')
        
        self._wells = new_wells
            
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
        if not isinstance(new_well, well):
            raise ValueError('well must be of type well')
            
        self._wells.add(new_well)
        
    def refresh_from_database(file, wells = None, do_pres = True, do_p_regr = True, do_Tres = True, do_welltops = True, do_survey = True, do_casing_design = True):
        '''
        Refreshes / obtains well data from the common database. This function is hardcoded and requires a correctly formatted input file.

        Parameters
        ----------
        file : bool
            DESCRIPTION.
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
        data = pd.from_excel(file)
            
        if do_pres:
            #TODO
            pass
        if do_p_regr:
            #TODO
            pass
        if do_Tres:
            #TODO
            pass
        if do_welltops: 
            #TODO
            pass
        if do_survey:
            #TODO
            pass
        if do_casing_design:
            #TODO
            pass
        
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
            
                
                
                
                
                
                
                