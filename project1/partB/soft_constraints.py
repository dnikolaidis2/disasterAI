import numpy as np 

def hoursWorked(employee):
    return np.count_nonzero(employee == 1)*c.M_HOURS +\
           np.count_nonzero(employee == 2)*c.E_HOURS +\
           np.count_nonzero(employee == 3)*c.N_HOURS


def straightDaysWorked(employee):
    straightDays = 0
    for day in employee:
        straightDays+=1

        if day == c.DAY_OFF:
            straightDays = 0

        if straightDays > c.MAX_WORK_DAYS:
            return 1
    return 0

def maxNightShifts(employee):
    nightShifts = 0
    timesViolated = 0
    for day in employee: 
        if day == c.NIGHT:
            nightShifts+=1
        else:
            nightShifts = 0
        if nightShifts > c.MAX_NIGHT_SHIFTS:    
            timesViolated+=1
            nightShifts = 0
    return timesViolated 

def morningAfterNight(employee):
    return 1 