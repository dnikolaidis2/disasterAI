import numpy as np
import constants as c
from util import uniqueCounts, minMaxNormalize


def workforceSatisfied(chromosome, expected_elems):
    # A bit complicated but for every day in a chromosome calculate the counts off all unique elements
    # with unique(). These counts are the numbers of employees working each shift on a given day.
    # Select only shifts that are greater then 0. This table has the coverage of every shift per day.
    workforce_coverage = np.apply_along_axis(uniqueCounts, 0, chromosome, 0, expected_elems)

    # For every element in workforce_coverage check that its greater or equal
    # to the minimum requirements given by REQUIRED_COVERAGE.
    return np.all(workforce_coverage == c.REQUIRED_COVERAGE)


def fitnessFunction(population, penalty=None):
    if penalty is None:
        penalty = penaltyFunction(population)

    penalty_norm = minMaxNormalize(penalty, c.MIN_PENALTY, c.MAX_PENALTY)

    np.testing.assert_array_less(-penalty_norm, 0, f"New min found! {penalty[penalty.argmin()]}")
    np.testing.assert_array_less(penalty_norm, 1.0000000000000001, f"New max found! {penalty[penalty.argmax()]}")

    return 1 - penalty_norm


def checkHardConstraints(population):
    pop = population.shape[0]
    ret = np.zeros(pop, dtype=bool)

    for i in range(pop):
        ret[i] = workforceSatisfied(population[i], c.EXPECTED_ELEMENTS)

    return ret


def penaltyFunction(population):
    pop = population.shape[0]
    ret = np.zeros(pop)

    for i in range(pop):
        # Give a value to a population based on soft constraints
        penalty = 0

        for employee in population[i]:

            # MAX 70 hours of work (per week or per 14 days)
            if hoursWorked(employee) > c.MAX_WORK_HOURS:
                penalty += 1000

            # MAX 7 continuous days of work
            if straightDaysWorked(employee):
                penalty += 1000

            # MAX 4 NIGHT SHIFTS
            val = maxNightShifts(employee)
            if val:
                # Multiply the penalty if constraint is broken more than once in schedule
                penalty += 1000*val

            # Morning Shift after Night Shift
            val = morningAfterNight(employee)
            if val:
                penalty += 1000*val

            # Morning Shift after Evening Shift
            val = morningAfterEvening(employee)
            if val:
                penalty += 800*val

            # Evening Shift after Night
            val = eveningAfterNight(employee)
            if val:
                penalty += 800*val

            # Two days Off after 4 Night Shifts
            if not twoDaysOffAfterNightShift(employee):
                penalty += 100

            # Two days Off after 7 days of work
            if not twoDaysOffAfterSevenDays(employee):
                penalty += 100

            val = workDayoffWork(employee)
            if val:
                penalty += 1*val

            val = dayOffWorkDayoff(employee)
            if val:
                penalty += 1*val

            if workInWeekends(employee):
                penalty += 1

        ret[i] = penalty

    return ret


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