from random import shuffle
import mpl_toolkits.axes_grid1.inset_locator as mpl_il
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# # # subplot
# plt.figure()
# ax1 = plt.subplot(1, 2, 1)

# linear_data = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# plt.plot(linear_data, '-o')

# exp_data = linear_data ** 2
# # pass sharey=ax1 to ensure the two subplots share the same y axis
# ax2 = plt.subplot(1, 2, 2, sharey=ax1)
# plt.plot(exp_data, '-o')

# plt.subplot(1, 2, 1)
# plt.plot(exp_data, '-o')
# plt.show()

# fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)
#       ) = plt.subplots(3, 3, sharex=True, sharey=True)
# # plot the linear_data on the 5th subplot axes
# ax5.plot(linear_data, '-')

# for ax in plt.gcf().get_axes():
#     for label in ax.get_xticklabels()+ax.get_yticklabels():
#         label.set_visible(True)

# plt.show()


# # # histogram
# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True)
# axs = [ax1, ax2, ax3, ax4]
# for n in range(0, len(axs)):
#     sample_size = 10**(n+1)
#     sample = np.random.normal(loc=0.0, scale=1.0, size=sample_size)
#     axs[n].hist(sample, bins=100)
#     axs[n].set_title('n={}'.format(sample_size))

# plt.figure()
# Y = np.random.normal(loc=0, scale=1.0, size=1000)
# X = np.random.random(size=1000)
# plt.scatter(X, Y)

# plt.figure()
# gspec = gridspec.GridSpec(3, 3)
# top_histogram = plt.subplot(gspec[0, 1:])
# side_histogram = plt.subplot(gspec[1:, 0])
# lower_right = plt.subplot(gspec[1:, 1:])

# Y = np.random.normal(loc=0, scale=1.0, size=10000)
# X = np.random.random(size=10000)
# lower_right.scatter(X, Y)
# top_histogram.hist(X, bins=100)
# side_histogram.hist(Y, bins=100, orientation='horizontal')

# top_histogram.clear()
# top_histogram.hist(X, bins=100, normed=True)
# side_histogram.clear()
# side_histogram.hist(Y, bins=100, orientation='horizontal', normed=True)
# side_histogram.invert_xaxis()
# plt.show()

# # box & whisker plot
# import pandas as pd
# normal_sample = np.random.normal(loc=0, scale=1, size=10000)
# random_sample = np.random.random(size=10000)
# gamma_sample = np.random.gamma(2, size=10000)

# df = pd.DataFrame({'normal': normal_sample,
#                    'random': random_sample,
#                    'gamma': gamma_sample})
# plt.figure()
# plt.boxplot([df['normal'], df['random'], df['gamma']], whis='range')
# plt.show()

# plt.figure()
# plt.hist(df['gamma'], bins=100)

# plt.figure()
# plt.boxplot([df['normal'], df['random'], df['gamma']], whis='range')
# ax2 = mpl_il.inset_axes(plt.gca(), width='60%', height='40%', loc=2)
# ax2.hist(df['gamma'], bins=100)
# ax2.margins(x=0.5)
# ax2.yaxis.tick_right()  # switch the y axis ticks for ax2 to the right side
# plt.show()

# # heatmap
# plt.figure()
# Y = np.random.normal(loc=0, scale=1, size=10000)
# X = np.random.random(size=10000)
# _ = plt.hist2d(X, Y, bins=100)
# plt.colorbar()
# plt.show()

# #animation
# import matplotlib.animation as animation
# n = 100
# x = np.random.randn(n)

# def update(curr):
#     if curr == n:
#         a.event_source.stop()
#     plt.cla()  # not clear()
#     bins = np.arange(-4, 4, 0.5)
#     plt.hist(x[:curr], bins=bins)
#     plt.axis([-4, 4, 0, 30])
#     plt.gca().set_title('sampling the normal distribution')
#     plt.gca().set_ylabel('frequency')
#     plt.gca().set_xlabel('value')
#     plt.annotate('n = {}'.format(curr), [3, 27])


# fig = plt.figure()
# a = animation.FuncAnimation(fig, update, interval=100)
# fig.show()

# #interactivity
# plt.figure()
# data = np.random.rand(10)
# plt.plot(data)


# def onclick(event):
#     plt.cla()
#     plt.plot(data)
#     plt.gca().set_title('Event at pixels {},{} \nand data {},{}'.format(
#         event.x, event.y, event.xdata, event.ydata))

# # tell mpl_connect we want to pass a 'button_press_event' into onclick when the event is detected
# plt.gcf().canvas.mpl_connect('button_press_event', onclick)
# plt.show()

origins = ['China', 'Brazil', 'India', 'USA', 'Canada',
           'UK', 'Germany', 'Iraq', 'Chile', 'Mexico']

shuffle(origins)

df = pd.DataFrame({'height': np.random.rand(10),
                   'weight': np.random.rand(10),
                   'origin': origins})
plt.figure()
# picker=5 means the mouse doesn't have to click directly on an event, but can be up to 5 pixels away
plt.scatter(df['height'], df['weight'], picker=5)
plt.gca().set_ylabel('Weight')
plt.gca().set_xlabel('Height')


def onpick(event):
    origin = df.iloc[event.ind[0]]['origin']
    plt.gca().set_title('Selected item came from {}'.format(origin))


# tell mpl_connect we want to pass a 'pick_event' into onpick when the event is detected
plt.gcf().canvas.mpl_connect('pick_event', onpick)
plt.show()
