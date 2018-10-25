

from numpy import poly1d
from scipy import signal
from scipy import *


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
        
        General.General_aprox.__init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas,orden, tipo, tretraso)
        self.nMinimo=0
        self.nMaximo=25
        self.Ws=ws*tretraso
        self.Wp=wp*tretraso
        self.n=1
        self.ganancia=1
        self.denom=np.poly1d([1])
        self.num=np.poly1d([1])
        self.Transferencia_norm=1
        self.Transferencia_desnorm=1
        self.order_calc_Bessel()
        self.n_apropiate_Bessel()
        self.polinomioBessel()
        self.coeficientes_de_Bessel()
        self.funcionTransferencia()
        self.s=Symbol('s')
       
        return;

    def order_calc_Bessel(self):
        Ns=(5*Wp**2)/(ap*math.log(10))
        N=int(Ns)+1        #Se redondea el N para arriba
        if N<self.nMaximo :
            self.n=int(Ns)+1        #Se redondea el N para arriba
        else:
            self.n=self.nMaximo
        return;
        #funcion que calcula la totalidad del polinomio de bessel en algebraico
    def polinomioBessel(self): 
        s=Symbol('s')
        B1=s+1
        B2=(s**2)+(3*s)+3
        if (N==1):
            B=B1
        elif N==2:
            B=B2
        else:
            B=expand ( (2*N-1)*polinomioBessel(N-1)+(s**2)*polinomioBessel(N-2))
        return B
    def coeficientes_de_Bessel(self,i):
        P=(math.factorial(2*self.n-i))/(2**(self.n-i)*math.factorial(i)*math.factorial(self.n-i))
        return P
    def funcionTransferencia(self): 
        numerador_array=[]
        denom_array=[]
        for k in range (0,self.n + 1):
            if (k==0):
                numerador_array.append(coeficientes_de_Bessel(k))   #genera el arreglo del numerador
            denom_array.insert(0,(coeficientes_de_Bessel(k)))       #genera el arreglo del denominador
            self.denom=np.poly1d(denom_array)
            self.num=np.poly1d(numerador_array)
            self.Transferencia_norm=signal.TransferFunction(self.num,self.denom)
        return;
    def n_apropiate_Bessel(self):
        default_gain=polinomioBessel()(s,0)/polinomioBessel(s,self.Wp)      #calculo la ganancia reemplazando en H(S)
        if (default_gain>self.Ap):
            self.n=self.n+1
        return;

