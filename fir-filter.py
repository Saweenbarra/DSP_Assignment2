import numpy as np

def unittest():
    mockData = np.zeros(10)
    mockCoeff = np.arange(1,11)
    filter = FIR_filter(mockCoeff)
    successCounter = 0
    for i in range(len(mockData)):
        sum = 0
        j = len(mockData) - 1
        mockData[0] = i
        test = filter.dofilter(mockData[0])
        for index in range(len(mockData)):
            sum += mockData[index] * mockCoeff[index]
        while(j>0):
            mockData[j] = mockData[j-1]
            j -= 1
        if test == sum:
            successCounter += 1
            print("Check successful!")
        else:
            print("Check Failed!")
    if successCounter == len(mockData):
        print("All checks were successful, the circular buffer FIR filter method is working")
    else:
        print("At least one check failed, the circular buffer FIR filter method is not working")


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

if __name__ == "__main__":
    unittest()