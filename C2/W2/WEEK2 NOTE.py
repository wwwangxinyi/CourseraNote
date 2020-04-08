import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import randint
# make a plot without using the scripting layer.
# create a new figure
fig = Figure()
# associate fig with the backend
canvas = FigureCanvasAgg(fig)
# add a subplot to the fig
ax = fig.add_subplot(111)
ax.plot(3, 2, '.')
canvas.print_png('test.png')

plt.figure()
plt.plot(3, 2, 'o')
# get the current axes
ax = plt.gca()
# Set axis properties [xmin, xmax, ymin, ymax]
ax.axis([0, 6, 0, 10])

plt.figure()
plt.plot(1.5, 1.5, 'o')
plt.plot(1, 1, 'o')
plt.plot(2, 2, 'o')

plt.show()

# scatter plot
# x=np.array([1,2,3,4,5,6])
# y=x
zip_generator = zip([1, 2, 3, 4, 5, 6, 7, 8], [8, 7, 6, 5, 4, 3, 2, 1])
x, y = zip(*zip_generator)
plt.figure()
plt.scatter(x[:2], y[:2], s=100, c='blue', label='point1')
plt.scatter(x[2:], y[2:], s=100, c='green', label='point2')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title('first try')
plt.legend(loc=2, frmeon=False, title='legend')
plt.show()

# line plot
plt.figure()
linear_data = np.array([1, 2, 3, 4, 5, 6, 7, 8])
exponential_data = linear_data**2
plt.plot(linear_data, '-o', exponential_data, '-o')
plt.plot([37, 84, 35], '--r')
plt.gca().fill_between(range(len(linear_data)), linear_data,
                       exponential_data, facecolor='blue', alpha=0.2)

plt.show()

# work with date
plt.figure()

linear_data = np.array([1, 2, 3, 4, 5, 6, 7, 8])
exponential_data = linear_data**2
obs_dates = np.arange('2017-01-01', '2017-01-09', dtype='datetime64[D]')
# trying to plot a map will result in an error
obs_dates = list(map(pd.to_datetime, obs_dates))
plt.plot(obs_dates, linear_data, '-o', obs_dates, exponential_data, '-o')

# rotate the tick labels for the x axis
x = plt.gca().xaxis
for item in x.get_ticklabels():
    item.set_rotation(45)
plt.subplots_adjust(bottom=0.25)

ax = plt.gca()
ax.set_xlabel('Date')
ax.set_ylabel('Units')
ax.set_title("Exponential ($x^2$) vs. Linear ($x$) performance")

plt.show()

# bar chart
plt.figure()

linear_data = np.array([1, 2, 3, 4, 5, 6, 7, 8])
exponential_data = linear_data**2
linear_err = [randint(0, 3) for x in range(len(linear_data))]

xvals = range(len(linear_data))
new_axvals = []
for item in xvals:
    new_axvals.append(item+0.3)

# plt.bar(xvals, linear_data, width=0.3)
# plt.bar(new_axvals, exponential_data, width=0.3)

# plt.bar(xvals, linear_data, width=0.3, yerr=linear_err)

# plt.bar(xvals, linear_data, width=0.3)
# plt.bar(xvals, exponential_data, width=0.3, bottom=linear_data)

plt.barh(xvals, linear_data, height=0.3)
plt.barh(xvals, exponential_data, height=0.3, left=linear_data, color='r')

plt.show()

# dejuncking

plt.figure()

languages = ['Python', 'SQL', 'Java', 'C++', 'JavaScript']
pos = np.arange(len(languages))
popularity = [56, 39, 34, 34, 29]

# change the bar color to be less bright blue
bars = plt.bar(pos, popularity, align='center',
               linewidth=0, color='lightslategrey')
# change one bar, the python bar, to a contrasting color
bars[0].set_color('#1F77B4')

# soften all labels by turning grey
plt.xticks(pos, languages, alpha=0.8)
# remove the Y label since bars are directly labeled
#plt.ylabel('% Popularity', alpha=0.8)
plt.title(
    'Top 5 Languages for Math & Data \nby % popularity on Stack Overflow', alpha=0.8)

# remove all the ticks (both axes), and tick labels on the Y axis
plt.tick_params(top='off', bottom='off', left='off',
                right='off', labelleft='off', labelbottom='on')

# remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)

# direct label each bar with Y axis values
for bar in bars:
    height = bar.get_height()
    plt.gca().text(bar.get_x() + bar.get_width()/2, bar.get_height() - 5, str(int(height)) + '%',
                   ha='center', color='w', fontsize=11)
plt.show()
