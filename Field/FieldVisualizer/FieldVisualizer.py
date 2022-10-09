#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:25:33 2022

@author: mischasch
"""

class FieldVisualizer(ABC):
    '''
    Abstract base class for any class that visualizes a field
    '''
    def __init__(self, field: Field, savepath: str = None) -> None:
        self.field = field
        if savepath is not None: 
            self.dosave= True
            self.savepath = savepath
        else:
            self.dosave = False
            
        #set matplotlib style
        plt.style.use('seaborn')
        io.renderers.default='browser'
    
    def plot(self):
        '''
        first, runs the visualize method in the sublasses. Then, saves the figure if required.
        '''
        fig = self.visualize()
        
        if self.dosave:
            if not Path(self.savepath).exists():
                os.mkdir(self.savepath)
            
            try:
                fig.savefig(Path(self.savepath) / 'ipr.png')
            except:
                raise Exception('File could not be saved')
        
    @abstractmethod
    def visualize(self):
        '''
        To be implemented in subclasses. Must return a pyplot figure.

        '''
        ...