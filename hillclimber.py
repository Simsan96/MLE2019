import numpy as np
import random
fitness = 0
distance = 0
rows, cols = (100,100)
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
    valuesToChange = random.sample(range(10),2)
    tmp = route[valuesToChange[0]]
    newRoute[valuesToChange[0]] = route[valuesToChange[1]]
    newRoute[valuesToChange[1]] = tmp
    if 0 in valuesToChange:
        newRoute[cols-1] = newRoute[0]
    elif cols - 1 in valuesToChange:
        newRoute[0] = newRoute[cols - 1]
    return newRoute
distances = setUpMatrix()
route = random.sample(range(cols),cols)
route[cols-1] = route[0]
distance = getDistanceFromRoute(route, distances)
fitness = distance * (-1)

for i in range(10000000):
    newRoute = changeRoute(route)
    newDistance = getDistanceFromRoute(newRoute, distances)
    if(newDistance < distance):
        route = newRoute
        distance = newDistance
        fitness = distance * (-1)
print(route)
print('newDistance + %s' %distance)
