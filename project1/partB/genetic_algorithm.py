#!/usr/bin/env python3
import numpy as np 
import constant as c
import soft_constraints as soft
from argparse import ArgumentParser


def geneticAlgorithm(pop):
    initPop = generateRandomPopulation(pop)

    initialViability = checkHardConstraints(initPop)

    penalties = penaltyFunction(initPop)
    print(penalties)


def generateRandomPopulation(pop):
    population = np.empty([pop, c.EMPLOYEE_COUNT, c.DAY_COUNT])
    for i in range(pop):
        population[i] = np.random.randint(0, 4, size=(c.EMPLOYEE_COUNT, c.DAY_COUNT))

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
    pop = population.shape[0]
    ret = np.zeros(pop)

    for i in range(pop):
        # As many employees as required per shift per day
        populationT = population[i].transpose()
        dayNumber = 0
        for day in populationT:
            if not workforceSatisfied(day, dayNumber):
                continue

            dayNumber += 1

        ret[i] = 1

    return ret


def penaltyFunction(population):
    pop = population.shape[0]
    ret = np.zeros(pop)

    for i in range(pop):
        # Give a value to a population based on soft constraints
        penalty = 0

        for employee in population[i]:
            # MAX 70 hours of work (per week or per 14 days)
            if soft.hoursWorked(employee) > c.MAX_WORK_HOURS:
                penalty += 1000

            # MAX 7 continuous days of work
            if soft.straightDaysWorked(employee):
                penalty += 1000

            # MAX 4 NIGHT SHIFTS
            if soft.maxNightShifts(employee):
                # Multiply the penalty if constraint is broken more than once in schedule
                penalty += 1000*soft.maxNightShifts(employee)

            # Morning Shift after Night Shift
            if soft.morningAfterNight(employee):
                penalty += 1000*soft.morningAfterNight(employee)

            # Morning Shift after Night Shift
            if soft.morningAfterNight(employee):
                penalty += 1000*soft.morningAfterNight(employee)

            # Morning Shift after Evening Shift
            if soft.morningAfterEvening(employee):
                penalty += 1000*soft.morningAfterEvening(employee)

            # Evening Shift after Night
            if soft.eveningAfterNight(employee):
                penalty += 1000*soft.eveningAfterNight(employee)

            # Two days Off after 4 Night Shifts
            if soft.twoDaysOffAfterNightShift(employee):
                penalty += 100

            # Two days Off after 7 days of work
            if soft.twoDaysOffAfterSevenDays(employee):
                penalty+=100

        ret[i] = penalty

    return ret


if __name__ == "__main__":
    parser = ArgumentParser(description="Run genetic algorithm for the WHPP problem.")
    parser.add_argument("--pop", type=int, default=100,
                        help="When I know I will tell you.")
    parser.add_argument("--iter", type=int, default=10,
                        help="When I know I will tell you.")
    parser.add_argument("--psel", type=float, default=.1,
                        help="When I know I will tell you.")
    parser.add_argument("--pcross", type=float, default=.1,
                        help="When I know I will tell you.")
    parser.add_argument("--pmut", type=float, default=.1,
                        help="When I know I will tell you.")
    args = parser.parse_args()

    geneticAlgorithm(args.pop)
