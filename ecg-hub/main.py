
from modules.bluetooth import Bluetooth
from modules.plotter import Plotter
from modules.reader import Reader

from collections import deque
from threading import Event
from queue import Queue

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


maxPointsOnPlot = 100


def main():
    times = deque(maxlen=maxPointsOnPlot)
    values = deque(maxlen=maxPointsOnPlot)
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
    main()
