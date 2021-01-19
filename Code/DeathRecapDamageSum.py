# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:19:32 2018

@author: Andy
"""
# Sums damage dealt
import numpy as np
import pandas as pd
def DamageSum(df, prev, condition):
    
    
    
    
    #Declaring cumulative value
    cumulative = 0
    #Making empty list to fill with values
    cumulist = []
    
    #Creates data for cumulative damage
    for i in range(len(df)):
        #Range of data in consideration
        temp = df[0:i + 1]
        #Sum od data from range that fills Type condition
        cumulative = sum(temp.Total[condition])
        #Append to list
        cumulist.append(cumulative)
    #Make sure I know what I'm doing
    
    #Return list
    return cumulist
        
    
    
