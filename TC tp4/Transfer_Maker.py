import cuentas
import math as m
import cmath
import scipy as sp
from scipy import signal
import numpy as np
import sympy as symp

class Transfer_Maker(object):
     #"""clase que se ocupa de generar las distintas funciones transferencias de orden 2 y 1 tanto para los zeros y los polos guardandolas en listas distintas"""
     #pasarle los polos y ceros desnormalizados 
    def __init__(self, polos_, zeros_ ):

        self.polos=polos_
        self.zeros=zeros_
        self.norma_polos=[]
        self.norma_zeros=[]
        self.polos_separados=self.separar_a_ordenes_menores(self.polos,self.norma_polos)
        self.zeros_separados=self.separar_a_ordenes_menores(self.zeros,self.norma_zeros)
        #paso intermedio para obtener las transferencias METER DESPUES EN OTRA FUNCION
        self.Media_TransfersDeZeros=self.armar_transferencias(self.zeros_separados)
        self.Media_TransferDePolos=self.armar_transferencias(self.polos_separados)
        ##########################################
        self.Transferencias_de_polos=[]
        self.Transferencias_de_zeros=[]
        self.crear_transferencias_polos(self.Media_TransferDePolos)
        self.crear_transferencias_zeros(self.Media_TransfersDeZeros)
        




        return;
   
    def separar_a_ordenes_menores(self,raices,norma_raices):
        ##me devuelve un arreglo con todos los raices sacandoles las conjugadas 
        aux=[]
        test=0
        #print(raices,"asdasdasdassdasdadsasd")
        if (len(raices) == 0):
            return aux;
        else:
            for i in range(0,len(raices)):
                if(np.abs(np.imag(raices[i])) < 1e-6):
                    aux.append(np.real(raices[i])) #para polos con parte iimagianaria igual a 0
                    norma_raices.append(np.abs(np.real(raices[i])))
                    #print(np.abs(np.real(raices[i])),"que salesdsad")
                else:
                    #test=(cmath.polar((np.conjugate(self.polos[i]))))
                    #control=self.polos[i]
                    for j in range (i+1,len(raices)):
                        compR1=np.abs(np.real(raices[i]))
                        compR2=np.abs(np.real(raices[j]))
                        compIm1=np.abs(np.imag(raices[i]))
                        compIm2=np.abs(np.imag(raices[j]))
                        #comparar las partes reales
                        if(cuentas.comparar(compR1,compR2)):
                            if(cuentas.comparar(compIm1,compIm2)):
                                aux.append(raices[i])
                                #test=cmath.polar(raices[j])
                                norma_raices.append(np.abs(raices[i]))
                                #print("raices[j]",test[0] )
                               # print(np.abs(raices[j]),"que sale")

                     #   b=(cmath.polar(self.polos[j]))
                        #if ((np.abs(self.polos[i]) ) == (np.abs(self.polos[j]))):
                        #    if( (cmath.phase(self.polos[i])) == (-1*cmath.phase(self.polos[j])) ):
        print(aux,"tu vieja")
        return aux;

    def armar_transferencias(self, raices):
        ##devuelve un arreglo donde se encuentran las raices de los distintos polinomios de orden 1 y 2 
        coef_de_transferencias=[]
        if(len(raices) == 0):
            return coef_de_transferencias;
        else:
            for i in range(0,len(raices)):
                a=raices[i]
                if((np.abs(np.imag(raices[i]))) < 1e-6):
                    coef_de_transferencias.append([raices[i]])
                else:
                    aux=[raices[i],np.conjugate(raices[i])]
                    coef_de_transferencias.append(aux)
        return coef_de_transferencias;

    def crear_transferencias_polos(self,lista_con_raices):
        ## crea las transfer fuction y las meten a una lista
        ##capaz se puede hacer de otra forma
        denom=1
        num=np.poly1d([1])
        print(num)
        ##para los polos

        for i in range(0,len(lista_con_raices)):
            
           # for j in range(0,len(lista_con_raices[i])):
            denom=np.poly(lista_con_raices[i])
            if(len(lista_con_raices[i]) == 2 ):
                num=np.poly1d([(self.norma_polos[i]**2)])
            elif(len(lista_con_raices[i]) == 1 ):
                num=np.poly1d([(self.norma_polos[i])])

                #poli=np.poly1d([1/lista_con_raices[i][j]],-1)
                #denom=denom*poli
            self.Transferencias_de_polos.append(signal.TransferFunction(num,denom))
                  
        #print(self.Transferencias_de_polos)
        return;
    def crear_transferencias_zeros(self,lista_con_raices):
        
        denom=np.poly1d([1])
        num=1
        if(len(lista_con_raices) == 0):
            denom=np.poly1d([1])
            num=np.poly1d([1])
            self.Transferencias_de_zeros.append(signal.TransferFunction(num,denom))
            
        ##para los polos zeros
        else:
            for i in range(0,len(lista_con_raices)):
                for j in range(0,len(lista_con_raices[i])):
                    poli=np.poly1d([1,-1*lista_con_raices[i][j]])
                    num=num*poli
                self.Transferencias_de_zeros.append(signal.TransferFunction(num,denom))
        
        return;
       
        
                


            


            
                   


