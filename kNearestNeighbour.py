import math
import random

# we have 194 entries( sqrt(194) = 13.9)
# Since 14 is even we choose 13 as k
k = 193



f = open('spiralInputData.txt', 'r+')
lines = f.readlines()
f.close()

spiralPoints = []
spiralClassification = []

for line in lines:
    fixedLine = line.rstrip()
    vector = fixedLine.split(';')
    vector = list(map(float, vector))
    spiralValue = int(vector.pop(2))
    spiralClassification.append(spiralValue)
    spiralPoints.append(vector)
    


def getEuclidDist(v1, v2):
    dist = 0
    for i in range(len(v1)):
        dist += (pow((v2[i] - v1[i]),2))
    
    return math.sqrt(dist)

def determineDistanceToAllPoints(vec):
    distances = []
    for i in range(len(spiralPoints)):
        distances.append(getEuclidDist(vec, spiralPoints[i]))
    return distances

def getMininumDistanceIndicesFromList(distances):
    minIndices = []
    distanceCopy = distances.copy()
    # replace distance that is 0 and thus represents the chosen point
    minIndex = distanceCopy.index(min(distanceCopy))
    distanceCopy[minIndex] = max(distanceCopy)
    for i in range(k):
        minIndex = distanceCopy.index(min(distanceCopy))
        minIndices.append(minIndex)
        distanceCopy[minIndex] = max(distanceCopy)
    return minIndices

# Choose random point on spiral

indexOfPointToBeClassified = 32

distances = determineDistanceToAllPoints(spiralPoints[indexOfPointToBeClassified])

minIndices = getMininumDistanceIndicesFromList(distances)

# Check classification according to indices of points with minimal distance

blueSpiralCounter = 0
redSpiralCounter = 0

for i in range(len(minIndices)):
    if(spiralClassification[minIndices[i]] == 1):
        blueSpiralCounter +=1;
    else:
        redSpiralCounter += 1;
print(blueSpiralCounter)
print(redSpiralCounter)
if(blueSpiralCounter > redSpiralCounter):
    print("point is on blue spiral")
    print("Verification", spiralClassification[indexOfPointToBeClassified] == 1)
else:
    print("point is on red spiral")
    print(indexOfPointToBeClassified)
    print(spiralClassification[indexOfPointToBeClassified])
    print("Verification", spiralClassification[indexOfPointToBeClassified] == -1)

    
    