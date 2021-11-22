
from collections import deque
from typing import Union, List


class Processor:

    minValue = 0
    maxValue = 2800

    def __init__(self, times: Union[List, deque], values: Union[List, deque]):
        self.times = times
        self.values = values

    def getProcessedValue(self, value: int) -> Union[None, float]:
        value = self._getInRangeValue(value)
        if not value:
            return None
        value = self._getNormalizedValue(value)
        return value

    def processValues(self):
        index = 0
        while index < len(self.values):
            value = self.getProcessedValue(self.values[index])
            if value:
                self.values[index] = value
                index += 1
            else:
                self.times.remove(self.times[index])
                self.values.remove(self.values[index])

    def _getInRangeValue(self, value: int) -> Union[None, int]:
        if self.minValue <= value <= self.maxValue:
            return value
        return None

    def _getNormalizedValue(self, value: int) -> Union[None, float]:
        return (value * 3.3) / 4096
