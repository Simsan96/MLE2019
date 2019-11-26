# -*- coding: utf-8 -*-
import math
import random
"""
Created on Wed Nov 20 20:05:37 2019

@author: Simon
"""



class ReinforcementLearning:

    def __init__(self,xCoordinates):
        # max xBall, max yBall, maxRacket, maxxV, maxxY
        random.seed(1996)
        self.maxForCoordinates = (12,12,10,2,2)
        self.numberOfStates = 12 * 12 * 10 * 2 * 2
        self.epsilon = 0.2
        self.qTable = [[]]
        self.stateT = self.getState(xCoordinates)
        self.alpha = 0.01
        for i in range(self.numberOfStates):
           newList = []
           newList.append(random.uniform(0, 0.3))
           newList.append(random.uniform(0, 0.3))
           newList.append(random.uniform(0, 0.3))
           self.qTable.append(newList)

    def getState(self, xCoordinates):
        state = xCoordinates[0]
        for i in range(1, len(xCoordinates)):
            state = state*self.maxForCoordinates[i] + xCoordinates[i]
            print(state)
        return state


    def getGamma(self, stepsToReward):
        return math.exp(-stepsToReward)

    def getReward(self,reward):
        return reward

    def getAction(self):
        if self.epsilon > random.uniform(0.0, 1.0):
            return  2.0 * random.random() - 1.0
        if self.qTable[self.stateT].index(max(self.qTable[self.stateT])) == 0:
            return 0
        elif self.qTable[self.stateT].index(max(self.qTable[self.stateT])) == 1:
            return 0.5
        return -0.5


    def updateQ(self, nextState, reward):
         print("nextState", nextState)
         for i in range(len(self.qTable[self.stateT])):
            self.qTable[self.stateT][i] = self.qTable[self.stateT][i] + self.alpha * (reward + (self.getGamma(1) * max(self.qTable[nextState])) - self.qTable[self.stateT][i])
         self.stateT = nextState
