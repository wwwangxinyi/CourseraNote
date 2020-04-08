# Easiest option: Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.

# Harder option: Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).

# Even Harder option: Add interactivity to the above, which allows the user to click on the y axis to set the value of interest. The bar colors should change with respect to what value the user has selected.

# Hardest option: Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).

import matplotlib.cm as cm
import matplotlib.colors as mcol
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
n = 3650
alpha = 1 - 0.95
mu = 1.96

np.random.seed(12345)
df = pd.DataFrame([np.random.normal(32000, 200000, 3650),
                   np.random.normal(43000, 100000, 3650),
                   np.random.normal(43500, 140000, 3650),
                   np.random.normal(48000, 70000, 3650)],
                  index=[1992, 1993, 1994, 1995])
df['mean'] = df.mean(axis=1)
df['std'] = df.std(axis=1)
df['CI'] = 1.96 * df['std']/np.sqrt(df.shape[1])
df['upper'] = df['mean'] + df['CI']
df['lower'] = df['mean'] - df['CI']


# def colorchk(minval, maxval):
#     if maxval < value:
#         return "blue"
#     if minval > value:
#         return "red"
#     return "white"


# df['color'] = df.apply(lambda row: colorchk(
#     row['lower'], row['upper']), axis=1)
# plt.figure()
# plt.bar(range(len(df.index)), df['mean'],
#         color=df['color'], yerr=df['CI'], capsize=5, width=0.5)
# plt.axhline(y=value, color="black")
# plt.xticks(range(len(df.index)), df.index)
# plt.show()

value = 42000


def percent(minval, maxval, value=42000):
    if minval > value:
        return 1
    if maxval < value:
        return 0
    return (maxval - value)/(maxval - minval)


df['percent'] = df.apply(lambda row: percent(
    row['lower'], row['upper']), axis=1)

cm_1 = mcol.LinearSegmentedColormap.from_list(
    "MyCmapName", ["dodgerblue", "white", "orange"])
result = cm.ScalarMappable(cmap=cm_1)
result.set_array([])

plt.figure()
plt.bar(range(len(df.index)), df['mean'],
        color=result.to_rgba(df['percent']), edgecolor='black', lw=1, yerr=df['CI'], capsize=5, width=0.5)
plt.axhline(y=value, color="black")
plt.xticks(range(len(df.index)), df.index)
plt.colorbar(result, orientation='horizontal')
plt.show()

plt.savefig('./test.jpg')
