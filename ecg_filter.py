fir = __import__("fir-filter")
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

data = np.loadtxt("shortecg.dat")
fs = 500

plt.figure(1)
tplot = plt.plot(data)


n = np.arange(-200, 200+1)

#Impulse response of a band stop filter between 45Hz and 55Hz https://youtu.be/Z0Vxuo1c5yY?t=1627
h = (1/(n*np.pi)) * (np.sin(45/500*2*np.pi*n) - np.sin(55/500*2*np.pi*n))
#L'hopitals rule - to avoid diving by 0 causing NaN error
h[200] = 1 - (55/500*2*np.pi - 45/500*2*np.pi)/np.pi

plt.figure(2)
tplot = plt.plot(h)
'''
filter = fir.FIR_filter(h)
for i in range(len(data)):
    data[i] = filter.dofilter(data[i])

plt.figure(3)
tplot = plt.plot(data)
'''
plt.figure(4)
y = signal.lfilter(h,1,data)
tplot = plt.plot(y)

plt.show()