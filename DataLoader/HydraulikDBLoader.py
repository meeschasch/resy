#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:28:23 2022

@author: mischasch
"""

class HydraulikDBLoader(DataLoader):
    '''
    loads all data from the SWM Hydraulikdatenbank
    '''
    def load(self):
        file = 'testdata.csv'
        d = pd.read_csv(file, index_col= False)
        
        for i, di in d.iterrows():
            if di.UWI in self.field.uwis:
                self.field[d.UWI].b_res = di.b
                self.field[d.UWI].c_res = di.c
            else:
                self.field.add_well(Well(uwi = di.UWI, c_res = di.c, b_res = di.c))
                