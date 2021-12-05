
import modules.const as const

import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Plotter:

    width = 36
    height = 6

    def __init__(self, processedData: dict, maxPointOnPlot=const.MAX_POINTS_ON_PLOT, interval=2000):
        self.processedData = processedData
        self.lastTime = 0
        self.lastPlot = time.time()
        self.maxPointsOnPlot = maxPointOnPlot
        self.interval = interval

        self.fig = plt.figure(figsize=(self.width, self.height))
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=interval)

    def animate(self, _):
        times = list(self.processedData.keys())
        values = list(self.processedData.values())

        minTimes = min(times)
        maxTimes = max(times)
        maxValues = max(values)

        self.ax.clear()
        self.ax.set_xlim([minTimes, maxTimes])
        self.ax.set_ylim([0, maxValues])
        self.ax.plot(times, values)

        plt.annotate(f"Delay: {str(round(time.time() - self.lastPlot, 2))}", xy=(minTimes, maxValues))
        plt.axvline(x=self.lastTime, color="red")

        self.lastTime = times[-1]
        self.lastPlot = time.time()

    def show(self):
        plt.show()
