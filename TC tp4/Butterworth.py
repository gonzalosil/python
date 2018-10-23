import General_aprox as General
import cuentas
import math as m
import cmath
import scipy as sp
from scipy import signal
import numpy as np
import sympy as symp

class Butterworth(General.General_aprox):
    def __init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas, tipo, a):
        
        General.General_aprox.__init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas, tipo, a)
        self.n=0
        self.epsilon=1
        self.ganancia=1
        self.zeros=[]
        self.polos=[]
        self.denom=np.poly1d([1])
        self.num=np.poly1d([1])
        self.Transferencia_norm=1
        self.Transferencia_desnorm=1
        self.epButter()
        self.nButter()
        self.polosButter()
        
        
        self.funcionTransferencia()

       
        return;

    def epButter(self):
        self.epsilon=m.sqrt((10**(self.Ap/10))-1)
        return;

    def nButter(self):
        self.n=m.ceil(m.log10((m.sqrt((10**(self.As/10))-1)/self.epsilon))/m.log10(self.wsn))
        print(self.n)
        return;

    def polosButter(self):
        r0=1
        raiz=1
        for k in range(1,self.n+1):
            raiz=r0*(-np.sin(np.pi*(2*k-1)/(2*self.n))+1j*np.cos(np.pi*(2*k-1)/(2*self.n)))
            if(np.real(raiz) < 0.0000000001):
                self.polos.append(raiz)
                poli=np.poly1d([-1/raiz,1])
                print(poli,"polo",k)
                self.denom=self.denom*poli
        print(self.denom)
               
       
       

    def funcionTransferencia(self):
        self.Transferencia_norm=signal.TransferFunction(self.num,self.denom) 
        print(self.Transferencia_norm)
        self.denom=np.poly1d([1])
        wc = self.wp /(self.epsilon**(1/self.n))
        for i in range(0,len(self.polos)):
            #poli=np.poly1d([-self.polos[i],wc])
            poli=np.poly1d([(1/wc),-self.polos[i]])           #pasabajos
            self.denom=self.denom*poli
        
        #poli_denor=np.poly1d([1,0])
        #self.denom=self.denom*poli_denor
        #self.num=self.num*poli_denor
        #print("aca viene el arreglo flashero")
        self.Transferencia_desnorm=signal.TransferFunction(self.num,self.denom)
 #       self.Transferencia=sp.signal.zpk2tf(self.zeros,self.polos,1)
        #print(self.Transferencia)






