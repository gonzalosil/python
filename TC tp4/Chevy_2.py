import matplotlib, sys
matplotlib.use('TkAgg')
import math as m
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot
from tkinter import *
from tkinter import ttk
import numpy as np
import General_aprox as denorm

class Chevy_2(object):
    def __init__(self, Ap, As, Wp, Ws, type, Wp_mas=None, Ws_mas=None):
                #si se quiere hacer un band pass o un band reject, Wp y Ws se usan como Wp- y Ws-
        e=1/m.sqrt(m.pow(10,As/10)-1)

        if (type == "LP"):
            WsN = Ws/Wp
        elif (type == "HP"):
            WsN = Wp/Ws
        elif (type == "BP"):
            WsN = (Ws_mas-Ws)/(Wp_mas-Wp)
        elif (type == "BR"):
            WsN = (Wp_mas-Wp)/(Ws_mas-Ws)

        n=m.ceil(m.acosh((m.sqrt(m.pow(10,As/10)-1))/(m.sqrt(m.pow(10,Ap/10)-1)))/(m.acosh(WsN)))
       # n=m.ceil(m.acosh((m.sqrt(m.pow(10,As/10)-1))/e)/(m.acosh(WsN)))
        #hallo los polos de chevy
        print("hola mijo")
        alpha = []
        beta = []
        sigma = []
        omega = []
        poles = []
        zeros = []
        self.Q = []
        self.qmax = 0
        
      
        for k in range (0,n):
            alpha.append([(2*(k+1)-1)/(2*n)*m.pi])

        beta.append([1/n*m.asinh(1/e)])
        beta.append([-1/n*m.asinh(1/e)])

       # print(beta[0][0])
        for k in range (0,n):
            if m.sin(alpha[k][0])*m.sinh(beta[0][0]) < 0: #tomo solo los polos con parte real negativa
                sigma.append(m.sin(alpha[k][0])*m.sinh(beta[0][0]))
                omega.append(m.cos(alpha[k][0])*m.cosh(beta[0][0])) #para omega es lo mismo si uso beta(0) o beta(1) ya que el cos es par
            else:
                sigma.append(m.sin(alpha[k][0])*m.sinh(beta[1][0]))
                omega.append(m.cos(alpha[k][0])*m.cosh(beta[0][0]))

        for k in range (0,len(sigma)):
            poles.append(1/complex(sigma[k],omega[k]))

        #print (poles)
        for k in range (0,n):
            zeros.append(complex(0,1/m.cos(alpha[k][0])))
        #print (zeros)
        print(n) 

        self.num, self.den = signal.zpk2tf(zeros,poles,1)
       #print(self.den)
        k = self.den[len(self.den)-1]/self.num[len(self .num)-1]
        self.sys = signal.TransferFunction(k*self.num,self.den)
       # self.w,self.mag,self.phase = signal.bode(self.sys, None, 10000)
       # pyplot.semilogx(self.w,-self.mag)
        #pyplot.show()
        self.H = denorm.General_aprox.denormalization(self,type,Ws,n,poles,zeros,Ws_mas,Wp,Wp_mas)
        zero_denorm, pole_denorm, gain_denorm = signal.tf2zpk(self.H.num,self.H.den)
        self.calcular_q(pole_denorm)



    def get_transfer(self):
        return self.H

    def calcular_q(self,polos):
        for i in range (0,len(polos)):
            modulo=np.abs(polos[i])
            qaux=(modulo/(-2*np.real((polos[i]))))
            self.Q.append(qaux)
            self.Q.sort()
            self.qmax=self.Q[(len(self.Q)-1)]
        return;


if __name__ == "__main__":
    ex1= Chevy_2(10,100,1000,2000, "LP")
    ex = Chevy_2.get_transfer(ex1)
    w,mag,phase = signal.bode(ex, None, 10000)
    pyplot.semilogx(w,-mag)
    pyplot.show()

        
        

