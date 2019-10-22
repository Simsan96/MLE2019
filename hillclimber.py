import numpy as np
import random
import simulatedAnnealing
rows, cols = (101,101)
def setUpMatrix():
    distances = np.random.randint(1, 10, size = (rows,cols))
    for i in range(cols):
        distances[[i],:] = distances[:,[i]].transpose()
    np.fill_diagonal(distances,0)
    return distances
def getDistanceFromRoute(route, distances):
    disSum = 0
    for i in range(rows-1):
        disSum += distances[route[i]][route[i+1]]
    return disSum
def changeRoute(route):
    newRoute = route
    valuesToChange = random.sample(range(cols),2)
    tmp = route[valuesToChange[0]]
    newRoute[valuesToChange[0]] = route[valuesToChange[1]]
    newRoute[valuesToChange[1]] = tmp
    if 0 in valuesToChange:
        newRoute[cols-1] = newRoute[0]
    elif cols - 1 in valuesToChange:
        newRoute[0] = newRoute[cols - 1]
    return newRoute

def classicHillClimber():
    distances = setUpMatrix()
    route = random.sample(range(cols),cols)
    route[cols-1] = route[0]
    distance = getDistanceFromRoute(route, distances)
    fitness = distance * (-1)
    for i in range(1000000):
        newRoute = changeRoute(route)
        newDistance = getDistanceFromRoute(newRoute, distances)
        newFitness = newDistance * (-1)
        if(newFitness > fitness):
            route = newRoute
            distance = newDistance
            print(newDistance)
            fitness = distance * (-1)
    print(route)
    print('newDistance + %s' %distance)


def hillClimberWithSimulatedAnnealing(temp, epsilon):
    temperature = temp;
    distances = setUpMatrix()
    route = random.sample(range(cols),cols)
    route[cols-1] = route[0]
    distance = getDistanceFromRoute(route, distances)
    fitness = distance * (-1)
    while(temperature > epsilon):
        newRoute = changeRoute(route)
        newDistance = getDistanceFromRoute(newRoute, distances)
        newFitness = newDistance * (-1)
        if(simulatedAnnealing.simulatedAnnealing(newFitness, fitness, temperature)):
            route = newRoute
            distance = newDistance
            print(newDistance)
            fitness = distance * (-1)
        temperature -= epsilon
        # Otherwise route remains the same
    print(route)
    print('newDistance Annealing + %s' %distance)

np.random.seed(541996)
hillClimberWithSimulatedAnnealing(1000, 0.001);
# classicHillClimber();
