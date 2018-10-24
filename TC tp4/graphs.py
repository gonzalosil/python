import matplotlib, sys
matplotlib.use('TkAgg')
import math 
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk
import numpy as np


class graphs:
    def plotPhase(self):
        self.axis.clear()
        self.axis.semilogx(((self.w)/(2*(math.pi))),self.phase)
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_xlabel("$f (Hz)$")
        self.axis.set_ylabel("$Phase (deg)$")
        self.dataPlot.draw()

    def plotMag(self):
        self.axis.clear()
        self.axis.semilogx((self.w/(2*(math.pi))),-self.mag)
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_xlabel("$f (Hz)$")
        self.axis.set_ylabel("$Attenuation (dB)$")
        self.dataPlot.draw()

    def plotStep(self):
        self.axis.clear()
        self.axis.plot(self.stepT,self.stepMag)
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_xlabel("$t (s)$")
        self.axis.set_ylabel("$V_{out} (Volts)$")
        self.dataPlot.draw()

    def plotImp(self):
        self.axis.clear()
        self.axis.plot(self.impT,self.impMag)
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_xlabel("$t (s)$")
        self.axis.set_ylabel("$V_{out} (Volts)$")
        self.dataPlot.draw()

    def plotGroupDelay(self):
        self.axis.clear()
        self.axis.plot(self.GDfreq,self.gd)
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_ylabel("$Group delay [ms]$")
        self.axis.set_xlabel("$Frequency [Hz]$")
        self.dataPlot.draw()

    def plotPZ(self):
        self.axis.clear()
        for i in range(0,self.pzg[0].size): #plotea los ceros
            self.axis.plot(np.real(self.pzg[0][i]),np.imag(self.pzg[0][i]),'o')
        for i in range(0,self.pzg[1].size): #plotea los polos
            self.axis.plot(np.real(self.pzg[1][i]),np.imag(self.pzg[1][i]),'X')
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_xlabel("$Real$")
        self.axis.set_ylabel("$Imaginary$")
        self.dataPlot.draw()

    def set_low_pass(self):
        self.num=[1]
        self.den=[1,1]
        self.sys = signal.TransferFunction([1],[1,1])
        self.w,self.mag,self.phase = signal.bode(self.sys)
        self.stepT,self.stepMag = signal.step(self.sys)
        self.impT,self.impMag = signal.impulse(self.sys)
        self.pzg = signal.tf2zpk(self.sys.num, self.sys.den)
        self.GDfreq,self.gd = signal.group_delay((self.num,self.den))
        self.plotMag()

    def set_high_pass(self):
        self.num=[1,0]
        self.den=[1,1]
        self.sys = signal.TransferFunction([1,0],[1,1])
        self.w,self.mag,self.phase = signal.bode(self.sys)
        self.stepT,self.stepMag = signal.step(self.sys)
        self.impT,self.impMag = signal.impulse(self.sys)
        self.pzg = signal.tf2zpk(self.sys.num, self.sys.den)
        self.GDfreq,self.gd = signal.group_delay((self.num,self.den))
        print (self.pzg[0].size)
        self.plotMag()

    def set_band_pass(self):
        self.num=[1,0]
        self.den=[1,1,1]
        self.sys = signal.TransferFunction([1,0],[1,1,1])
        self.w,self.mag,self.phase = signal.bode(self.sys)
        self.stepT,self.stepMag = signal.step(self.sys)
        self.impT,self.impMag = signal.impulse(self.sys)
        self.pzg = signal.tf2zpk(self.sys.num, self.sys.den)
        self.GDfreq,self.gd = signal.group_delay((self.num,self.den))
        self.plotMag()

    def set_band_stop(self):
        self.num=[1,0,1]
        self.den=[1,1,1]
        self.sys = signal.TransferFunction([1,0,1],[1,1,1])
        self.w,self.mag,self.phase = signal.bode(self.sys)
        self.stepT,self.stepMag = signal.step(self.sys)
        self.impT,self.impMag = signal.impulse(self.sys)
        self.pzg = signal.tf2zpk(self.sys.num, self.sys.den)
        self.GDfreq,self.gd = signal.group_delay((self.num,self.den))
        self.plotMag()

#-------------------------------------------------------------------------

    def SelectFilter(self):
        
        self.AttenuationAp()
        self.AttenuationAa()
        self.Frec_p()
        self.Frec_a()
        v=["Low Pass","High Pass","Band Pass","Band Stop"]
        combo=ttk.Combobox(self.root,values=v, width=20)
        combo.set("Select Type of Filter")
        combo.pack(side=LEFT,padx=2,pady=4)
        self.SelectFilter=combo
        button= Button(self.root, text="Graph", command=self.graph_me).pack(side=LEFT)



    def graph_me(self):

        value=self.SelectFilter.get()
        Ap=self.AttenuationAp.get()
        Aa=self.AttenuationAa.get()
        Fp=self.Frec_p.get()
        Fa=self.Frec_a.get()

        print(value)
        print(Ap)
        print(Aa)  # Para castear estos valores simplemente hacer int(variable)
        print(Fp)
        print(Fa)

        if value=="Low Pass":
            self.set_low_pass()
        if value=="High Pass":
            self.set_high_pass()
        if value=="Band Pass":
            self.set_band_pass()
        if value=="Band Stop":
            self.set_band_stop()




#------------------------------------------------------------------------------------------------------------
    def AttenuationAp(self):
        Ap=Label(text="Ap:").place(x=0,y=300)
        entradaAp=StringVar()
        txtUsuario=Entry(self.root, width=5 ,textvariable=entradaAp).place(x=30,y=300)
        self.AttenuationAp=entradaAp

    def AttenuationAa(self):
        Aa=Label(text="Aa:").place(x=70,y=300)
        entradaAa=StringVar()
        txtUsuario=Entry(self.root, width=5 ,textvariable=entradaAa).place(x=100,y=300)
        self.AttenuationAa=entradaAa

    def Frec_p(self):
        Fp=Label(text="Fp:").place(x=0,y=330)
        entradaFp=StringVar()
        txtUsuario=Entry(self.root, width=5, textvariable=entradaFp).place(x=30,y=330)
        self.Frec_p=entradaFp

    def Frec_a(self):
        Fa=Label(text="Fa:").place(x=70,y=330)
        entradaFa=StringVar()
        txtUsuario=Entry(self.root, width=5, textvariable=entradaFa).place(x=100,y=330)
        self.Frec_a=entradaFa


#---------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.root = Tk()
        self.root.title("TP4")




  
        #------------------------------------------------------------------------
        toolbar = Frame(self.root)
        #toolbar2 = Frame(self.root)
   
       
       #primera toolbar

        buttonPhase = Button(toolbar,text="Bode Phase",command=self.plotPhase)
        buttonPhase.pack(side=LEFT,padx=2,pady=2)
        buttonMag = Button(toolbar,text="Bode Mag",command=self.plotMag)
        buttonMag.pack(side=LEFT,padx=2,pady=2)
        buttonStep = Button(toolbar,text="Step",command=self.plotStep)
        buttonStep.pack(side=LEFT,padx=2,pady=2)
        buttonImp = Button(toolbar,text="Impulse",command=self.plotImp)
        buttonImp.pack(side=LEFT,padx=2,pady=4)
        buttonPZ = Button(toolbar,text="Poles and zeros",command=self.plotPZ)
        buttonPZ.pack(side=LEFT,padx=2,pady=4)
        buttonGD = Button(toolbar,text="Group Delay",command=self.plotGroupDelay)
        buttonGD.pack(side=LEFT,padx=2,pady=4)
       
       # segunda toolbar
        self.SelectFilter()

       
        #button_low_pass = Button(toolbar2, text = "Low Pass", command = self.set_low_pass)
        #button_low_pass.pack(side=LEFT,padx=2,pady=4)
        #button_high_pass = Button(toolbar2, text = "High Pass", command = self.set_high_pass)
        #button_high_pass.pack(side=LEFT,padx=2,pady=4)
        #button_band_pass = Button(toolbar2, text = "Band Pass", command = self.set_band_pass)
        #button_band_pass.pack(side=LEFT,padx=2,pady=4)
        #button_band_stop = Button(toolbar2, text = "Stop Band", command = self.set_band_stop)
        #button_band_stop.pack(side=LEFT,padx=2,pady=4)
        toolbar.pack(side=TOP,fill=X)
        #toolbar2.pack(side=TOP, fill=X)
        graph = Canvas(self.root)
        graph.pack(side=TOP,fill=BOTH,expand=True,padx=2,pady=4)

        #--------------------------------------------------------------------------------

        f = Figure()
        self.axis = f.add_subplot(111)

        self.dataPlot = FigureCanvasTkAgg(f, master=graph)
        self.dataPlot.draw()
        self.dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        nav = NavigationToolbar2Tk(self.dataPlot, self.root)
        nav.update()
        self.dataPlot._tkcanvas.pack(side=TOP, fill=X, expand=True)

       
       

        
        #self.root.geometry("1000x1000")
        self.root.mainloop()

if __name__ == "__main__":
    ex = graphs()



