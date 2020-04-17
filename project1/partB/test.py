import numpy as np 
import crossover_function as cross

A = np.zeros((30, 14))
B = np.ones((30, 14))
C = np.array([A, B])

print(cross.crossover(C, 'Uniform'))