import fir_filter as fir
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("shortecg.dat")
fs = 250
time = np.linspace(0,len(data)*1/fs,len(data))

plt.subplot(2,1,1)
plt.plot(time,data)
plt.title("Original ECG")
plt.xlabel("Time (s)")
plt.ylabel("Volts (V)")

M = fs*2
y = np.ones(M)

#Indexes corresponding to 45Hz and 55Hz
k1 = int(45/fs * M)
k2 = int(55/fs * M)

#Set range of 45Hz to 55Hz to 0, and nyquist mirror image
y[k1:k2+1] = 0
y[M-k2:M-k1+1] = 0

#Indexes corresponding to 0Hz and 0.5Hz
k1 = int(0/fs * M)
k2 = int(0.5/fs * M)

#Set range of 0Hz to 0.5Hz to 0, and nyquist mirror image
y[k1:k2+1] = 0
y[M-k2:M-k1+1] = 0

#Take FFT of transfer function
y = np.fft.ifft(y)
y = np.real(y)

#Swap FFT around data to obtain impulse response
h = np.zeros(M)
h[0:int(M/2)] = y[int(M/2):M]
h[int(M/2):M] = y[0:int(M/2)]

h = h * np.hamming(M)

filter = fir.FIR_filter(h)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

plt.subplot(2,1,2)
plt.plot(time,data)
plt.title("ECG Filtered")
plt.xlabel("Time (s)")
plt.ylabel("Volts (V)")
plt.subplots_adjust(hspace = 0.7)

plt.show()