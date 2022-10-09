#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:24:01 2022

@author: mischasch
"""

class PlotlyFieldIPRPlotter(FieldVisualizer):
    '''
    Plots the IPR curves of all wells in the field with Plotly
    '''
    def visualize(self, q: tuple = (0,150)):
        q = np.arange(*q)
        dp = pd.DataFrame(index = q, columns = self.field.uwis)
        for well in dp.columns:
            dp[well] = self.field[well].b_res * q + self.field[well].c_res * q**2
                          
        dp['q']= q
        dp = dp.melt(id_vars = 'q', var_name = 'well', value_name = 'dP')
 
        fig = px.line(dp, x = 'q', y = 'dP', color = 'well')
        fig.show()