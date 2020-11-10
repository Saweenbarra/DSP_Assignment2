import fir_filter as fir
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signalpu
from ecg_gudb_database import GUDb

subject_number = 9
experiment = 'walking'

#import data set for analysis
ecg_class = GUDb(subject_number, experiment)
data = ecg_class.einthoven_II
fs = ecg_class.fs

#importing data to create template from
template_data = np.loadtxt("shortecg.dat")
template_fs = 250

#producing indices for bandstop filter
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

#apply windowing function to impulse response
h = h * np.hamming(M)

#filter the template for 50Hz and DC
filter = fir.FIR_filter(h)
for i in range(len(template_data)):
    template_data[i] = filter.dofilter(template_data[i])
    
#filter the data for 50Hz and DC
filter = fir.FIR_filter(h)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

#take slice of data to use as template
template_data = template_data[650:850]
#reverse the data
template_data = template_data[::-1]

#filter data using the template data
filter = fir.FIR_filter(template_data)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

#square data to improve signal to noise ratio
data *= data

#find peaks in the filtered data 
peaks = np.where(data[M:] > np.max(data[M:])*0.35)
#remove peaks that are within 10 positions of each other
peaks = np.delete(peaks, np.argwhere(np.ediff1d(peaks) <= 10) + 1)
peakstime = []
hrate = []

#process peaks to find the time of each peak
for i in range(len(peaks)):
    peakstime.append(float(peaks[i]/fs))

#find the instantaneous heart rate using the time between each peek 
for i in range(len(peakstime)-1):
    hrate.append(60/(peakstime[i+1] - peakstime[i]))

plt.figure(1)
Hplot = plt.plot(peakstime[:-1],hrate)
plt.show()
