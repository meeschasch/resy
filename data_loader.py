#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:27:26 2022

@author: mischasch
"""
import pandas as pd
from abc import ABC, abstractmethod
from pathlib import Path
import numpy as np

#local application import
from resy.well import Well
from resy.field import Field
from resy.welltop import Welltop
from resy.casing_design import CasingDesign
from resy.hydraulic_characterisation import PTA, IPR
import resy.config

class DataLoader(ABC):
    '''
    abstractr base class for any class that loads data
    '''
    def __init__(self, field: Field) -> None:
        
        self.field = field
        
    @abstractmethod
    def load(self):
        ...
        
class HydraulikDBLoader(DataLoader):
    '''
    loads all data from the SWM Hydraulikdatenbank from the path provided with 
    the HydraulikDB keyword of the config.ini
    
    '''
    def __init__(self, field):
        super().__init__(field)
        
        #import config for location of HydraulikDB file
        from resy.config import config
        self.hdb_file = config.get('DataLoader', 'HydraulikDB')

    def load(self):       
        #file = r'I:\Projekte\SW-ER-PG\FG Reservoir\(05) Reservoir Engineering\Datensammlung\neu\HydraulikdatenbankSWM.xlsx'
        
        #%% Verlauf, ATTENTION: nrows needs to be adjusted
        #when new wells are present
        print('Loading 1a Verlauf...')
        d_verlauf = (pd.read_excel(self.hdb_file, sheet_name = '1a Verlauf',
                                  header = 0,
                                  nrows = 69))
        
        
        #create field and new well for each verlauf entry with UWI and well name
        
        
        for i, welli in d_verlauf.iterrows():
            well = Well(uwi = welli.UWI,
                             name = welli.Bohrung)
            
            #create TR welltop
            tr_welltop = Welltop(name = 'top reservoir',
                               z_MD = welli.Z1_mMD_TR,
                               z_TVD = welli.Z1_mTVD_TR,
                               x = welli.X_TR,
                               y = welli.Y_TR
                               )
            
            gok_welltop = Welltop(name = 'surface',
                                  z_MD = 0,
                                  z_NN = welli.GOK_mNN)
            
            if not np.isnan(welli.GOK_mNN):
                well.welltops['surface'] = gok_welltop
                
            if not all([np.isnan(tr_welltop.z_MD),
                    np.isnan(tr_welltop.z_TVD)]):    
                
                well.welltops['top reservoir'] = tr_welltop
            
            #create final depth welltop
            fd_welltop = Welltop(name = 'final depth',
                                      z_MD = welli.Z1_mMD_ET,
                                      z_TVD = welli.Z1_mTVD_ET,
                                      x = welli.X_ET,
                                      y = welli.Y_ET
                                      )
            if not all([np.isnan(fd_welltop.z_MD),
                    np.isnan(fd_welltop.z_TVD)]): 
                
                well.welltops['final depth'] = fd_welltop
            
            self.field.add_well(well)
            
        print('Done')
        
        #%%Temperatur
        print('Loading 2a Temperatur...')
        d_temperature = (pd.read_excel(self.hdb_file , sheet_name = '2a Temperatur',
                                  header = 2,
                                  nrows = 170))
        d_temperature = (d_temperature
                         .loc[d_temperature.chk1 == 1])
        
        for i, welli in d_temperature.iterrows():
            self.field[welli.UWI].T_res = welli.TRESmax
        print('Done')
            
            
        # %% Potential
        print('Loading 3a Potential...')
        d_potential = pd.read_excel(self.hdb_file , sheet_name = '3a Potential',
                                    header = 2,
                                    nrows = 125)
        
        d_potential = (d_potential
                       .loc[d_potential.chk == 1])
        
        for i, welli in d_potential.iterrows():
            self.field[welli.UWI].p_res = welli.PRES_TR
        print('Done')
        # %% Mineralisation
        print('Loading 8 Mineralisation...')
        d_mineralisation = pd.read_excel(self.hdb_file , sheet_name = '8 Mineralisation',
                                    header = 0,
                                    nrows = 54,
                                    na_values = ' ')
               
        for i, welli in d_mineralisation.iterrows():
            self.field[welli.UWI].S = welli.Mineralisation
        print('Done')
            
        #%% b- und c-Koeffizienten
        print('Loading 5a Produktivität...')
        d_ipr = pd.read_excel(self.hdb_file , sheet_name = '5a Produktivität',
                                    header = 2,
                                    nrows = 37,
                                    na_values = ' ')
        d_ipr = (d_ipr
                 .rename(columns = {'C [-]': 'c',
                                    'B [-]': 'b',
                                    'Bohrung': 'Name',
                                    d_ipr.columns[2]: 'UWI',
                                    d_ipr.columns[7]: 'certain_end',
                                    d_ipr.columns[9]: 'uncertain_end',
                                    d_ipr.columns[10]: 'description',
                                    d_ipr.columns[11]: 'origin'})
                 .query('~UWI.isnull()', engine = 'python'))
        
        for i, welli in d_ipr.iterrows():
            ipr = IPR()
            ipr.b = welli.b
            ipr.c = welli.c
            ipr.range_certain = (welli.Sicher, welli.certain_end)
            ipr.range_uncertain = (welli.Unsicher, welli.uncertain_end)
            ipr.description = welli.description
            ipr.origin = welli.origin
            
            if isinstance(welli.description, str): #if not: nan
                if 'BDS' in welli.description:
                    #neglect distance from sensor to top reservoir
                    try:
                        ipr.measurement_depth = (self.field[welli.UWI]
                                             .welltops['top reservoir'].z_MD)
                    except:
                        raise ValueError('no welltop found for top reservoir in well: '
                                         + welli.UWI)
                elif 'TKP' in welli.description or 'TKP':
                    #Attention: no esp intake depth is known form the data. 
                    # 700 m is just assumed.
                    ipr.measurement_depth = 700
                else:
                    ipr.measurement_depth = 0
                
            self.field[welli.UWI].ipr = ipr
            
        print('Done')
        
        #%% PTA
        
        print('Loading PTA...')
        d_pta = pd.read_excel(self.hdb_file , sheet_name = '4d Hydraulik PTA',
                                    header = 2,
                                    nrows = 78,
                                    na_values = ' ')
        d_pta = (d_pta.loc[d_pta.chk == 1])
               
        for i, welli in d_pta.iterrows():
            pta = PTA(perm = welli['Permeabilität'],
                                   poro = welli['Porosität'],
                                   aquifer_thickness = welli['Mächtigkeit Auswertung'],
                                   transmissibility = welli['Transmissibilität'],
                                   transmissivity = welli['Transmissivität'],
                                   porosity_thickness = welli['Porosität x Mächtigkeit'],
                                   storativity = welli['Speicherkoeffizient'],
                                   m_d_comp = welli['M=D'],
                                   skin = welli['Skin/Skin0'])
            
            self.field[welli['chk Bohrung']].pta = pta

        print('Done')
            
                
class SurveyLoader(DataLoader):
    def load(self):
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
    
class CasingDesignLoader(HydraulikDBLoader):
    '''
    imnport casing design. Inherits from HydraulikDBLoader because the casing
    design is stored in the same excel file
    '''
    def load(self):
        '''
        #TODO
        Returns
        -------
        field
            DESCRIPTION.

        '''
        #file = r'I:\Projekte\SW-ER-PG\FG Reservoir\(05) Reservoir Engineering\Datensammlung\neu\HydraulikdatenbankSWM.xlsx'
        
        print('Loading 14 Casing Design...')
        d_cd = (pd.read_excel(self.hdb_file, sheet_name = '14 Casing Design',
                                  header = 1))
        
        d_cd = (d_cd.loc[~pd.isna(d_cd.OD)])
        
        for i, cd in d_cd.groupby('UWI'):
            cd = cd.sort_values(by = 'Teufe bis', ascending = False)
            new_cd = CasingDesign(ls = cd['Teufe von'] - cd['Teufe bis'],
                                  ids = cd.ID,
                                  ods = cd.OD,
                                  z_from = cd['Teufe von'],
                                  z_to = cd['Teufe bis'],
                                  wgs = cd['Wandstärke'],
                                  descr = cd.Sektion)
            
            self.field[i].casing_design = new_cd