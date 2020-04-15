import numpy as np


class Employee:
    hoursWorked = 0
    shifts = np.zeros(14)

    def __init__(self, hoursWorked, shifts):
        self.shifts = shifts

    def hoursWorked(self):
        return 1
