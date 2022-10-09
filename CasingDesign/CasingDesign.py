#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:32:38 2022

@author: mischasch
"""

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
            
        
        return self
    
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