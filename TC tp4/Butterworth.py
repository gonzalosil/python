import General_aprox as General
import cuentas
import math as m
import cmath
import scipy as sp
from scipy import signal
import numpy as np
import sympy as symp

class Butterworth(General.General_aprox):
    def __init__(self, As, Ap, wp, ws, tipo, orden=None, Q=None, a=None, wpMenos=None,wpMas=None, wsMenos=None, wsMas=None):

        General.General_aprox.__init__(self, As, Ap, wp, ws, tipo, orden, a, wpMenos,wpMas, wsMenos, wsMas)
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
        self.Transferencia_desnorm = signal.TransferFunction([1],[1])
        self.epButter()
        self.nButter()

        while 1:
            self.polosButter()
            self.funcionTransferencia()
            self.Q=[]
            self.qmax=0
            self.get_denormalize_roots(self.Transferencia_desnorm)
            self.calcular_q(self.Transferencia_desnorm.poles)
            print(self.Transferencia_desnorm.poles)
            if Q != None: 
                if self.qmax > Q:
                    if self.n > 1:
                        self.n = self.n-1
                        self.Q.clear()
                        self.polos.clear()
                        self.zeros.clear()
                    else:
                        break
                    
                else:
                    break
            else:
                break
        if tipo == "BP":
            self.Transferencia_desnorm._num = self.Transferencia_desnorm._num*(3.3333333333333333333333/(Ap+(1/As)))
       # self.conseguir_polos_por_separado()
        #self.testeador=self.cons
       
        return;

    def epButter(self):
        self.epsilon=m.sqrt((10**(self.Ap/10))-1)
        return;

    def nButter(self):  #me fijo que el n que se ingreso es valido sino lo cambio
        
        control=m.ceil(m.log10((m.sqrt((10**(self.As/10))-1)/self.epsilon))/m.log10(self.wsn))
        if self.n != None:
            if(self.n < control):
                self.n=control
            elif(self.n > self.nMaximo):
                self.n =self.nMaximo
        else:
            self.n=control

         
        return;

    def polosButter(self):
        r0=1/((self.epsilon)**(1/self.n))
        raiz=1
        for k in range(1,self.n+1):
            raiz=r0*(-np.sin(np.pi*(2*k-1)/(2*self.n))+1j*np.cos(np.pi*(2*k-1)/(2*self.n)))
            if(np.real(raiz) < 0.0000000001):
                self.polos.append(raiz)
                poli=np.poly1d([-1/raiz,1])
                self.denom=self.denom*poli
       
               
       
       

    def funcionTransferencia(self):
        self.Transferencia_norm=signal.TransferFunction(self.num,self.denom) 
        
        self.denom=np.poly1d([1])
        if(self.tipo == "LP"):
            wc = self.wp #/(self.epsilon**(1/self.n))
        elif(self.tipo == "HP"):
            wc = self.wp
           #* (self.epsilon**(1/self.n))
        else:
            wc=self.wpMenos
       #poles=None, zeros=None, Wpmas=None, Wamenos=None, Wamas=None)
        self.Transferencia_desnorm=self.denormalization(self.tipo,wc,self.n,self.polos,None,self.wpMas,self.wsMenos,self.wsMas)
        
  
        return;

    #agregar a general aprox
    #def calcular_q(self):
    #    for i in range (0,len(self.polos)):
    #        modulo=np.abs(self.polos[i])
    #        qaux=(modulo/(-2*np.real((self.polos[i]))))
    #        self.Q.append(qaux)
    #        self.Q.sort()
    #        self.qmax=self.Q[(len(self.Q)-1)]
    #    return;

    def get_transfer(self):
        return self.Transferencia_desnorm


    ##
    def separar_a_ordenes_menores(self,raices):
        ##me devuelve un arreglo con todos los raices sacandoles las conjugadas 
        aux=[]
        test=0
        
        if (len(raices) == 0):
            return aux;
        else:
            for i in range(0,len(raices)):
                if(np.abs(np.imag(raices[i])) < 1e-6):
                    aux.append(raices[i]) #para polos con parte iimagianaria igual a 0
                else:
                    for j in range (i+1,len(raices)):
                        compR1=np.abs(np.real(raices[i]))
                        compR2=np.abs(np.real(raices[j]))
                        compIm1=np.abs(np.imag(raices[i]))
                        compIm2=np.abs(np.imag(raices[j]))
                        #comparar las partes reales
                        if(cuentas.comparar(compR1,compR2)):
                            if(cuentas.comparar(compIm1,compIm2)):
                                aux.append(raices[i])

                    

            return aux;

    def armar_transferencias(self, raices):
        ##devuelve un arreglo donde se encuentran las raices de los distintos polinomios de orden 1 y 2 
        coef_de_transferencias=[]
        for i in range(0,len(raices)):
            a=raices[i]
            if((np.abs(np.imag(raices[i]))) < 1e-6):
                coef_de_transferencias.append(raices[i])
            else:
                aux=[raices[i],np.conjugate(raices[i])]
                coef_de_transferencias.append(aux)

        return coef_de_transferencias;

                


        


                        
   


                




    
