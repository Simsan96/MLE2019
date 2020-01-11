import random
import math
def simulatedAnnealing(newFitness, oldFitness, temp):
    print("new Fitness ",newFitness)
    print(oldFitness)
    if(newFitness > oldFitness):
        return True
    else:
        print(math.exp((newFitness - oldFitness)/temp))
        if(random.random < math.exp((newFitness - oldFitness)/temp)):
            return True
        else:
            return False
