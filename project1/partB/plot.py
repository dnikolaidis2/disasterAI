import matplotlib.pyplot as plt 

def plotData(popCount, popMeanCost, elitCost):
    plt.plot(range(popCount+1), popMeanCost)
    plt.title('Mean Penalty of Population')
    plt.xlabel('Population No.')
    plt.ylabel('Mean Penalty')
    plt.show()

    plt.figure(2)
    plt.plot(range(popCount+1), elitCost)
    plt.title('Mean Penalty of Elit Chromosome')
    plt.xlabel('Population No.')
    plt.ylabel('Mean Penalty')
    plt.show()
     