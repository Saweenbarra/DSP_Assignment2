fir = __import__("fir-filter")
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

data = np.loadtxt("shortecg.dat")
fs = 500

plt.figure(1)
tplot = plt.plot(data)


n = np.arange(-200, 200+1)

#Impulse response of a band stop filter between 20Hz and 120Hz https://youtu.be/Z0Vxuo1c5yY?t=1627
h = (1/(n*np.pi)) * (np.sin(20/500*2*np.pi*n) - np.sin(120/500*2*np.pi*n))
#L'hopitals rule - to avoid diving by 0 causing NaN error
h[200] = 1 - (55/500*2*np.pi - 45/500*2*np.pi)/np.pi

plt.figure(2)
tplot = plt.plot(h)

dataf = np.fft.fft(data)
#Convert FFT data to decibels relative to full scale (dBFS)
datafdB = 20*np.log10(abs(dataf)*2/len(dataf)/(pow(2,15)-1))

#Create frequency axis
f = np.linspace(0, fs, len(dataf))

#Plot sample in frequency domain
plt.figure(3)
fplot = plt.plot(f, datafdB)
fplot = plt.xlabel("Frequency (Hz)")
fplot = plt.ylabel("dBFS")
plt.xscale("log")


filter = fir.FIR_filter(h)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

plt.figure(4)
tplot = plt.plot(data)


plt.show()