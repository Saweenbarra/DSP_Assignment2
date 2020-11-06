import fir_filter as fir
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signalpu
from ecg_gudb_database import GUDb

subject_number = 9
experiment = 'walking'

ecg_class = GUDb(subject_number, experiment)

template_data = np.loadtxt("shortecg.dat")
template_data *= 100000
template_fs = 250
template_time = np.linspace(0,1/template_fs,len(template_data))
data = ecg_class.einthoven_II
fs = ecg_class.fs

M = fs*2

k1 = int(45/fs * M)
k2 = int(55/fs * M)
k3 = int(0/fs * M)
k4 = int(4/fs * M)

y = np.ones(M)

y[k1:k2+1] = 0
y[M-k2:M-k1+1] = 0
y[k3:k4+1] = 0
y[M-k4:M-k3+1] = 0

y = np.fft.ifft(y)
y = np.real(y)

h = np.zeros(M)
h[0:int(M/2)] = y[int(M/2):M]
h[int(M/2):M] = y[0:int(M/2)]

h = h * np.hamming(M)
filter = fir.FIR_filter(h)
for i in range(len(template_data)):
    template_data[i] = filter.dofilter(template_data[i])
    
filter = fir.FIR_filter(h)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

template_data = template_data[650:850]
template_data = template_data[::-1]

filter = fir.FIR_filter(template_data)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

data *= data
data = data[550:]

plt.figure(1)
plot = plt.plot(data)
plt.show()
