import General_aprox as General
import cuentas
import math as m
import cmath
import scipy as sp
from scipy import signal
import numpy as np
import sympy as symp

class Butterworth(General.General_aprox):
    def __init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas,orden, tipo, a):
        
        General.General_aprox.__init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas,orden, tipo, a)
        self.nMinimo=0
        self.nMaximo=25
        self.epsilon=1
        self.ganancia=1
        self.zeros=[]
        self.polos=[]
        self.testeador=[]
        self.denom=np.poly1d([1])
        self.num=np.poly1d([1])
        self.Transferencia_norm=1
        self.Transferencia_desnorm=1
        self.epButter()
        self.nButter()
        self.polosButter()
        self.funcionTransferencia()
        self.Q=[]
        self.qmax=1
        self.calcular_q()
       # self.conseguir_polos_por_separado()
        #self.testeador=self.cons
       
        return;

    def epButter(self):
        self.epsilon=m.sqrt((10**(self.Ap/10))-1)
        return;

    def nButter(self):  #me fijo que el n que se ingreso es valido sino lo cambio
        
        control=m.ceil(m.log10((m.sqrt((10**(self.As/10))-1)/self.epsilon))/m.log10(self.wsn))
        
        if(self.n < control):
            self.n=control
        elif(self.n > self.nMaximo):
            self.n =self.nMaximo
         
        return;

    def polosButter(self):
        r0=1
        raiz=1
        for k in range(1,self.n+1):
            raiz=r0*(-np.sin(np.pi*(2*k-1)/(2*self.n))+1j*np.cos(np.pi*(2*k-1)/(2*self.n)))
            if(np.real(raiz) < 0.0000000001):
                self.polos.append(raiz)
                poli=np.poly1d([-1/raiz,1])
                self.denom=self.denom*poli
       
               
       
       

    def funcionTransferencia(self):
        #self.Transferencia_norm=signal.TransferFunction(self.num,self.denom) 
        #self.denom=np.poly1d([1])

        #para hallar el factor necesario al cual multiplicar el wn
        if (self.tipo == "LP"):
            wc = self.wp /(self.epsilon**(1/self.n))
        elif(self.tipo == "HP"):
            wc=self.wp*(self.epsilon**(1/self.n))

        self.Transferencia_desnorm=self.denormalization(self.tipo,wc,self.n,self.polos)
      
        return;
 

    def calcular_q(self):
        for i in range (0,len(self.polos)):
            modulo=np.abs(self.polos[i])
            qaux=(modulo/(-2*np.real((self.polos[i]))))
            self.Q.append(qaux)
            self.Q.sort()
            self.qmax=self.Q[len(self.Q)-1]
      
        return;


                
   




