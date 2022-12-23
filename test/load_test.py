# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:37:40 2022

@author: SCHWEINGRUBER.MISC
"""
import sys
sys.path.append(r'C:\Users\Schweingruber.Misc\Documents\GitHub')
import pandas as pd
import resy
from resy.casing_design import CasingDesign

file = r'I:\Projekte\SW-ER-PG\FG Reservoir\(05) Reservoir Engineering\Datensammlung\neu\HydraulikdatenbankSWM.xlsx'


        
print('Loading 14 Casing Design...')
d_cd = (pd.read_excel(file, sheet_name = '14 Casing Design',
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
    print(new_cd)