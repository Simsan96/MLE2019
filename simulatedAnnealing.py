import random
import math
def simulatedAnnealing(newFitness, oldFitness, temp):
    if(newFitness > oldFitness):
        return True
    elif(random.random < math.exp((newFitness - oldFitness)/temp)):
        return True
    else:
        return False
