import numpy as np 
import constant as c

def geneticAlgorithm():

    initPop = generateRandomPopulation()
    if checkHardConstraints(initPop):
        print("Not legal.")

    penaltyFunction(initPop)
    
def generateRandomPopulation():
    
    population = np.random.randint(0, 4, size=(30,14))
    print(population)

    return population  
