import numpy as np
import random
import constant as c 

def crossover(parent, method):
    #Each gene is selected from either parent with equal probability  
    children = np.empty([2, c.EMPLOYEE_COUNT, c.DAY_COUNT])
    if method == 'Uniform':
        for i in range(len(parent[0])):
            for j in range(len(parent[0][i])):
                indx1 = random.randint(0,1)
                indx2 = 1
                if indx1:
                    indx2 = 0
                
                children[0][i][j] = parent[indx1][i][j] 
                children[1][i][j] = parent[indx2][i][j]
             
    return children
