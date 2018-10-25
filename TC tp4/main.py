import General_aprox

import Butterworth
import scipy as sp
from scipy import signal
import math
import numpy
import sympy

import matplotlib 
matplotlib.use('TkAgg')
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.pyplot import plot,xscale,show
import cuentas as cuentas
import Transfer_Maker 

test=Butterworth.Butterworth(20,0.5,1000,2000,0,0,0,0,2,"LP",0)
x=sympy.Symbol('x')
test.get_denormalize_roots((test.Transferencia_desnorm))
#print(test.polos)
#print(test.zeros)
#a=(numpy.poly1d(test.Transferencia_desnorm.num))
#print(a)
#b=(numpy.poly1d(test.Transferencia_desnorm.den))
#print(b)
#print(test.polos,"raciessss")
#print(numpy.roots(b),"raices denom")
#print(sympy.Poly(a,x).all_coeffs(),"asfasdasdsaf")
#print(sympy.Poly(b,x).all_coeffs(),"asfasdasdsafasdfffff")

#prueba=Transfer_Maker.Transfer_Maker(test.zeros,test.polos)
#print(prueba.Transferencias_de_polos,"transferencias de los polos" )
#print(prueba.Media_TransfersDeZeros,"transferencias de los zeros")


######################## PRUEBAS TRANSFER MAKER ################################
## con el de aca es como tengo que hacer para que me quede los ceros y polos
#a=(test.separar_a_ordenes_menores(numpy.roots(b)))
#print(a,"separar ordenes")
#print(a,"el de butter")
#print(prueba.polos_separados,"el de transfer maker")

#a=(test.armar_transferencias(a))



#print(a," transferencias de butter")
#print(prueba.Media_TransferDePolos, "el de tfm")
######################## PRUEBAS TRANSFER MAKER ################################



#print(" ")
#print(test.separar_a_ordenes_menores(test.zeros))

#print(test.armar_transferencias(a))

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