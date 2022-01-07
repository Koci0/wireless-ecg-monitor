
from typing import Union


class Processor:

    minValue = 40
    maxValue = 4055

    alpha = 0.3
    previousEma = 0

    def __init__(self, processedData: dict):
        self.processedData = processedData

    def getProcessedValue(self, value: int) -> Union[None, float]:
        value = self._getInRangeValue(value)
        if not value:
            return None
        value = self._getExponentialMovingAverageValue(value)
        value = self._getNormalizedValue(value)
        return value

    def processValues(self):
        keysToDelete = list()
        for time, value in self.processedData.items():
            processedValue = self.getProcessedValue(value)
            if processedValue:
                self.processedData[time] = processedValue
            else:
                keysToDelete.append(time)

        for key in keysToDelete:
            del self.processedData[key]

    def _getInRangeValue(self, value: int) -> Union[None, int]:
        if self.minValue <= value <= self.maxValue:
            return value
        return None

    def _getExponentialMovingAverageValue(self, value: int) -> float:
        if not self.previousEma:
            self.previousEma = value
            return value
        else:
            currentEma = self.alpha * value + \
                (1 - self.alpha) * self.previousEma
            self.previousEma = currentEma
            return currentEma

    def _getNormalizedValue(self, value) -> Union[None, float]:
        return (value * 3.3) / 4096
