import numpy as np
from itertools import repeat
import random

np.random.seed(1996)

bitLength = 100
populationSize = 100
crossOverRate = 0.25

mutationRate = 0.25
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


def graycode(bitString):
    graycode = []
    graycode.append(bitString[0])
    for i in range(len(bitString) - 1):
        graycode.append(bitString[i] ^ bitString[i + 1])

    return graycode


def reverseGraycode(graycode):
    newBinary = []
    newBinary.append(graycode[0])
    for i in range(len(graycode) - 1):
        newBinary.append(newBinary[i] ^ graycode[i + 1])

    return newBinary


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


def mutatePopulation(population):
    popCopy = population
    mutationSize = int(mutationRate * populationSize)
    memberIndices = random.sample(range(1, populationSize), mutationSize)
    while (fitness.index(maxFitness) in memberIndices):
        memberIndices = random.sample(range(1, populationSize), mutationSize)

    for i in range(mutationSize):
        member = popCopy[memberIndices[i]]
        memberGray = graycode(member)
        indexOfBitToChange = np.random.randint(bitLength)
        memberGray[indexOfBitToChange] = 1 if memberGray[indexOfBitToChange] == 0 else 0;
        popCopy[memberIndices[i]] = reverseGraycode(memberGray)

    return popCopy


optimum = np.random.randint(2, size=bitLength)
population = np.random.randint(2, size=(populationSize, bitLength))

while (maxFitness < bitLength):
    fitness = list(map(lambda b: calcFitness(optimum, b), population))

    maxFitness = max(fitness)

    selectionSize = int(round((1 - crossOverRate) * populationSize))

    if(selectionSize % 2 != 0):
        selectionSize = selectionSize -1

    newPopulation = []
    newPopulation.append(population[fitness.index(maxFitness)])
    for i in range(selectionSize - 1):
        currentIndex = selectHypothesis()
        newPopulation.append(population[currentIndex])
    crossOverSize = populationSize - selectionSize

    pairs = []

    for i in range(int(crossOverSize)):
        currentIndex = selectHypothesis()
        pairs.append(population[currentIndex])

    successors = createSuccessors(pairs)

    newPopulation.extend(successors)

    population = mutatePopulation(newPopulation)

    maxFitness = max(fitness)

    print(maxFitness)

fitness = list(map(lambda b: calcFitness(optimum, b), population))
maxFitness = max(fitness)

print(population[fitness.index(maxFitness)])

print(optimum)
