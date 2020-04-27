#!/usr/bin/env python3
import numpy as np 
import constant as c
import soft_constraints as soft
from argparse import ArgumentParser
from util import minMaxNormalize, uniqueCounts
from random import uniform
import crossover_function as cross


def geneticAlgorithm(pop, iter_max, psel, pcross, pmut):
    # Generate initial population
    population = generateNotSoRandomPopulation(pop)
    # check hard constraints
    # TODO: do something with this check.
    print(checkHardConstraints(population))

    # Fitness calculation for every chromosome.
    fitness = fitnessFunction(population)
    for i in range(iter_max):
        # Generate next generation

        population = selectWorthyChromosomes(population, fitness)
        cross.crossover(population, 'TwoPoint', pcross)

        if terminationCriteria():
            # Finished is true!
            # TODO: Do stuff and exit
            break
    else:
        # Reached iter_max without reaching the termination criteria
        # TODO: Do other stuff and exit
        pass


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
            shifts = np.split(employees, np.cumsum(coverage[day]))
            np.put(chromosome[day], shifts[-1], 0)
            shift_code = 1
            for s in shifts[:-1]:
                np.put(chromosome[day], s, shift_code)
                shift_code += 1

        population[i] = chromosome.transpose()

    return population


def generateTotallyRandomPopulation(pop):
    population = np.empty([pop, c.EMPLOYEE_COUNT, c.DAY_COUNT])
    for i in range(pop):
        population[i] = np.random.randint(0, 4, size=(c.EMPLOYEE_COUNT, c.DAY_COUNT))

    return population


def selectWorthyChromosomes(population, fitness):
    # pop = population.shape[0]
    new_population = np.zeros(population.shape, dtype=int)
    sorted_indexes = np.argsort(fitness)
    sorted_fitness = fitness[sorted_indexes]
    sorted_population = population[sorted_indexes]

    # Eliteness
    new_population[-1] = sorted_population[-1]
    sorted_fitness = sorted_fitness[:-1]
    sorted_population = sorted_population[:-1]

    fitness_cumsum = minMaxNormalize(np.cumsum(sorted_fitness))

    # Roulette wheel selection
    for i in range(fitness_cumsum.size):
        prob = uniform(0, 1)
        roulette = list(fitness_cumsum.copy())
        roulette.append(prob)
        roulette = sorted(roulette)
        new_population[i] = sorted_population[roulette.index(prob)]

    return new_population


def terminationCriteria():
    return False


def workforceSatisfied(chromosome):
    # A bit complicated but for every day in a chromosome calculate the counts off all unique elements
    # with unique(). These counts are the numbers of employees working each shift on a given day.
    # Select only shifts that are greater then 0. This table has the coverage of every shift per day.
    workforce_coverage = np.apply_along_axis(uniqueCounts, 0, chromosome, 0)

    # For every element in workforce_coverage check that its greater or equal
    # to the minimum requirements given by REQUIRED_COVERAGE.
    return np.all(workforce_coverage == c.REQUIRED_COVERAGE)


def fitnessFunction(population):
    penalty = penaltyFunction(population)
    penalty_norm = minMaxNormalize(penalty, c.MIN_PENALTY, c.MAX_PENALTY)

    np.testing.assert_array_less(-penalty_norm, 0, f"New min found! {penalty[penalty.argmin()]}")
    np.testing.assert_array_less(penalty_norm, 1.0000000000000001, f"New max found! {penalty[penalty.argmax()]}")

    return 1 - penalty_norm


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

            # Morning Shift after Evening Shift
            if soft.morningAfterEvening(employee):
                penalty += 800*soft.morningAfterEvening(employee)

            # Evening Shift after Night
            if soft.eveningAfterNight(employee):
                penalty += 800*soft.eveningAfterNight(employee)

            # Two days Off after 4 Night Shifts
            if not soft.twoDaysOffAfterNightShift(employee):
                penalty += 100

            # Two days Off after 7 days of work
            if not soft.twoDaysOffAfterSevenDays(employee):
                penalty += 100
            
            if soft.workDayoffWork(employee):
                penalty += 1*soft.workDayoffWork(employee)
            
            if soft.dayOffWorkDayoff(employee):
                penalty += 1*soft.dayOffWorkDayoff(employee)
            
            if soft.workInWeekends(employee):
                penalty += 1

        ret[i] = penalty

    return ret


if __name__ == "__main__":
    parser = ArgumentParser(description="Run genetic algorithm for the WHPP problem.")
    parser.add_argument("--pop", type=int, default=100,
                        help="When I know I will tell you.")
    parser.add_argument("--iter-max", type=int, default=10,
                        help="When I know I will tell you.")
    parser.add_argument("--psel", type=float, default=.1,
                        help="When I know I will tell you.")
    parser.add_argument("--pcross", type=float, default=0.5,
                        help="When I know I will tell you.")
    parser.add_argument("--pmut", type=float, default=.1,
                        help="When I know I will tell you.")
    args = parser.parse_args()

    geneticAlgorithm(args.pop, args.iter_max, args.psel, args.pcross, args.pmut)
