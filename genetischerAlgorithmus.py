import numpy as np
from itertools import repeat
import random

np.random.seed(1996)

bitLength = 8
populationSize = 64
crossOverRate = 0.3

mutationrate = 0.001
fitness = []
population = []


def selectHypothesis():
    randNum = random.random
    sum = 0.0
    index = np.random.randint(populationSize)
    index += 1
    index = index % populationSize
    sum += calcProbability(fitness[index], fitness)

    while(sum < randNum) :
        index += 1
        index = index % populationSize
        sum += calcProbability(fitness[index], fitness)

    return index

def calcProbability(currentFitness, fitnessList):
    print(currentFitness)
    return currentFitness / sum(fitnessList)

def compare(a, b) :
    return 1 if a == b else 0

def calcFitness(a, b):
    dist = 0
    for i in range(bitLength):
        dist += compare(a[i],b[i])
    fitness = bitLength - dist
    return fitness;


optimum = np.random.randint(2, size = bitLength);
population = np.random.randint(2 , size = (populationSize, bitLength))
while (np.isin(population.all(), optimum)) :
    optimum = np.random.randint(2, size = bitLength)

fitness = list(map( lambda b:calcFitness(optimum, b), population))

selectionSize = int(round((1 - crossOverRate) * populationSize))
print(selectionSize)

newPopulation = []
for i in range(selectionSize):
    currentIndex = selectHypothesis()
    np.append(newPopulation, population[currentIndex])

priont(newPopulation)
