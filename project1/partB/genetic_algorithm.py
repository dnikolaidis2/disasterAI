#!/usr/bin/env python3
import numpy as np 
import constant as c
import soft_constraints as soft
from argparse import ArgumentParser
from util import minMaxNormalize, uniqueCounts


def geneticAlgorithm(pop):
    initPop = generateRandomPopulation(pop)

    initialViability = checkHardConstraints(initPop)
    print(initialViability)

    penalties = penaltyFunction(initPop)
    print(penalties)


def generateRandomPopulation(pop):
    population = np.empty([pop, c.EMPLOYEE_COUNT, c.DAY_COUNT])
    for i in range(pop):
        chromosome = np.empty([c.DAY_COUNT, c.EMPLOYEE_COUNT], dtype=int)
        for day in range(c.DAY_COUNT):
            while True:
                chromosome[day] = np.random.randint(0, 4, size=(c.EMPLOYEE_COUNT))
                workDaysIndex = np.nonzero(chromosome[day])
                test = workDaysIndex[0].size
                if workDaysIndex[0].size == 25 or workDaysIndex[0].size == 20 or workDaysIndex[0].size == 15:
                    break
        # print(chromosome.transpose())
        population[i] = chromosome.transpose()

    return population


def generateNotSoRandomPopulation(pop):
    population = np.empty([pop, c.EMPLOYEE_COUNT, c.DAY_COUNT])
    for i in range(pop):
        chromosome = np.empty((c.DAY_COUNT, c.EMPLOYEE_COUNT), dtype=int)
        coverage = c.REQUIRED_COVERAGE.transpose()
        for day in range(c.DAY_COUNT):
            employees = np.arange(c.EMPLOYEE_COUNT)
            np.random.shuffle(employees)
            shifts = np.split(employees, [coverage[day][0],
                                          coverage[day][0] + coverage[day][1],
                                          coverage[day][0] + coverage[day][1] + coverage[day][2]])
            np.put(chromosome[day], shifts[0], 1)
            np.put(chromosome[day], shifts[1], 2)
            np.put(chromosome[day], shifts[2], 3)
            # np.put(chromosome[day], shifts[3], np.random.randint(0, 4, size=shifts[3].shape))
            pzero = 0.85
            np.put(chromosome[day], shifts[3], np.random.choice(np.arange(4), size=shifts[3].shape,
                                                                p=[pzero, (1-pzero)/3, (1-pzero)/3, (1-pzero)/3]))

        population[i] = chromosome.transpose()

    return population


def generateTotallyRandomPopulation(pop):
    population = np.empty([pop, c.EMPLOYEE_COUNT, c.DAY_COUNT])
    for i in range(pop):
        population[i] = np.random.randint(0, 4, size=(c.EMPLOYEE_COUNT, c.DAY_COUNT))

    return population


def workforceSatisfied(chromosome):
    # A bit complicated but for every day in a chromosome calculate the counts off all unique elements
    # with unique(). These counts are the numbers of employees working each shift on a given day.
    # Select only shifts that are greater then 0. This table has the coverage of every shift per day.
    workforce_coverage = np.apply_along_axis(uniqueCounts, 0, chromosome, 0)

    # For every element in workforce_coverage check that its greater or equal
    # to the minimum requirements given by REQUIRED_COVERAGE.
    return np.all(workforce_coverage >= c.REQUIRED_COVERAGE)


def fitnessFunction():
    return 1


def checkHardConstraints(population):
    pop = population.shape[0]
    ret = np.zeros(pop, dtype=bool)

    for i in range(pop):
        ret[i] = workforceSatisfied(population[i])

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
                penalty += 100

        ret[i] = penalty

    return minMaxNormalize(ret)


if __name__ == "__main__":
    parser = ArgumentParser(description="Run genetic algorithm for the WHPP problem.")
    parser.add_argument("--pop", type=int, default=10,
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
