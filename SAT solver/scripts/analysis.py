import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=3)
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
import itertools

def main():

    folder = '../results'
    heuristics = ['nishio', 'JW', 'JWTS', 'random', 'MOM']
    all_data, long_data = read_results(folder, long_format=True)

    # Getting initial statistics
    mean = get_mean_grouped(all_data)
    print(mean)

    # Visualization
    distplot_groups(all_data, "Backtracks", heuristics, \
        xlab="Backtracks", ylab="log Count", title="Spread of Backtrack counts")
    distplot_groups(all_data, "TriedAssignments", heuristics, \
        xlab="Tried Assignments", ylab="log Count", title="Spread of Tried Assignments counts")
    distplot_groups(all_data, "Difficulty", heuristics, \
        xlab="Difficulty", ylab="log Count", title="Spread of difficulty scores")

    #scatter_groups(all_data, "Difficulty", "random", "nishio", title="Difficulty across heuristics")
    scatter_all_groups(all_data, "Difficulty", heuristics, title="Difficulty across heuristics")

    # Statistical testing: ANOVA
    ANOVA(all_data, long_data, "Difficulty")


def read_results(folder, long_format=False):

    '''Read in the results of the SAT experiment by concatenating dataframes.'''


    # the empty dataframe
    all_data = pd.DataFrame()
    long_data = pd.DataFrame(columns=["Difficulty", "Heuristic"])

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

        if long_format:
            new_df = pd.DataFrame()
            new_df["Difficulty"] = df[heuristic + "-Difficulty"]
            new_df["Heuristic"] = heuristic
            long_data = pd.concat([long_data, new_df])

    return all_data, long_data


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


def scatter_groups(df, scatter_var, xaxis, yaxis, title=None, color=None):

    df = df.replace(0, np.NaN)
    xvar = xaxis + "-" + scatter_var
    yvar = yaxis + "-" + scatter_var

    if color:
        sns.scatterplot(x=xvar, y=yvar, data=df, hue=0, palette=[color], legend=False)
    else:
        sns.scatterplot(x=xvar, y=yvar, data=df)


    plt.xlabel(xaxis)
    plt.ylabel(yaxis)

    if title:
        plt.title(title)

    plt.axis('equal')

    plt.show()


def scatter_all_groups(df, scatter_var, groups, title=None):

    current_palette = sns.color_palette()

    combs = itertools.combinations(groups, 2)
    for i, com in enumerate(combs):
        scatter_groups(df, scatter_var, com[0], com[1], title=title, color=current_palette[i])


def ANOVA(df, longdata, metric, pthreshold=0.05):

    '''Perform ANOVA test and Tukey's test to determine significant difference
    between groups as well as the nature of this difference (which heuristic is
    significantly better than the others?)'''

    # remove rows with difficulty score 0: heuristics have no effect
    df = df[df["nishio-" + metric] > 0]

    # logtransform columns
    logfo = np.log(df["nishio-" + metric])
    logJW = np.log(df["JW-" + metric])
    logJWTS = np.log(df["JWTS-" + metric])
    logrand = np.log(df["random-" + metric])

    # perform ANOVA
    f, p = stats.f_oneway(logfo, logJW, logJWTS, logrand)

    print('One-way ANOVA')
    print('=============')
    print('F value:', f)
    print('P value:', p)

    if p < pthreshold:
        print("Reject null: groups significantly different")

    # Tukey's Test
    longdata = longdata[longdata[metric] > 0]
    data = np.log(np.array(longdata[metric], dtype='float64'))
    mc = MultiComparison(data, np.array(longdata["Heuristic"]))
    result = mc.tukeyhsd()

    print(result)
    print(mc.groupsunique)


if __name__ == '__main__':
    main()
