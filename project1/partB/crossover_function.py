import numpy as np
import random
import constant as c 


def crossover(population, method, pcross):
    # Considering the last chromosome as elite, do we crossover it?
    crossPopulation = np.empty(population.shape)
    for i in range(0, (len(population)-2), 2):
        crossPass = np.random.choice((1, 0), p=[pcross, 1-pcross])
        if crossPass:
            children = crossover_methods(np.array([population[i], population[i+1]]), method=method)
            crossPopulation[i] = children[0]
            crossPopulation[i+1] = children[1]
        else: 
            crossPopulation[i] = population[i]
            crossPopulation[i+1] = population[i+1]
    return crossPopulation


def crossover_methods(parent, method):
    # Each gene is selected from either parent with equal probability
    children = np.empty([2, c.EMPLOYEE_COUNT, c.DAY_COUNT])
    if method == 'Uniform':
        for i in range(len(parent[0])):
            for j in range(len(parent[0][i])):
                indx1 = random.randint(0, 1)
                indx2 = 1
                if indx1:
                    indx2 = 0
                
                children[0][i][j] = parent[indx1][i][j] 
                children[1][i][j] = parent[indx2][i][j]
    
    if method == 'TwoPoint':
        point1 = np.random.randint(1, len(parent[0]))
        point2 = np.random.randint(point1, len(parent[0]))
        children[0] = np.vstack((parent[0][0:point1], parent[1][point1:point2], parent[0][point2:]))
        children[1] = np.vstack((parent[1][0:point1], parent[0][point1:point2], parent[1][point2:]))
    return children
