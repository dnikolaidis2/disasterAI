import numpy as np
import constant as c


def hoursWorked(employee):
    return np.count_nonzero(employee == 1)*c.M_HOURS +\
           np.count_nonzero(employee == 2)*c.E_HOURS +\
           np.count_nonzero(employee == 3)*c.N_HOURS


def straightDaysWorked(employee):
    straightDays = 0
    for day in employee:
        straightDays += 1

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
            nightShifts += 1
        else:
            nightShifts = 0
        if nightShifts > c.MAX_NIGHT_SHIFTS:    
            timesViolated += 1
            nightShifts = 0
    return timesViolated 


def morningAfterNight(employee):
    timesViolated = 0
    prevDay = employee[0]
    for day in employee[1:]:
        if prevDay == c.NIGHT and day == c.MORNING:
            timesViolated += 1
        prevDay = day 
    return timesViolated


def morningAfterEvening(employee):
    timesViolated = 0
    prevDay = employee[0]
    for day in employee[1:]:
        if prevDay == c.EVENING and day == c.MORNING:
            timesViolated += 1
        prevDay = day 
    return timesViolated 


def eveningAfterNight(employee):
    timesViolated = 0
    prevDay = employee[0]
    for day in employee[1:]:
        if prevDay == c.NIGHT and day == c.EVENING:
            timesViolated += 1
        prevDay = day 
    return timesViolated 


def twoDaysOffAfterNightShift(employee):
    for i in range(len(employee[:-6])):
        if np.array_equal(employee[i:i+7], c.PREFERRED_SCHEDULE):
            return 1
    return 0


def twoDaysOffAfterSevenDays(employee):
    daysOfWork = 0
    for i in range(len(employee[:-2])):
        if employee[i] != c.DAY_OFF:
            daysOfWork+=1
        
        if daysOfWork == c.MAX_WORK_DAYS:
            if employee[i+1] == c.DAY_OFF and employee[i+2] == c.DAY_OFF:
                return 1
    return 0


def workDayoffWork(employee):
    timesViolated = 0
    for i in range(len(employee[:-2])):
        if employee[i] != c.DAY_OFF and employee[i+1] == c.DAY_OFF and employee[i+2] != c.DAY_OFF: 
            timesViolated += 1
    return timesViolated


def dayOffWorkDayoff(employee):
    timesViolated = 0
    for i in range(len(employee[:-2])):
        if employee[i] == c.DAY_OFF and employee[i+1] != c.DAY_OFF and employee[i+2] == c.DAY_OFF: 
            timesViolated += 1
    return timesViolated


def workInWeekends(employee):
    if employee[5] != c.DAY_OFF or employee[6] != c.DAY_OFF:
        if employee[12] != c.DAY_OFF or employee[13] != c.DAY_OFF:
            return 1
    else:
        return 0 

'''
def workDayoffWork(employee):
    if True in np.all(rolling_window(employee, 3) == [1, 0, 1], axis=1):
        return 1
    return 0

def dayOffWorkDayoff(employee):
    if True in np.all(rolling_window(employee, 3) == [0, 1, 0], axis=1):
        return 1
    return 0

def workInWeekends(employee):
    if employee[5] != c.DAY_OFF or employee[6] != c.DAY_OFF:
        if employee[12] != c.DAY_OFF or employee[13] != c.DAY_OFF:
            return 1
    else:
        return 0



def rolling_window(a, size):
    shape = a.shape[:-1] + (a.shape[-1] - size + 1, size)
    strides = a.strides + (a. strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
    
'''