#!/usr/bin/env python3
import numpy as np 
import constant as c
import soft_constraints as soft
import statistics as stat
from argparse import ArgumentParser
from util import minMaxNormalize, uniqueCounts
from random import uniform
from plot import plotData
import crossover_function as cross


def geneticAlgorithm(pop, iter_max, pcross, corss_type, pmut, mut_type, save_plot=False, file_name="figure"):
    count = 0
    print(f"Starting generation {count}! Initial population is {pop}")
    print(f"Function parameters are:\n\titer_max = {iter_max}"
          # f"\n\tpsel = {psel}"
          f"\n\tpcross = {pcross}"
          f"\n\tcorss_type = {corss_type}"
          f"\n\tpmut = {pmut}"
          f"\n\tmut_type = {mut_type}")
    # Generate initial population
    population = generateNotSoRandomPopulation(pop)
    # check hard constraints
    hard_constraint_check = checkHardConstraints(population)
    population = population[np.argwhere(hard_constraint_check == True).flatten()]
    print(f"Count of initial population going to the next generation: {np.count_nonzero(hard_constraint_check)}")

    # Fitness calculation for every chromosome.
    penalties = penaltyFunction(population)
    fitness = fitnessFunction(population, penalties)
    meanPenaltiesList = [penalties.mean()]
    elitePenaltiesList = [penalties.min()]
    print(f"Average penalty = {meanPenaltiesList[-1]:.3f},"
          f" Min penalty = {penalties.min():.3f}, Max penalty = {penalties.max():.3f}")
    print(f"Min fitness = {fitness.min():.3f}, Max fitness = {fitness.max():.3f}")

    while True:
        # Generate next generation
        count += 1
        print(f"---------- Moving to generation {count} ----------")
        print("Selecting...")
        population = selectWorthyChromosomes(population, fitness)
        print("Crossing over...")
        population = cross.crossover(population, corss_type, pcross)
        print("Mutating ...")
        population = mutate(population, mut_type, pmut, .33)

        hard_constraint_check = checkHardConstraints(population)
        population = population[np.argwhere(hard_constraint_check == True).flatten()]
        print(f"Count of population that survived: {np.count_nonzero(hard_constraint_check)}")
        penalties = penaltyFunction(population)
        fitness = fitnessFunction(population, penalties)
        meanPenaltiesList.append(penalties.mean())
        elitePenaltiesList.append(penalties.min())
        print(f"Average penalty = {meanPenaltiesList[-1]:.3f},"
              f" Min penalty = {penalties.min():.3f}, Max penalty = {penalties.max():.3f}")
        print(f"Min fitness = {fitness.min():.3f}, Max fitness = {fitness.max():.3f}")

        if terminationCriteria(count, iter_max, meanPenaltiesList, np.count_nonzero(hard_constraint_check)):
            # Finished is true!
            plotData(count, meanPenaltiesList, elitePenaltiesList,
                     f"Results with pop={pop} for pcorss={pcross},"
                     f" corss_type={corss_type}, pmut={pmut}, mut_type={mut_type}",
                     save_plot, file_name)
            break

    return meanPenaltiesList, elitePenaltiesList


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
    new_fitness = np.zeros(fitness.shape)
    sorted_indexes = np.argsort(fitness)
    sorted_fitness = fitness[sorted_indexes]
    sorted_population = population[sorted_indexes]

    # Eliteness
    new_population[-1] = sorted_population[-1]
    new_population[-2] = sorted_population[-2]
    new_fitness[-1] = sorted_fitness[-1]
    new_fitness[-2] = sorted_fitness[-2]
    sorted_fitness = sorted_fitness[:-2]
    sorted_population = sorted_population[:-2]

    if sorted_fitness.size == 0:
        return new_population

    fitness_cumsum = minMaxNormalize(np.cumsum(sorted_fitness))

    # Roulette wheel selection
    for i in range(fitness_cumsum.size):
        prob = uniform(0, 1)
        roulette = list(fitness_cumsum.copy())
        roulette.append(prob)
        roulette = sorted(roulette)
        new_population[i] = sorted_population[roulette.index(prob)]
        new_fitness[i] = sorted_fitness[roulette.index(prob)]

    # Sort new population
    sorted_indexes = np.argsort(new_fitness)

    return new_population[sorted_indexes]


def mutate(population, type, pmut, pmut_depth):
    for i in range(population.shape[0]-2):
        if uniform(0, 1) <= pmut:
            chromosome = population[i].transpose()
            for j in range(chromosome.shape[0]):
                if uniform(0, 1) <= pmut_depth:
                    if type == 'swap':
                        inds = np.random.choice(chromosome.shape[1], 2)
                        tmp = chromosome[j][inds[0]]
                        chromosome[j][inds[0]] = chromosome[j][inds[1]]
                        chromosome[j][inds[1]] = tmp
                    elif type == "bit-flip":
                        ind = np.random.choice(chromosome.shape[1], 1)
                        chromosome[j][ind] = np.random.choice(c.ALLOWED_VALUES)

            population[i] = chromosome.transpose()
    return population


def terminationCriteria(count, iter_max, meanPenalties, popCount):
    # print(meanPenalties)
    # Criteria 1 : Mean penalties stop decreasing - Algorithm is not improving
    s = len(meanPenalties)
    if s > 4:
        if stat.stdev(meanPenalties[s-4:s-1]) < c.MIN_PENALTY_DIFFERENTIATION:
            print('Algorithm is not improving... Exiting!')

    # Criteria 2 : Reached Max Iterations
    if count >= iter_max:
        print("Reached max iterations... Exiting!")
        return True
    
    # Criteria 3 : Stop when population gets low 
    if popCount < c.MINIMUM_POPULATION:
        print("Population is too low... Exiting!")
        return True

    return False


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
            if soft.hoursWorked(employee) > c.MAX_WORK_HOURS:
                penalty += 1000

            # MAX 7 continuous days of work
            if soft.straightDaysWorked(employee):
                penalty += 1000

            # MAX 4 NIGHT SHIFTS
            val = soft.maxNightShifts(employee)
            if val:
                # Multiply the penalty if constraint is broken more than once in schedule
                penalty += 1000*val

            # Morning Shift after Night Shift
            val = soft.morningAfterNight(employee)
            if val:
                penalty += 1000*val

            # Morning Shift after Evening Shift
            val = soft.morningAfterEvening(employee)
            if val:
                penalty += 800*val

            # Evening Shift after Night
            val = soft.eveningAfterNight(employee)
            if val:
                penalty += 800*val

            # Two days Off after 4 Night Shifts
            if not soft.twoDaysOffAfterNightShift(employee):
                penalty += 100

            # Two days Off after 7 days of work
            if not soft.twoDaysOffAfterSevenDays(employee):
                penalty += 100

            val = soft.workDayoffWork(employee)
            if val:
                penalty += 1*val

            val = soft.dayOffWorkDayoff(employee)
            if val:
                penalty += 1*val

            if soft.workInWeekends(employee):
                penalty += 1

        ret[i] = penalty

    return ret


if __name__ == "__main__":
    parser = ArgumentParser(description="Run genetic algorithm for the WHPP problem.")
    parser.add_argument("--pop", type=int, default=1000,
                        help="Initial population count.")
    parser.add_argument("--iter-max", type=int, default=50,
                        help="Maximum iterations to run for.")
    # parser.add_argument("--psel", type=float, default=.1,
    #                     help="When I know I will tell you.")
    parser.add_argument("--pcross", type=float, default=0.7,
                        help="The probability with which to decide whether to crossover chromosomes or not.")
    parser.add_argument("--cross-type", default="uniform", choices=c.CROSS_TYPE,
                        help="The crossover algorithm to use.")
    parser.add_argument("--pmut", type=float, default=.1,
                        help="The probability with which to decide whether to mutate chromosomes or not.")
    parser.add_argument("--mut-type", default="swap", choices=c.MUT_TYPE,
                        help="The mutation algorithm to use.")
    parser.add_argument("--save-plot", action='store_true',
                        help="Save plot instead of displaying it.")
    parser.add_argument("--plot-file-name", default="figure",
                        help="File name for saved plot.")
    args = parser.parse_args()

    geneticAlgorithm(args.pop, args.iter_max, args.pcross, args.cross_type, args.pmut, args.mut_type,
                     args.save_plot, args.plot_file_name)
