
import modules.const as const

import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from collections import deque

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Plotter:

    width = 36
    height = 6

    def __init__(self, times: deque, values: deque, maxPointOnPlot=const.MAX_POINTS_ON_PLOT, interval=10):
        self.times = times
        self.values = values
        self.lastTime = 0
        self.lastPlot = time.time()
        self.maxPointsOnPlot = maxPointOnPlot
        self.interval = interval

        self.fig = plt.figure(figsize=(self.width, self.height))
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=interval)

    def animate(self, _):
        minTimes = min(self.times)
        maxTimes = max(self.times)
        maxValues = max(self.values)

        self.ax.clear()
        self.ax.set_xlim([minTimes, maxTimes])
        self.ax.set_ylim([0, maxValues])
        self.ax.plot(self.times, self.values)

        plt.annotate(str(round(time.time() - self.lastPlot, 2)), xy=(minTimes, maxValues))
        plt.axvline(x=self.lastTime, color="red")

        self.lastTime = self.times[-1]
        self.lastPlot = time.time()

    def show(self):
        plt.show()
