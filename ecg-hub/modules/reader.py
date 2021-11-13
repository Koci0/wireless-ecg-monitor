
from modules.processor import Processor

import sys

from collections import deque
from datetime import datetime
from queue import Queue, Empty
from threading import Event, Thread

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

filename = f"data_{datetime.now()}.dat"


class Reader:

    def __init__(self, stopEvent: Event, dataQueue: Queue, times: deque, values: deque, saveToFile: bool = True):
        self.stopEvent = stopEvent
        self.dataQueue = dataQueue
        self.times = times
        self.values = values
        self.startTime = 0
        self.processor = Processor(times, values)
        self.saveToFile = saveToFile

        self.thread = Thread(target=self.readFromQueue)

        if self.saveToFile:
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
        while not self.startTime:
            try:
                raw_data = self.dataQueue.get_nowait()
            except Empty:
                continue
            self.startTime = int.from_bytes(raw_data[0:4], "big")
        logger.info(f"Start time is {self.startTime}")

        while not self.stopEvent.is_set():
            try:
                raw_data = self.dataQueue.get_nowait()
                time, isLeadDisconnected, value = int.from_bytes(raw_data[0:4], "big"), int.from_bytes(
                    raw_data[4:6], "big"), int.from_bytes(raw_data[6:8], "big")
                if not isLeadDisconnected:
                    value = self.processor.getProcessedValue(value)
                    if value:
                        time = (time - self.startTime) / 1000
                        self.times.append(time)
                        self.values.append(value)

                        if self.saveToFile:
                            self.file.write(f"{time} {value}\n")
            except Empty:
                pass
