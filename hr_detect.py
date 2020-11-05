import fir_filter as fir
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signalpu
from ecg_gudb_database import GUDb

subject_number = 9
experiment = 'walking'

ecg_class = GUDb(subject_number, experiment)

data = ecg_class.einthoven_II
fs = ecg_class.fs

plt.figure(1)
tplot = plt.plot(ecg_class.t, data)


M = fs*2

k1 = int(45/fs * M)
k2 = int(55/fs * M)

#Filter function before bandstop
y = np.ones(M)

#Filter function with bandstop
y[k1:k2+1] = 0
y[M-k2:M-k1+1] = 0

k1 = int(0/fs * M)
k2 = int(4/fs * M)

y[k1:k2+1] = 0
y[M-k2:M-k1+1] = 0

y = np.fft.ifft(y)
y = np.real(y)

h = np.zeros(M)
h[0:int(M/2)] = y[int(M/2):M]
h[int(M/2):M] = y[0:int(M/2)]

h = h * np.hamming(M)
filter = fir.FIR_filter(h)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

plt.figure(2)
fplot = plt.plot(ecg_class.t, data)
plt.show()
