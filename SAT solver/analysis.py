import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

def main():

    folder = 'results'
    heuristics = ['fewestoptions', 'JW', 'JWTS', 'random']
    all_data = read_results(folder)

    # Getting initial statistics
    mean = get_mean_grouped(all_data)
    print(mean)

    # Visualization
    # distplot_groups(all_data, "Backtracks", heuristics, \
    #     xlab="Backtracks", ylab="log Count", title="Spread of backtrack counts")
    # distplot_groups(all_data, "TriedAssignments", heuristics, \
    #     xlab="Tried Assignments", ylab="log Count", title="Spread of Tried Assignments counts")
    # distplot_groups(all_data, "Difficulty", heuristics, \
    #     xlab="Difficulty", ylab="log Count", title="Spread of difficulty counts")

    #scatter_groups(all_data, "Difficulty", "random", "fewestoptions", title="Difficulty across heuristics")

    # Statistical testing: ANOVA
    ANOVA(all_data, "Difficulty")


def read_results(folder, long_format=False):

    '''Read in the results of the SAT experiment by concatenating dataframes.'''


    # the empty dataframe
    all_data = pd.DataFrame()
    long_data = pd.DataFrame(names=["Difficulty", "Heuristic"])

    for filename in os.scandir(folder):

        # the heuristic is not in the file yet, so extract it from filename
        heuristic = filename.name.split('_')[1]

        colnames = ["PuzzleID", heuristic + "-TriedAssignments", heuristic + "-Backtracks"]

        df = pd.read_csv(filename, header=None, names=colnames).set_index('PuzzleID')

        df[heuristic + "-Difficulty"] = df[heuristic + "-TriedAssignments"] + df[heuristic + "-Backtracks"]

        #df[heuristic + "-DifficultyRank"] = df[heuristic + "-Difficulty"].rank()

        if all_data.empty:
            all_data = df
        else:
            all_data = all_data.join(df)

    return all_data


def get_mean_grouped(df, ignore_zeros=True):

    '''Extracting the mean from a dataframe'''

    if ignore_zeros:
        df = df.replace(0, np.NaN)

    return df.mean()


def distplot_groups(df, var_viz, groups, xlab=None, ylab=None, title=None):

    '''Drawing the groupwise distribution of a variable within a dataframe.'''

    for var in groups:

        dffilter = df.filter(regex=var).filter(regex=var_viz)
        data = dffilter[dffilter[var + "-" + var_viz] > 0]
        logdata = np.log(data[var + "-" + var_viz])
        ax = sns.distplot(logdata, label=var)

    if xlab:
        plt.xlabel(xlab)
    if ylab:
        plt.ylabel(ylab)
    if title:
        plt.title(title)

    plt.legend()
    plt.show()


def scatter_groups(df, scatter_var, xaxis, yaxis, title=None):

    df = df.replace(0, np.NaN)
    xvar = xaxis + "-" + scatter_var
    yvar = yaxis + "-" + scatter_var
    sns.scatterplot(x=xvar, y=yvar, data=df)

    plt.xlabel(xaxis)
    plt.ylabel(yaxis)

    if title:
        plt.title(title)

    plt.show()


def ANOVA(df, metric, pthreshold=0.05):

    f, p = stats.f_oneway(df["fewestoptions-" + metric], df["JW-" + metric], \
        df["JWTS-" + metric], df["random-" + metric])


    print('One-way ANOVA')
    print('=============')

    print('F value:', f)
    print('P value:', p, '\n')

    if p < pthreshold:
        print("Reject null: groups significantly different")




    mc = MultiComparison(data['Score'], data['Archer'])
    result = mc.tukeyhsd()

    print(result)
    print(mc.groupsunique)


if __name__ == '__main__':
    main()
