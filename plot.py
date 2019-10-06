# Libraries
from math import pi

import matplotlib.pyplot as plt
import pandas as pd


def plot_me(file_name, id=0):
    # Set data
    data = pd.read_csv(r'' + file_name, names=['UP', 'DOWN', 'LEFT', 'RIGHT'], header=None)
    df = pd.DataFrame({
        'group': ['A'],
        'RIGHT': data['RIGHT'].sum(),
        'UP': data['UP'].sum(),
        'LEFT': data['LEFT'].sum(),
        'DOWN': data['DOWN'].sum()
    })
    # number of variable
    categories = list(df)[1:]
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    values

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    plt.figure(id)
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    # Draw ylabels
    # ax.set_rlabel_position(0)
    # plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
    # plt.ylim(0, 40)

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.savefig(file_name + '.png')


if __name__ == '__main__':
    import glob

    path = "*.csv"
    i = 0
    # plot_me('validate_top_row.csv')
    for fname in glob.glob(path):
        plot_me(fname, id=i)
        i = i+1
