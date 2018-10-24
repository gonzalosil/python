import General_aprox

import Butterworth
import scipy as sp
from scipy import signal
import math

import matplotlib 
matplotlib.use('TkAgg')
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.pyplot import plot,xscale,show
import cuentas as cuentas

test=Butterworth.Butterworth(20,0.5,1000,2000,0,0,0,0,2,"LP",0)

print(test.polos)



#w, mag, phase = sp.signal.bode(test.Transferencia_desnorm)
#xscale('log')
#plot(w,mag)
#show()

#wachin=test.conseguir_polos_por_separado()
#print(wachin)
#from scipy import signal
#import matplotlib.pyplot as plt
#import numpy as np

#b, a = signal.butter(5, 1000, 'low', analog=True)
#w, h = signal.freqs(b, a)
#plt.plot(w, 20 * np.log10(abs(h)))
#plt.xscale('log')
#plt.title('Butterworth filter frequency response')
#plt.xlabel('Frequency [radians / second]')
#plt.ylabel('Amplitude [dB]')
#plt.margins(0, 0.1)
#plt.grid(which='both', axis='both')
#plt.axvline(100, color='green') # cutoff frequency
#plt.show()