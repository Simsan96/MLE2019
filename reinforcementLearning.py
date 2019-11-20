# -*- coding: utf-8 -*-
import math
"""
Created on Wed Nov 20 20:05:37 2019

@author: Simon
"""

alpha = 0.01

action = 2.0 * np.random.random() - 1.0
qTable = [[]]

def getState(xCoordinates, sortedXCoordinates):
    state = xCoordinates[0]
    for(i in range(1,len(xCoordinates))):
        s = s*max[i] + x[i]
        
    return s


def getGamma(stepsToReward):
    return math.exp(-stepsToReward)

def getReward(reward):
    return reward

for(i in range(2)):
    qTable[0].append(0.01)
    qTable[1].append(0.01)
    
