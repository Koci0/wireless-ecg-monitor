
import modules.const as const
from modules.bluetooth import Bluetooth
from modules.plotter import Plotter
from modules.reader import Reader
from modules.processor import Processor

import sys

from threading import Event
from queue import Queue

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def process(filename: str):
    ecgData = dict()
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            time, value = line.strip('\n').split(" ")
            ecgData[int(time)] = float(value)

    processor = Processor(ecgData)
    processor.processValues()

    with open(f"processed_{filename}", "w") as file:
        for time, value in ecgData.items():
            print(f"{time} {value}")
            file.write(f"{time} {value}\n")


def plot(filename: str):
    ecgData = dict()
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            time, value = line.strip('\n').split(" ")
            ecgData[int(time)] = float(value)

    plotter = Plotter(ecgData)
    plotter.show()


def main(saveToFile: bool = True):
    processedData = dict()
    dataQueue = Queue()
    stopEvent = Event()

    bluetooth = Bluetooth(dataQueue, stopEvent)
    reader = Reader(stopEvent, dataQueue, processedData, saveToFile)
    plotter = Plotter(processedData)

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
    elif "--plot" in sys.argv:
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
