from genetic_algorithm import geneticAlgorithm
from constant import CROSS_TYPE, MUT_TYPE
from statistics import mean

if __name__ == "__main__":
    params = [[5000, 20, 0.8, 0.2],
              [2000, 15, 0.4, 0.1]]

    with open('mean of mins.txt', 'w') as f:
        for i, param in enumerate(params):
            for cross_type in CROSS_TYPE:
                for mut_type in MUT_TYPE:
                    mins = []
                    for j in range(5):
                        means, elites = geneticAlgorithm(param[0], param[1], param[2], cross_type, param[3], mut_type,
                                                         True, f"set_{i+1}_{cross_type}_{mut_type}_{j}")
                        mins.append(min(elites))
                    print(mins)
                    print(f"set_{i+1}_{cross_type}_{mut_type}: {mean(mins)}")
                    f.write(f"set_{i+1}_{cross_type}_{mut_type}: {mean(mins)}\n")
