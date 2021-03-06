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

class Chevy_1(object):
    def __init__(self, Ap, As, Wp, Ws, type):
        e=m.sqrt(m.pow(10,Ap/10)-1)
        n=m.ceil(m.acosh((m.sqrt(m.pow(10,As/10)-1))/e)/(m.acosh(Ws/Wp)))

        #hallo los polos de chevy

        alpha = []
        beta = []
        sigma = []
        omega = []
        poles = []
      
        for k in range (0,n):
            alpha.append([(2*(k+1)-1)/(2*n)*m.pi])

        beta.append([1/n*m.asinh(1/e)])
        beta.append([-1/n*m.asinh(1/e)])

        #a = float ('' .join(str(i) for i in alpha[0]))
        #print (a)
        print(beta[0][0])
        for k in range (0,n):
            if m.sin(alpha[k][0])*m.sinh(beta[0][0]) < 0: #tomo solo los polos con parte real negativa
                sigma.append(m.sin(alpha[k][0])*m.sinh(beta[0][0]))
                omega.append(m.cos(float (alpha[k][0]))*m.cosh(beta[0][0])) #para omega es lo mismo si uso beta(0) o beta(1) ya que el cos es par
            else:
                sigma.append(m.sin(alpha[k][0])*m.sinh(beta[1][0]))
                omega.append(m.cos(float (alpha[k][0]))*m.cosh(beta[0][0]))

        for k in range (0,n):
            poles.append(complex(sigma[k],omega[k]))
        #print(n)
        #print (poles)

        self.num, self.den = signal.zpk2tf(1,poles,1)
       # print(self.den)
       
        self.sys = signal.TransferFunction(1,self.den)
        self.w,self.mag,self.phase = signal.bode(self.sys, None, 10000)
       # self.w=self.w/Wp*pow(e,1/n)
        pyplot.semilogx(self.w,-self.mag)
        pyplot.show()
        self.H = denorm.General_aprox.denormalization(type,Wp,n,poles)
        self.w,self.mag,self.phase = signal.bode(self.H, None, 10000)
        pyplot.semilogx(self.w,-self.mag)
        pyplot.show()

if __name__ == "__main__":
    ex = Chevy_1(10,100,1000,1500, "LP")



