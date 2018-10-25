

import matplotlib.pyplot as plt
from numpy import poly1d
from scipy import signal
from scipy import *
import matplotlib, sys
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot
import General_aprox as General
import cuentas
import math as m
import cmath
import scipy as sp
from scipy import signal
import numpy as np
from sympy import *

class Bessel(General.General_aprox):
    
    def __init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas,orden, tipo, a):
        
        General.General_aprox.__init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas,orden, tipo, a)
        self.nMinimo=0
        self.nMaximo=15
        self.Ws=ws*a/ws
        self.Wp=wp*a/ws
        self.n=1
        self.ganancia=1
        self.denom=np.poly1d([1])
        self.num=np.poly1d([1])
        self.Transferencia_norm=signal.TransferFunction(1,1)
        self.Transferencia_desnorm=signal.TransferFunction(1,1)
        self.order_calc_Bessel(Ap)
        self.polinomioBessel(self.n)
        self.funcionTransferencia()
        self.s=Symbol('s')
        self.getTransfer()
       
        return;
    def coeficientes_de_Bessel(self,J):
        P=(math.factorial(2*self.n-J))/(2**(self.n-J)*math.factorial(J)*math.factorial(self.n-J))
        return P;
    def order_calc_Bessel(self,Ap):
        if(self.n != None):
            Ns=(5*self.Wp**2)/(self.Ap*math.log(10))
            N=int(Ns)+1        #Se redondea el N para arriba
            if N<self.nMaximo :
                self.n=N    #Se redondea el N para arriba
            else:
                print("Math error:exceso en la capacidad de computo")
                self.n=self.nMaximo
        return;
        #funcion que calcula la totalidad del polinomio de bessel en algebraico
    def polinomioBessel(self,a): 
        s=Symbol('s')
        B1=s+1
        B2=(s**2)+(3*s)+3
        if (a==1):
            B=B1
        elif a==2:
            B=B2
        else:
            B=expand((2*a-1)*self.polinomioBessel(a-1)+(s**2)*self.polinomioBessel(a-2))
        return B
   
    def funcionTransferencia(self): 
        numerador_array=[]
        denom_array=[]
        for k in range (0,self.n + 1):
            if (k==0):
                numerador_array.append(self.coeficientes_de_Bessel(k))   #genera el arreglo del numerador
            denom_array.insert(0,(self.coeficientes_de_Bessel(k)))       #genera el arreglo del denominador
        self.denom=np.poly1d(denom_array)
        self.num=np.poly1d(numerador_array)
        self.Transferencia_norm=signal.TransferFunction(self.num,self.denom)
        #self.Transferencia_desnorm= General_aprox.denormalization(self,type,Wp,n,poles,None,2000,800,8000)
        return;
   
    

    def getTransfer(self):
        return self.Transferencia_norm;


    ##OJO CON ESTO QUE NO ESTA HECHO
    #def n_apropiate_Bessel(self):
    #    default_gain=self.polinomioBessel()(s,0)/self.polinomioBessel(s,self.Wp)      #calculo la ganancia reemplazando en H(S)
    #    if (default_gain>self.Ap):
    #        self.n=self.n+1
    #    return;
   
if __name__ == "__main__":
    print("holanda")
    ex1= Bessel(3,10,1000,2000,None,None,None,None,None,"LP",1)
    ex = ex1.getTransfer()
 
    w,mag,phase = signal.bode(ex, None, 10000)
    pyplot.semilogx(w,mag)
    pyplot.show()
