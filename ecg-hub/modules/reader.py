
import sys

from collections import deque
from datetime import date
from queue import Queue, Empty
from threading import Event, Thread

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

filename = f"data_{date.today()}.dat"


class Reader:

    def __init__(self, stopEvent: Event, dataQueue: Queue, times: deque, values: deque):
        self.stopEvent = stopEvent
        self.dataQueue = dataQueue
        self.times = times
        self.values = values

        self.thread = Thread(target=self.readFromQueue)

        self.file = open(filename, "w")
        if not self.file:
            logger.error("Failed to open file, abort!")
            sys.exit(1)

    def start(self):
        logger.info("Thread starting.")
        self.thread.start()

    def stop(self):
        logger.info("Thread stopping.")
        self.thread.join()
        self.file.close()

    def readFromQueue(self):
        while not self.stopEvent.is_set():
            try:
                raw_data = self.dataQueue.get_nowait()
                time, isLeadDisconnected, value = int.from_bytes(raw_data[0:4], "big"), int.from_bytes(
                    raw_data[4:6], "big"), int.from_bytes(raw_data[6:8], "big")
                if not isLeadDisconnected:
                    self.times.append(time)
                    self.values.append(value)

                    self.file.write(f"{time} {value}\n")
            except Empty:
                pass
