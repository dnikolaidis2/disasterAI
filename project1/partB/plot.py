import importlib.util
if importlib.util.find_spec('tkinter') is None:
    print("tkinter not found on this system! Figures will be saved and not displayed.\n"
          "Install tkinter to fix this")
    show_plot = False
    import matplotlib
    matplotlib.use('agg')
else:
    show_plot = True
import matplotlib.pyplot as plt


def plotData(popCount, popMeanCost, eliteCost, sup_title="Results", save_plot=False, file_name='figure'):
    plt.figure(figsize=(16, 8))
    plt.subplot(121)
    plt.plot(range(popCount+1), popMeanCost)
    plt.title('Mean Penalty of Population')
    plt.xlabel('Generation No.')
    plt.ylabel('Mean Penalty')

    plt.subplot(122)
    plt.plot(range(popCount+1), eliteCost)
    plt.title('Penalty of Elite Chromosome')
    plt.xlabel('Generation No.')
    plt.ylabel('Penalty')

    plt.suptitle(sup_title)

    if not show_plot or save_plot:
        plt.savefig(file_name)
    elif show_plot and not save_plot:
        plt.show()
