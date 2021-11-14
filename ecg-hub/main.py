
import modules.const as const
from modules.bluetooth import Bluetooth
from modules.plotter import Plotter
from modules.reader import Reader
from modules.processor import Processor

import sys

from collections import deque
from threading import Event
from queue import Queue

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def process(filename: str):
    times = []
    values = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            time, value = line.strip('\n').split(" ")
            values.append(int(value))
            times.append(int(time))

    processor = Processor(times, values)
    processor.processValues()

    with open(f"processed_{filename}", "w") as file:
        for index in range(min(len(times), len(values))):
            print(f"{times[index]} {values[index]}")
            file.write(f"{times[index]} {values[index]}\n")


def plot(filename: str):
    times = []
    values = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            time, value = line.strip('\n').split(" ")
            values.append(int(value))
            times.append(int(time))

    plotter = Plotter(times, values)
    plotter.show()


def main(saveToFile: bool = True):
    times = deque(maxlen=const.MAX_POINTS_ON_PLOT)
    values = deque(maxlen=const.MAX_POINTS_ON_PLOT)
    dataQueue = Queue()
    stopEvent = Event()

    bluetooth = Bluetooth(dataQueue, stopEvent)
    reader = Reader(stopEvent, dataQueue, times, values, saveToFile)
    plotter = Plotter(times, values)

    bluetooth.connect()
    bluetooth.start()
    reader.start()

    try:
        logger.info("Entering main loop.")
        plotter.show()
        while bluetooth.thread.is_alive() or reader.thread.is_alive():
            pass
    except KeyboardInterrupt:
        stopEvent.set()
    finally:
        bluetooth.thread.join()
        bluetooth.socket.close()
        reader.thread.join()


if __name__ == "__main__":
    if "--process" in sys.argv:
        index = sys.argv.index("--process") + 1
        print(f"Processing file {sys.argv[index]}")
        process(sys.argv[index])
    if "--plot" in sys.argv:
        index = sys.argv.index("--plot") + 1
        print(f"Plotting file {sys.argv[index]}")
        plot(sys.argv[index])
    elif len(sys.argv) == 2 and "--no-history" in sys.argv:
        main(saveToFile=False)
    elif len(sys.argv) == 1:
        main(saveToFile=True)
    else:
        print("USAGE:")
        print("Run with real time data from Node: run.sh [--no-history]")
        print("Process stored data: run.sh --process <filename>")
        print("Plot stored data: run.sh --plot <filename>")
