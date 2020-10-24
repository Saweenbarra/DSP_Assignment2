import numpy as np

class FIR_filter:

    def __init__(self,_coefficients):
        self._coefficients = _coefficients
        self.ringBuffer = np.zeros(len(self._coefficients))
        self.offset = 0
        
    def dofilter(self,v):
        self.ringBuffer[self.offset] = v
        self.sum = 0
        coef_index = 0
        buff_index = self.offset

        while(buff_index >= 0):
            self.sum += self.ringBuffer[buff_index] * self._coefficients[coef_index]
            buff_index -= 1
            coef_index += 1
        
        buff_index = len(self.ringBuffer)-1

        while(coef_index < len(self._coefficients) - 1):
            self.sum += self.ringBuffer[buff_index] * self._coefficients[coef_index]
            buff_index -= 1
            coef_index += 1

        if self.offset < len(self._coefficients)-1:
            self.offset += 1
        else:
            self.offset = 0
        

        return self.sum