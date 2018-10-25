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
        e=1/(m.sqrt(m.pow(10,As/10)-1))

        if (type == "LP"):
            WsN = Ws/Wp
        elif (type == "HP"):
            WsN = Wp/Ws
        elif (type == "BP"):
            WsN = (Ws_mas-Ws)/(Wp_mas-Wp)
        elif (type == "BR"):
            WsN = (Wp_mas-Wp)/(Ws_mas-Ws)

        n=m.ceil(m.acosh((m.sqrt(m.pow(10,As/10)-1))/(m.sqrt(m.pow(10,Ap/10)-1)))/(m.acosh(WsN)))

        #hallo los polos de chevy
        alpha = []
        poles = []
        zeros = []
      
        for k in range (0,2*n):
            alpha.append([(2*(k+1)-1)/(2*n)*m.pi])

        beta = 1/n*m.asinh(1/e)

        for k in range (0,2*n): #hallo los polos
            if (1/(complex(m.sin(alpha[k][0])*m.sinh(beta), m.cos(alpha[k][0]*m.cosh(beta))))).real < 0:
                poles.append(WsN*(1/(complex(m.sin(alpha[k][0])*m.sinh(beta), m.cos(alpha[k][0]*m.cosh(beta))))))

        #print (poles)
        for k in range (0,n):
            zeros.append(WsN*complex(0,1/m.cos(alpha[k][0])))
        #print (zeros)
        print(n)
        self.num, self.den = signal.zpk2tf(zeros,poles,1)
       #print(self.den)
        k = self.den[len(self.den)-1]/self.num[len(self .num)-1]
        self.sys = signal.TransferFunction(k*self.num,self.den)
       # self.w,self.mag,self.phase = signal.bode(self.sys, None, 10000)
       # pyplot.semilogx(self.w,-self.mag)
        #pyplot.show()
        self.H = denorm.General_aprox.denormalization(self,type,Wp,n,poles,zeros)

    def get_transfer(self):
        return self.H


if __name__ == "__main__":
    ex1= Chevy_2(10,100,1000,5000, "LP")
    ex = Chevy_2.get_transfer(ex1)
    w,mag,phase = signal.bode(ex, None, 10000)
    pyplot.semilogx(w,-mag)
    pyplot.show()

        
        

