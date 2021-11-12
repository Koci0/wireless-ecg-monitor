
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

MAX_POINTS_ON_PLOT = 300


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


def main():
    times = deque(maxlen=MAX_POINTS_ON_PLOT)
    values = deque(maxlen=MAX_POINTS_ON_PLOT)
    dataQueue = Queue()
    stopEvent = Event()

    bluetooth = Bluetooth(dataQueue, stopEvent)
    reader = Reader(stopEvent, dataQueue, times, values)
    plotter = Plotter(times, values)

    bluetooth.connect()
    bluetooth.start()
    reader.start()

    try:
        logger.info("Entering main loop.")
        while bluetooth.thread.is_alive() or reader.thread.is_alive():
            plotter.show()
    except KeyboardInterrupt:
        stopEvent.set()
    finally:
        bluetooth.thread.join()
        bluetooth.socket.close()
        reader.thread.join()


if __name__ == "__main__":
    if "--file" in sys.argv and len(sys.argv) == 3:
        print(f"Processing file {sys.argv[2]}")
        process(sys.argv[2])
    elif len(sys.argv) == 1:
        main()
    else:
        print("USAGE:")
        print("Run with real time data from Node: run.sh")
        print("Run for stored data: run.txt --file <filename>")
