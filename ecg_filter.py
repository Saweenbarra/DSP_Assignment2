fir = __import__("fir-filter")
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

data = np.loadtxt("shortecg.dat")
fs = 500

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

'''
n = np.arange(-200, 200+1)

#Impulse response of a band stop filter between 20Hz and 120Hz https://youtu.be/Z0Vxuo1c5yY?t=1627
h = (1/(n*np.pi)) * (np.sin(20/500*2*np.pi*n) - np.sin(120/500*2*np.pi*n))
#L'hopitals rule - to avoid diving by 0 causing NaN error
h[200] = 1 - (55/500*2*np.pi - 45/500*2*np.pi)/np.pi

plt.figure(2)
tplot = plt.plot(h)
'''
# https://www.youtube.com/watch?v=mvlxm8Jzlk4&list=PLxWwb-b9LnpCtqVTaACY_U28EheNGtk_r&index=9
M = fs*3

#Bandstop markers
k1 = int(25/fs * M)
k2 = int(120/fs * M)

#Filter function before bandstop
y = np.ones(M)

#Filter function with bandstop
y[0] = 0
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