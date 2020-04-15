#!/usr/bin/env python3
import numpy as np 
import constant as c
import soft_constraints as soft


def geneticAlgorithm():
    initPop = generateRandomPopulation()

    if checkHardConstraints(initPop):
        print("Not legal.")

    penaltyFunction(initPop)


def generateRandomPopulation():
    population = np.random.randint(0, 4, size=(30, 14))
    print(population)

    return population  


def workforceSatisfied(day, dayNumber):
    employeeSchedule = np.array([[10, 10, 5, 5, 5, 5, 5],
                                 [10, 10, 10, 5, 10, 5, 5],
                                 [5, 5, 5, 5, 5, 5, 5]]).transpose()
    employeeCount = np.zeros(3)

    for shift in day:
        if shift == c.MORNING:
            employeeCount[0] += 1
        elif shift == c.EVENING:
            employeeCount[1] += 1
        else:
            employeeCount[2] += 1
    
    if np.array_equal(employeeCount, employeeSchedule[dayNumber]):
        return 1

    return 0


 

def checkHardConstraints(population):
    # As many employees as required per shift per day
    populationT = population.transpose()
    dayNumber = 0
    for day in populationT:
        if workforceSatisfied(day, dayNumber):
            print("Legal day") 
        
        dayNumber += 1
        if dayNumber == 7:
            dayNumber = 0
    return 1


def penaltyFunction(population):
    # Give a value to a population based on soft constraints
    penalty = 0

    for employee in population: 
        # MAX 70 hours of work (per week or per 14 days)
        if soft.hoursWorked(employee) > c.MAX_WORK_HOURS:
            penalty += 1000

        # MAX 7 continuous days of work
        if soft.straightDaysWorked(employee):
            penalty += 1000

        # MAX 4 NIGHT SHIFTS 
        if soft.maxNightShifts(employee):
            #Multiply the penalty if constraint is broken more than once in schedule
            penalty+= 1000*soft.maxNightShifts(employee)

        #Morning Shift after Night Shift 
        if soft.morningAfterNight(employee):
            penalty += 1000*soft.morningAfterNight(employee)

    return penalty   


geneticAlgorithm()
