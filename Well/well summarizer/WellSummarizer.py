#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:15:28 2022

@author: mischasch
"""

class WellSummarizer(ABC):
    '''
    ABC for well summarizer classes
    '''
    def __init__(self, well):
        self.well = well
    @abstractmethod
    def summarize(self):
        '''
        to be implemented by all subclasses

        '''
        ...