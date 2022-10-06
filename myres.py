#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 17:29:52 2022

@author: mischasch
"""
from collections.abc import Iterable
import pandas as pd
import numpy as np
import reseng_2101 as res
import warnings
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class Survey():
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
        self.incl = incl
        self.azim = azim
        self.tvd = tvd
        
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
        if new_azim is not None:
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
        if new_incl is not None:
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
        #TODO (vectorized)
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
        
        
        
class CasingDesign():
    '''
    '''
    def get_ids_from_api(self):
        '''
        tries to fill missing id values from the API casing list using od and weight

        '''
        #TODO
        pass
        
    def __init__(self, ls, ids = None, ods = None, wgs = None):
        '''
        Casing design as relevant for the computation of friction losses.
        A casing design must contain the lengths of each casing section. 
        TODO. Inner diameters
        can be defined in two ways:
            - by providing the inner diameters directly (attribute ids)
            - by providing outer diameter and weight. Inner dianeters will be completed according 
            to the API standards.

        Parameters
        ----------
        ls : np.array
            Length of each casing section from Top Reservoir to surface (ascending) [m]
        ids : array of floats, optional
            inner diameters in inch (e.g. 6.625). The default is None. TODO: If it is not explicitly given, myres tries to obtain ids values 
            according to the API casing list using outer diameters and weights. For casings where no entry in the API casing list
            can be found, ids will be set to zero.
        ods : array of floats, optional
            outer diameters in inch (e.g. 6.625). The default is None.
        wgs : array of floats, optional
            weights in pounds per feet [ppf]. The default is None.

        Returns
        -------
        None.

        '''
        self.ls = ls
        self.ids = ids
        self.ods = ods
        self.wgs = wgs
    
# =============================================================================
# get item and set item methods        
# =============================================================================
    def __getitem__(self, index) -> dict:
        '''
        return the nth element of the casing design.

        Parameters
        ----------
        index : int
            index (zero indexed).

        Returns
        -------
        dict with fields: l, id, od, wg

        '''
        #type check
        if not isinstance(index, int):
            raise ValueError('Casing can only be indexed by integer')
            
        #length check
        if index > len(self.ls) - 1:
            raise ValueError('Index out of bounds')
            
        return {'l': self.ls[index],
                'id': self.ids[index],
                'od': self.ods[index],
                'wg': self.wgs[index]}
    
    def __setitem__(self, index, new) -> None:
        '''
        sets a casing in a casing design. Cannot be used to add a new casing (see funtion add_section for that)

        Parameters
        ----------
        index : int
            DESCRIPTION.
        new : dict
            fields: l, id, od, wg.

        Returns
        -------
        None
            DESCRIPTION.

        '''
        #type check
        if not isinstance(new, dict):
            raise ValueError('Section casing design must be provided as dictionary')
            
        #check index
        if index > len(self.ls):
            raise ValueError('index out of bounds')
            
        #set item
        self.ls[index] = new['l']
        self.ids[index] = new['id']
        self.ods[index] = new['od']
        self.wgs[index] = new['wg']
        
    def __repr__(self):
        return pd.DataFrame(data = np.array([self.ls, self.ids, self.ods, self.wgs]).T, columns = ['ls', 'ids', 'ods', 'wgs']).to_string(index = False)
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
            
            
        self._ls = np.array(ls)
    
    #inner diameters
    @property
    def ids(self):
        '''
        array of inner casing diameters [m]. 
        
        '''
                         
        return self._ids
    
    @ids.setter
    def ids(self, new_ids):
        #ids given
        #type check
        if new_ids is not None:
            if not isinstance(new_ids, Iterable):
                raise ValueError('object must be an iterable')
                
            #check length integrity
            if len(new_ids) != len(self.ls):
                raise ValueError('Number of ids must correspond to number of lengths')
                
            #check ascending ids (must be from bottom to top)
            
            #if not np.all(np.diff(new_ids) > 0):
            #    raise ValueError('inner diameters must be ascending (from top reservoir to surface')
          
            self._ids = np.array(new_ids)
            
        else:   
            self._ids = None
        
    #outer diameters
    @property
    def ods(self):
        '''
        array of inner casing diameters [m]
        
        '''
        return self._ods
    
    @ods.setter
    def ods(self, new_ods):
        #type check
        if new_ods is not None:
            if not isinstance(new_ods, Iterable):
                raise ValueError('object must be an iterable')
                
            #check length integrity
            if len(new_ods) != len(self.ls):
                raise ValueError('Number of ods must correspond to number of lengths')
                
                
            self._ods = np.array(new_ods)
        else:
            self._ods = None
        
    #weights
    @property
    def wgs(self):
        '''
        Wandstärken [pound]
        
        '''
        return self._wgs
    
    @wgs.setter
    def wgs(self, new_wgs):
        #type check
        if new_wgs is not None:
            if not isinstance(new_wgs, Iterable):
                raise ValueError('object must be an iterable')
                
            #check length integrity
            if len(new_wgs) != len(self.ls):
                raise ValueError('Number of wgs must correspond to number of lengths')
            
            self._wgs = np.array(new_wgs)
        else:
            self._wgs = None
        
# =============================================================================
#Methods
# =============================================================================
    def remove_section(self, index):
        '''
        removes a section from the casing design. 

        Parameters
        ----------
        section : int or list of ints
            index of section in casing design to remove (0 = lowest section, -1 = uppermost section).

        '''
        index = np.array(index)
        #check length
        if any(index > len(self.ls) - 1):
            raise ValueError('index of section higher than sections in casing design')
        
        reduce = 0
        for i in index:
            i -= reduce
            #remove section from ls, ids, ods, wgs
            _filter = np.ones(len(self.ls)) > 0
            _filter[i] = False
            
            self.ls = self.ls[_filter]
            
            if self.ods is not None:
                self.ods = self.ods[_filter]
                
            if self.ids is not None:
                self.ids = self.ids[_filter]
                
            if self.wgs is not None:
                self.wgs = self.wgs[_filter]
            
            reduce += 1
            
    def add_section(self, section: dict, index: int = None) -> None:
        '''
        adds a section to a casing list. Missing values (id, od, wg) will be set to zero

        Parameters
        ----------
        index : int, optional
            position (0 indexed) at which to insert the section. If not set, section will be added as topmost (last) section
            
        section:dict
            fields: l, id, od, wg. l is mandatory, rest is optional. Unset fields will be added as 0.
    

        '''
        #check indx
        if index is not None and index > len(self.ls):
            raise ValueError('index out of bounds')
            
        if index is None:
            index = len(self.ls)
            
        self.ls = np.insert(self.ls, index, section['l'])
        
        self.ids = np.insert(self.ids, index, section.get('id') if 'id' in section else 0)
        self.ods = np.insert(self.ods, index, section.get('od') if 'od' in section else 0)
        self.wgs = np.insert(self.wgs, index, section.get('wg') if 'wg' in section else 0)
   
    def find_containing_section(self, z_ref) ->int:
        '''
        finds the section, in which a given depth lies.

        Parameters
        ----------
        z_ref : float
            reference depth [m MD].

        Returns
        -------
        section_index : int
            the section (zero indexed) that contains the reference depth.

        '''
        length = sum(self.ls) - z_ref
        #find section in which z_ref lies
        for i in np.arange(len(self.ls))+1:
            if self.ls[:i].sum() >= length:
                return i-1
                    

    def adjust_to_zref(self, z_ref: float, direction:str = 'up') -> None:
        '''
        adjusts the casing design to a reference depth. The new casing design will stop at this depth.
        

        Parameters
        ----------
        z_ref : float
            reference depth [m TVD].
        direction: string
            either 'up' or 'down'. The new casing design will start at the surface 'down' or at the bottom 'up'.

        '''
        #type check
        if direction not in ['up', 'down']:
            raise ValueError('direction must be either up or down.')
            
        #find section in which z_ref liesn(zero indexed, zero is lowest section)
        containing_section = self.find_containing_section(z_ref)
        
        if direction == 'up':
            length = sum(self.ls) - z_ref
            rest = self.ls[:containing_section + 1].sum() - length#reduce containing section by rest length
            self.ls[containing_section] -= rest
            self.remove_section(np.arange(containing_section + 1, len(self.ls))) #remove sections above
            
        if direction == 'down':
            rest = self.ls[containing_section:].sum() - z_ref #reduce containing section by rest length
            self.ls[containing_section] -= rest
            self.remove_section(np.arange(0, containing_section)) #remove sections above
            
        
        
    
    def compute_volume(z_ref: float) -> float:
        '''
        computes the volume of the entire casing design.

        Parameters
        ----------
        z_ref : float
            depth [m TVD] up onto which (starting from bottom of lowest section) volume should be computed.

        Returns
        -------
        float
            wellbore volume [m3].

        '''
        #TODO
        pass
        

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
        
        
                        
        
class Well():
    '''
    Contains information on a well and allows for computations of derived values
    '''
    
    def __init__(self, name, uwi = None, casing_design = None, survey = None, welltops = None, c_res = None, b_res = None, c_surf = None, T_res = None, p_res = None, p_regr = None, S = None, k = 3e-5, welltype = 'prod', z_ESP = None):
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
            if not isinstance(new_casing_design, CasingDesign()):
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

    def find_containing_section(self, z_ref):
        '''
        finds the section, in which a given depth lies. ATTENTION: different behaviour in injection and production wells.
        in production wells, the depth is interpreted as depth below surface.
        in injection wells, the depth is interpreted as depth above bottom of lowest section.

        Parameters
        ----------
        z_ref : float
            reference depth [m MD].

        Returns
        -------
        section_index : TYPE
            DESCRIPTION.

        '''
        #find section in which z_ref lies
        
        #production wells
        if self.welltype == 'prod':
            for i in np.arange(len(self.casing_design.ls)) + 1:
                if self.casing_design.ls[:i].sum() >= z_ref:
                    return i-1
                    
        #injection wells       
        elif self.welltype =='inj':
            for i in np.flip(np.arange(len(self.casing_design.ls))) + 1:
                if self.casing_design.ls[-i:].sum() >= z_ref:
                    return i-1
                
    def get_adjusted_cd_zref(self, z_ref):
        '''
        adjustes a casing design to only reach to z_ref. In production wells, it starts at surface, in injection wells at the bottom of the lowest casing.

        Parameters
        ----------
        z_res : float
            reference depth [m MD].

        Returns
        -------
        adj_casing_design : casing design
            adjusted cd.

        '''
        #adjust casing design for z_ref
        containing_section = self.find_containing_section(z_ref)
        
        adj_casing_design = self.casing_design
        
        if self.welltype == 'prod':
            z_ref_rest = adj_casing_design.ls[:containing_section - 1].sum()
            for i in np.arange(0, containing_section - 1):
                adj_casing_design.remove_section(i)
            
            adj_casing_design.ls[containing_section] = adj_casing_design.ls[containing_section] - z_ref_rest
            
        elif self.welltype == 'inj':
            z_ref_rest = adj_casing_design.ls[containing_section + 1:-1].sum()
            for i in np.arange(containing_section + 1, len(adj_casing_design.ls) -1):
                adj_casing_design.remove_section(i)
                
        
        return adj_casing_design
    
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
        adj_casing_design = self.get_adjusted_cd_zref(z_ref)

        if not isinstance(q, Iterable): #only one q value
            fl = res.hyd_fl_well_aux(self.casing_design.ids, self.casing_design.ls, k = self.k,  q = q, p =  p_res, T = T_wellbore, S = S)
        else:
            fl = [res.hyd_fl_well_aux(self.casing_design.ids, self.casing_design.ls, k = self.k,  q = qi, p =  p_res, T = T_wellbore, S = S) for qi in q]
            
        #TODO
        return fl
    
    #@np.vectorize
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
    
        
class Field():
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
        self.wells = wells
        
# =============================================================================
#Properties
# =============================================================================
    #array of all wells
    @property
    def wells(self):
        return self._wells
    
    @wells.setter
    def wells(self, new_wells):
        if new_wells is not None:
            #type check
            if not isinstance(new_wells, Iterable):
                raise ValueError('wells must be a list or an array of wells')
            else:             
                for welli in new_wells:
                    if not isinstance(welli, Well):
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
        if not isinstance(new_well, Well):
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
    
    def plot(plot:str):
        '''
        calls FieldVisualizer objects to plot field data.

        Parameters
        ----------
        plot : str
            plot type. Available:
                - 'ipr': plots IPR curves of all wells in the field


        '''
        if case == 'ipr':
            FieldIPRPlotter(self).plot()
        elif:
            raise ValueError(f"Plot type {plot} not available")

# =============================================================================
# Load data from somewhere and store it in the fields wells            
# =============================================================================
class DataLoader(ABC):
    '''
    abstractr base class for any class that loads data
    '''
    def __init__(self, field: Field) -> None:
        self.field = field
        
    @abstractmethod
    def load(self) -> Field:
        ...
        
class SurveyLoader(DataLoader):
    def load(self) -> Field:
        '''
        #TODO: implement such that to each well a corresponding survey is looked up, loaded andconverted to a survey object.

        Returns
        -------
        field
            DESCRIPTION.

        '''
        for well in self.wells:
            pass
        
        pass

# =============================================================================
# Visualize well data    
# =============================================================================
class WellVisualizer(ABC):
    '''
    Abstract base class for any well plotters
    '''
    def __init__(self, well: Well, savepath:str = None) -> None:
        self.well = well
        if savepath is not None: 
            self.dosave= True
            self.savepath = savepath
            
                
    @abstractmethod
    def plot(self):
        '''
        To be implemented in subclasses

        '''
        ...
        
class Well3dPathPlotter(WellVisualizer):
    '''
    Creates a 3D plot of the wellpath along with all welltops
    '''
    def plot(self):
        #TODO
        ...
# =============================================================================
# Visualize data from a field
# =============================================================================
class FieldVisualizer(ABC):
    '''
    Abstract base class for any class that visualizes a field
    '''
    def __init__(self, field: Field, savepath: str = None) -> None:
        self.field = field
        if savepath is not None: 
            self.dosave= True
            self.savepath = savepath
        
    @abstractmethod
    def plot(self):
        '''
        To be implemented in subclasses

        '''
        ...
        
class FieldIPRPlotter(FieldVisualizer):
    def plot(self):
        '''
        Plots the IPR curves of all wells in the field
        '''
        fig, ax = plt.subplots()
        for well in self.field.wells:
            # TODO: extract b and c values, compoute dP for q
            # Then plot the IPR on ax
            ...
        if self.dosave:
            fig.savefig(self.savepath)
        return fig
    
class FieldWellpathPlotter(FieldVisualizer):
    '''
    Plots the surface trajectories of all wells
    '''
    def plot(self):
        #TODO
        ...
        
class FieldPRegressionPlotter(FieldVisualizer):
    '''
    Plots reservoir pressure vs. depth of all wells in the field and adda a linear regression
    '''
    def plot(self):
        #TODO
        ...
    
     
                
                
                
                
                
                