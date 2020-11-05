import fir_filter as fir
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

data = np.loadtxt("shortecg.dat")
fs = 250

plt.figure(1)
tplot = plt.plot(data)

dataf = np.fft.fft(data)
#Convert FFT data to decibels relative to full scale (dBFS)
datafdB = 20*np.log10(abs(dataf)*2/len(dataf)/(pow(2,15)-1))

#Create frequency axis
f = np.linspace(0, fs, len(dataf))

#Plot sample in frequency domain
plt.figure(2)
fplot = plt.plot(f, datafdB)
fplot = plt.xlabel("Frequency (Hz)")
fplot = plt.ylabel("dBFS")
plt.xscale("log")

M = fs*2

#Bandstop markers

k1 = int(45/fs * M)
k2 = int(55/fs * M)

#Filter function before bandstop
y = np.ones(M)

#Filter function with bandstop
y[k1:k2+1] = 0
y[M-k2:M-k1+1] = 0

k1 = int(0/fs * M)
k2 = int(0.5/fs * M)

y[k1:k2+1] = 0
y[M-k2:M-k1+1] = 0

y = np.fft.ifft(y)
y = np.real(y)

h = np.zeros(M)
h[0:int(M/2)] = y[int(M/2):M]
h[int(M/2):M] = y[0:int(M/2)]

h = h * np.hamming(M)

plt.figure(3)
tplot = plt.plot(h)

filter = fir.FIR_filter(h)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

dataf = np.fft.fft(data)
datafdB = 20*np.log10(abs(dataf)*2/len(dataf)/(pow(2,15)-1))

plt.figure(4)
fplot = plt.plot(f, datafdB)
fplot = plt.xlabel("Frequency (Hz)")
fplot = plt.ylabel("dBFS")
plt.xscale("log")

plt.figure(5)
tplot = plt.plot(data)


plt.show()