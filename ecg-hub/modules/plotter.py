
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from collections import deque

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HEIGHT = 6
WIDTH = 36


class Plotter:
    def __init__(self, times: deque, values: deque, maxPointOnPlot=100, interval=10):
        self.times = times
        self.values = values
        self.maxPointsOnPlot = maxPointOnPlot
        self.interval = interval

        self.fig = plt.figure(figsize=(WIDTH, HEIGHT))
        self.ax1 = self.fig.add_subplot(1, 1, 1)

        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=500)

    def animate(self, i):
        self.ax1.clear()
        self.ax1.plot(self.times, self.values)

    def show(self):
        plt.show()
