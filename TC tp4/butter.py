import math as m
from math import pi,ceil,sqrt
from cmath import exp 
from decimal import *   
from numpy.polynomial import polynomial as poly
import numpy as np
import sympy as sp


import matplotlib 
matplotlib.use('TkAgg')
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.pyplot import plot,xscale,show
import cuentas as cuentas

Ap=3  #banda pasante
As=20   #banda atenuada
wp=1000
ws=2000



def Butterworthaprox(self):
    self.zeros=[]
    self.polos=[]
    self.epButter()
    self.nButter()
    self.polosButter()
    return;
    
ep=m.sqrt((10**(Ap/10))-1)
n=m.ceil(m.log10((m.sqrt((10**(As/10))-1)/ep))/m.log10(ws/wp))

modulo=1/(ep**(1/n))
poles=[]
polos=[]
sk=[]
#symbols = []
a=sp.Symbol("a",real=True)
s = sp.Symbol("s",imag=True)

#print(expand(h))
h=1

ganancia=1

for k in range(1,n+1):
     polo=modulo*exp(1j * (2 * k + n - 1) * (pi / (2 * n)))
     re=Decimal(polo.real)
     imaginario=Decimal(polo.imag)
     if(polo.real < 0):
         sk.append(polo)
         ganancia=ganancia*np.abs(polo)
     
print(ganancia)     
for i in range (len(sk)):
    #print(s-sk[i],sk[i])
    h=h*((s/sk[i])-1)*sk[i]
    

#print(sp.expand(h))
test=cuentas.conseguir_tf(1/h,s)
w,mag,phase = signal.bode(test)

print (test)


xscale('log')
plot(w/(2*pi),mag)
show()



# print(num)
# print(denom)


#tuvieja = signal.TransferFunction(test[0],test[1])


#np.roots(test)
#     print(poles[i]["symbol"],poles[i]["value"])

