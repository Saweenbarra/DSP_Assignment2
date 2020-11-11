import numpy as np

def unittest():
    #Generate mock data and mock coefficients
    mockData = np.arange(1,9)
    mockCoeff = np.arange(1,9)

    #Empty array for output test to go in
    test = np.zeros(len(mockData))

    #Perform dofilter function on mock variables
    filter = FIR_filter(mockCoeff)
    for i in range(len(mockData)):
        test[i] = filter.dofilter(mockData[i])
        print(test[i])
    #Correct answers are 1,4,10,20,35,56,84,120
    print("Expected: 1, 4, 10, 20, 35, 56, 84, 120")
    


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