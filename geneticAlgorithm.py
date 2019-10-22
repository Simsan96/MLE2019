import numpy as np
from itertools import repeat
import random

np.random.seed(1996)

bitLength = 8
populationSize = 64
crossOverRate = 0.5

mutationrate = 0.001
fitness = []
population = []


def selectHypothesis():
    randNum = random.random()
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
    return (float(currentFitness) / sum(fitnessList))

def compare(a, b) :
    return 1 if a == b else 0

def calcFitness(a, b):
    dist = 0
    for i in range(bitLength):
        dist += compare(a[i],b[i])
    fitness = bitLength - dist
    return fitness

def createSuccessors(pairs) :
    successors = []
    crossOverLength = int(bitLength * crossOverRate)

    for i in range(0,len(pairs)/2),2:
        firstPartFirstSuccessor = pairs[i][0:crossOverLength]
        secondPartFirstSuccessor = pairs[i+1][crossOverLength:bitLength]
        firstPartSecondSuccessor = pairs[i+1][0:crossOverLength]
        secondPartSecondSuccessor = pairs[i][crossOverLength:bitLength]
        firstNewSuccessor = np.append(firstPartFirstSuccessor, secondPartFirstSuccessor)
        secondNewSuccesor = np.append(firstPartSecondSuccessor, secondPartSecondSuccessor)
        successors.append(firstNewSuccessor)
        successors.append(secondNewSuccesor)

    print(successors)


optimum = np.random.randint(2, size = bitLength)
population = np.random.randint(2 , size = (populationSize, bitLength))
while (np.isin(population.all(), optimum)) :
    optimum = np.random.randint(2, size = bitLength)

fitness = list(map(lambda b:calcFitness(optimum, b), population))

selectionSize = int(round((1 - crossOverRate) * populationSize))
print(selectionSize)

newPopulation = []
for i in range(selectionSize):
    currentIndex = selectHypothesis()
    newPopulation.append(population[currentIndex])
print(newPopulation[1])

crossoverSize = round((crossOverRate*populationSize))
print("crossover")
print(crossoverSize)
pairs = []

for i in range(int(crossoverSize)):
    currentIndex = selectHypothesis()
    pairs.append(population[currentIndex])

createSuccessors(pairs)