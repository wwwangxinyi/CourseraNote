# To complete this assignment, create a code cell that:
# Creates a number of subplots using the `pyplot subplots` or `matplotlib gridspec` functionality.
# Creates an animation, pulling between 100 and 1000 samples from each of the random variables (`x1`, `x2`, `x3`, `x4`) for each plot and plotting this as we did in the lecture on animation.
# Bonus: Go above and beyond and "wow" your classmates (and me!) by looking into matplotlib widgets and adding a widget which allows for parameterization of the distributions behind the sampling animations.


# Tips:
# Before you start, think about the different ways you can create this visualization to be as interesting and effective as possible.
# Take a look at the histograms below to get an idea of what the random variables look like, as well as their positioning with respect to one another. This is just a guide, so be creative in how you lay things out!
# Try to keep the length of your animation reasonable (roughly between 10 and 30 seconds).

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
# generate 4 random variables from the random, gamma, exponential, and uniform distributions
n = 100
x1 = np.random.normal(5, 1, n)
x2 = np.random.gamma(2, 1.5, n)
x3 = np.random.exponential(2, n)
x4 = np.random.uniform(0, 10, n)


def update(curr):
    if curr == n:
        a.event_source.stop()
    plt.cla()

    bins = 10
    ax1.hist(x1[:curr], bins=bins)
    ax1.set_title('x1:Normal')
    ax2.hist(x2[:curr], bins=bins)
    ax2.set_title('x2:Gamma')
    ax3.hist(x3[:curr], bins=bins)
    ax3.set_title('x3:Exponential')
    ax4.hist(x4[:curr], bins=bins)
    ax4.set_title('x4:Uniform')
    plt.axis([0, 10, 0, 50])
    plt.gca().set_ylabel('frequency')
    plt.gca().set_xlabel('value')


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
    2, 2, sharex=True, sharey=True)
a = animation.FuncAnimation(fig, update, interval=1)
fig.show()
