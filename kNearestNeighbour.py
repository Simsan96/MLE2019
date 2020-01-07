import math
import random
import pygame
import np
import time


# we have 194 entries( sqrt(194) = 13.9)
# Since 14 is even we choose 13 as k
k = 13



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

def evalVector(vec):
    minimumIndices = getMininumDistanceIndicesFromList(determineDistanceToAllPoints(vec))
    counter = 0
    for i in range(len(minimumIndices)):
        counter += spiralClassification[minimumIndices[i]]
    if counter > 0:
        return 1
    return -1

pygame.init()
screen = pygame.display.set_mode((400, 400))
screen.fill((255,255,255))

#x_array = np.arange(-1,1,0.01)
#y_array = np.arange(-1,1,0.01)



for i in range(len(spiralPoints)):
    classification = spiralClassification[i]
    # 1 represents red
    if( classification == 1):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((spiralPoints[i][0] +1)*200, (spiralPoints[i][1]+1)*200, 2, 2))
    #-1 represents blue
    else:
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((spiralPoints[i][0]+1)*200, (spiralPoints[i][1]+1)*200,2, 2))
    pygame.event.get()
    pygame.display.flip()


xCoordinate = -1
while xCoordinate <= 1:
    yCoordinate = -1
    while yCoordinate <= 1:
        vec = (xCoordinate, yCoordinate)
        value = evalVector(vec)
        if(value == 1):
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((xCoordinate +1)*200, (yCoordinate +1)*200, 2 ,2),1)
        else:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((xCoordinate +1)*200, (yCoordinate +1)*200, 2 ,2),1)
        pygame.event.get()
        pygame.display.flip()
        yCoordinate += 0.02
    xCoordinate += 0.02



time.sleep(10)
#pygame.quit()
