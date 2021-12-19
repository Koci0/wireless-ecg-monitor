
from bluetooth.bluez import stop_advertising
import modules.const as const

import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from multiprocessing import Event, Process

from modules.logger import Logger
logger = Logger()


class Plotter:

    width = 36
    height = 6

    def __init__(self, stopEvent: Event, processedData: dict, maxPointOnPlot=const.MAX_POINTS_ON_PLOT):
        self.stopEvent = stopEvent
        self.processedData = processedData
        self.lastTime = 0
        self.lastPlot = time.time()
        self.maxPointsOnPlot = maxPointOnPlot

        self.fig = plt.figure(figsize=(self.width, self.height))
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=const.PLOT_INTERVAL * 1000)
        
        self.process = Process(target=self.animate, args=(0, ), daemon=True)

    def animate(self, _):
        if self.stopEvent.is_set():
            self.stop()
            return

        times = list(self.processedData.keys())
        values = list(self.processedData.values())
        if not times or not values:
            return

        minTimes = min(times)
        maxTimes = max(times)
        maxValues = max(values)

        self.ax.clear()
        self.ax.set_xlim([minTimes, maxTimes])
        self.ax.set_ylim([0, maxValues])
        self.ax.plot(times, values)

        plt.annotate(
            f"Delay: {str(round(time.time() - self.lastPlot, 2))}", xy=(minTimes, maxValues))
        plt.axvline(x=self.lastTime, color="red")

        self.lastTime = times[-1]
        self.lastPlot = time.time()

    def start(self):
        plt.show()
        self.process.start()
    
    def stop(self):
        plt.close()
