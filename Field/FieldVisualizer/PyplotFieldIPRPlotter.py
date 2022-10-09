#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:24:29 2022

@author: mischasch
"""

class PyplotFieldIPRPlotter(FieldVisualizer):
    # def __init__(self, field, savepath):
    #     super().__init__(self, field, savepath)
        
    def visualize(self, q: tuple = (0,150)):
        '''
        Plots the IPR curves of all wells in the field with Pyplot
        '''
        q = np.arange(*q)
        fig, ax = plt.subplots()
        for well in self.field.wells:
            ax.plot(q, well.b_res * q + well.c_res * q**2, label = well.uwi)
        
        ax.legend()
        ax.set_xlabel('q [l/s]')
        ax.set_ylabel('dP [bara]')
        
        return fig