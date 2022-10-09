#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:27:26 2022

@author: mischasch
"""

class DataLoader(ABC):
    '''
    abstractr base class for any class that loads data
    '''
    def __init__(self, field: Field) -> None:
        self.field = field
        
    @abstractmethod
    def load(self):
        ...