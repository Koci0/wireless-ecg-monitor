
from collections import deque
from typing import Union, List


class Processor:

    minValue = 0
    maxValue = 2800

    def __init__(self, times: Union[List, deque], values: Union[List, deque]):
        self.times = times
        self.values = values

    def getProcessedValue(self, value: int):
        if value >= self.maxValue or value <= self.minValue:
            return None
        return value

    def processValues(self):
        index = 0
        while index < len(self.values):
            if not self.getProcessedValue(self.values[index]):
                self.values.pop(index)
                self.times.pop(index)
            else:
                index += 1
