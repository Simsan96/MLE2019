import random
import math
import numpy as np

np.random.seed(1996)

bitLength = 100
populationSize = 100
crossOverRate = 0.5

mutationRate = 0.05
fitness = []
population = []
newPopulation = []
optimum = []

maxFitness = 0


def selectHypothesis():
    randNum = random.random()
    sum = 0.0
    index = np.random.randint(populationSize)
    index += 1
    index = index % populationSize
    sum += calcProbability(fitness[index], fitness)

    while (sum < randNum):
        index += 1
        index = index % populationSize
        sum += calcProbability(fitness[index], fitness)

    return index


def calcProbability(currentFitness, fitnessList):
    return (float(currentFitness) / sum(fitnessList))


def compare(a, b):
    return 0 if a == b else 1


def calcFitness(a, b):
    dist = 0
    for i in range(bitLength):
        dist += compare(a[i], b[i])
    fitness = bitLength - dist

    return fitness

def createSuccessors(pairs):
    successors = []
    crossOverLength = int(bitLength * crossOverRate)


    for i in range(0, len(pairs), 2):
        firstPartFirstSuccessor = (pairs[i])[0:crossOverLength]
        secondPartFirstSuccessor = pairs[i + 1][crossOverLength:bitLength]
        firstPartSecondSuccessor = pairs[i + 1][0:crossOverLength]
        secondPartSecondSuccessor = pairs[i][crossOverLength:bitLength]
        firstNewSuccessor = np.append(firstPartFirstSuccessor, secondPartFirstSuccessor)
        secondNewSuccesor = np.append(firstPartSecondSuccessor, secondPartSecondSuccessor)
        successors.append(firstNewSuccessor)
        successors.append(secondNewSuccesor)

    return successors

def createFitnessList(optimum, population):
    fitnessList = []
    for i in range(0, len(population)):
        fitnessList.append(calcFitness(optimum, population[i]))


    return fitnessList

def mutatePopulation(population):
    popCopy = population
    fitness = createFitnessList(optimum, popCopy)
    maxFitness = max(fitness)
    mutationSize = math.ceil(mutationRate * populationSize)
    memberIndices = random.sample(range(0, populationSize), mutationSize)

    for i in range(mutationSize):
        if(memberIndices[i] != fitness.index(maxFitness)):
            member = popCopy[memberIndices[i]]
            indexOfBitToChange = np.random.randint(bitLength)
            member[indexOfBitToChange] = 1 if member[indexOfBitToChange] == 0 else 0;
            popCopy[memberIndices[i]] = member
            fitness = createFitnessList(optimum, popCopy)
            maxFitness = max(fitness)
            print(maxFitness)

    return popCopy


optimum = np.random.randint(2, size=bitLength)
population = np.random.randint(2, size=(populationSize, bitLength))
selectionSize = int(round((1 - crossOverRate) * populationSize))
if(selectionSize % 2 != 0):
    selectionSize = selectionSize -1

crossOverSize = populationSize - selectionSize


iterations = 0
while (maxFitness < bitLength):
    iterations = iterations +1
    fitness = createFitnessList(optimum, population)

    maxFitness = max(fitness)

    newPopulation = []
    newPopulation.append(population[fitness.index(maxFitness)])

    for i in range(selectionSize - 1):
        currentIndex = selectHypothesis()
        newPopulation.append(population[currentIndex])


    pairs = []

    for i in range(int(crossOverSize)):
        currentIndex = selectHypothesis()
        pairs.append(population[currentIndex])

    successors = createSuccessors(pairs)

    newPopulation.extend(successors)

    population = mutatePopulation(newPopulation)

    fitness = createFitnessList(optimum, population)

    maxFitness = max(fitness)


fitness = createFitnessList(optimum, population)
maxFitness = max(fitness)

print(population[fitness.index(maxFitness)])

print(optimum)

print(iterations)
