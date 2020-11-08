import numpy as np

def unittest():
    mockData = np.random.rand(10)
    mockCoeff = np.random.rand(10)
    buffer = np.zeros(10)
    filter = FIR_filter(mockCoeff)
    successCounter = 0
    for i in range(len(mockData)):
        sum = 0
        j = len(mockData) - 1
        buffer[0] = mockData[i]
        test = filter.dofilter(buffer[0])
        for index in range(len(buffer)):
            sum += buffer[index] * mockCoeff[index]
        while(j>0):
            buffer[j] = buffer[j-1]
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
    #Constructor saves the coefficients, creates a ring buffer, and initialises the offset
    def __init__(self,_coefficients):
        self._coefficients = _coefficients
        self.ringBuffer = np.zeros(len(self._coefficients))
        self.offset = 0
    
    def dofilter(self,v):
        self.ringBuffer[self.offset] = v
        self.sum = 0
        coef_index = 0
        buff_index = self.offset

        #While travelling down the ring buffer from the offset, travel up the coefficient array from 0
        #Multiplying the values and summing them accumulatively
        while(buff_index >= 0):
            self.sum += self.ringBuffer[buff_index] * self._coefficients[coef_index]
            buff_index -= 1
            coef_index += 1
        
        #Set buff_index to top of ringBuffer
        buff_index = len(self.ringBuffer)-1

        #Continue this process until all taps have been accounted for
        while(coef_index < len(self._coefficients) - 1):
            self.sum += self.ringBuffer[buff_index] * self._coefficients[coef_index]
            buff_index -= 1
            coef_index += 1

        #Increment offset or set to zero if beyond length of the ringBuffer
        if self.offset < len(self.ringBuffer)-1:
            self.offset += 1
        else:
            self.offset = 0
        
        return self.sum

if __name__ == "__main__":
    unittest()
