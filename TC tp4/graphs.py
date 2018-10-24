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

#----funciones de ploteo
#-----------------------------------------------------------------------
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


#----funciones de seteo de tipo de filtro
#------------------------------------------------------------------------

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





#-----frames
#---------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.root = Tk()
        self.root.title("TP 4 - Grupo 6 - Teoria de Circuitos - 2018")


#---VENTANA IZQUIERDA
#------------------------------------------------------------------------
    
        ventana_izquierda=Frame(self.root)

        ventana_izquierda.grid(row=0,column=0)

#Seleccionador de aproximacion
        
        values_approx=["Butterworth","Chebycheff","Chebycheff Inverso","Bessel"]
        Type_of_approx=ttk.Combobox(ventana_izquierda,values=values_approx, width=20)
        Type_of_approx.set("Select Appoximation")
        Type_of_approx.grid(row=0,column=0,padx=40,pady=10)


#Seleccionador de tipo de filtro

        values_filter=["Low Pass","High Pass","Band Pass","Band Stop"]
        Type_of_filter=ttk.Combobox(ventana_izquierda,values=values_filter, width=20)
        Type_of_filter.set("Select Type of Filter")
        Type_of_filter.grid(row=0,column=1,padx=10,pady=10)


#boton seleccionador
        button_select=Button(ventana_izquierda, text="   Select   ")
        button_select.grid(row=0,column=3)




#Frecuencias y atenuaciones

        label_wp0=Label(ventana_izquierda,text="Wp+:")
        label_wa0=Label(ventana_izquierda,text="Wa+:")
        label_Ap0=Label(ventana_izquierda,text="Ap+:")
        label_Aa0=Label(ventana_izquierda,text="Aa+:")

        label_wp1=Label(ventana_izquierda,text="Wp-:")
        label_wa1=Label(ventana_izquierda,text="Wa-:")
        label_Ap1=Label(ventana_izquierda,text="Ap-:")
        label_Aa1=Label(ventana_izquierda,text="Aa-:")



        entry_wp0=Entry(ventana_izquierda)
        entry_wa0=Entry(ventana_izquierda)
        entry_Ap0=Entry(ventana_izquierda)
        entry_Aa0=Entry(ventana_izquierda)

        entry_wp1=Entry(ventana_izquierda)
        entry_wa1=Entry(ventana_izquierda)
        entry_Ap1=Entry(ventana_izquierda)
        entry_Aa1=Entry(ventana_izquierda)


        label_wp0.grid(row=1,column=0)
        label_wa0.grid(row=2,column=0)
        label_Ap0.grid(row=3,column=0)
        label_Aa0.grid(row=4,column=0)

        label_wp1.grid(row=5,column=0)
        label_wa1.grid(row=6,column=0)
        label_Ap1.grid(row=7,column=0)
        label_Aa1.grid(row=8,column=0)

#unidades
        label_Hz=Label(ventana_izquierda,text="rad/s")
        label_Hz.grid(row=1,column=2)
        label_Hz=Label(ventana_izquierda,text="rad/s")
        label_Hz.grid(row=2,column=2)
        label_dB=Label(ventana_izquierda,text="dB")
        label_dB.grid(row=3,column=2)
        label_dB=Label(ventana_izquierda,text="dB")
        label_dB.grid(row=4,column=2)


        entry_wp0.grid(row=1,column=1)
        entry_wa0.grid(row=2,column=1)
        entry_Ap0.grid(row=3,column=1)
        entry_Aa0.grid(row=4,column=1)

        entry_wp1.grid(row=5,column=1)
        entry_wa1.grid(row=6,column=1)
        entry_Ap1.grid(row=7,column=1)
        entry_Aa1.grid(row=8,column=1)

#unidades
        label_Hz=Label(ventana_izquierda,text="rad/s")
        label_Hz.grid(row=5,column=2)
        label_Hz=Label(ventana_izquierda,text="rad/s")
        label_Hz.grid(row=6,column=2)
        label_dB=Label(ventana_izquierda,text="dB")
        label_dB.grid(row=7,column=2)
        label_dB=Label(ventana_izquierda,text="dB")
        label_dB.grid(row=8,column=2)


#Denormalizacion
        label_frec_denor=Label(ventana_izquierda,text="Denormalize Frecuency:")
        label_frec_denor.grid(row=9,column=0)

        values_frec=["Wa","Wp","Wohter"]
        Denormalize=ttk.Combobox(ventana_izquierda,values=values_frec, width=30)
        Denormalize.set("Select")
        Denormalize.grid(row=9,column=1,padx=10,pady=10)

        entry_Denorm_percentage=Entry(ventana_izquierda)
        entry_Denorm_percentage.grid(row=9,column=3)

        label_percentage=Label(ventana_izquierda,text="%")
        label_percentage.grid(row=9,column=4)

#Orden del filtro
        label_orden=Label(ventana_izquierda,text="Filter Order:")
        label_orden.grid(row=10,column=0)

        label_fixed=Label(ventana_izquierda,text="Check if fixed:")
        label_fixed.grid(row=10,column=1, sticky="w")

        check_button_orden=Checkbutton(ventana_izquierda)
        check_button_orden.grid(row=10,column=1)

        entry_orden=Entry(ventana_izquierda)
        entry_orden.grid(row=10,column=3)

#Q del filtro
        label_Q=Label(ventana_izquierda,text="Q of the Filter:")
        label_Q.grid(row=11,column=0)

        label_fixed=Label(ventana_izquierda,text="Check if fixed:")
        label_fixed.grid(row=11,column=1, sticky="w")

        check_button_orden=Checkbutton(ventana_izquierda)
        check_button_orden.grid(row=11,column=1)

        entry_Q=Entry(ventana_izquierda)
        entry_Q.grid(row=11,column=3)


#boton graficar
        button_select=Button(ventana_izquierda, text="   Graph   ")
        button_select.grid(row=12,columnspan=50)

#-----------------------------------------------------------

        
#---VENTANA DERECHA
#------------------------------------------------------------------------
    
        ventana_derecha=Frame(self.root)

        ventana_derecha.grid(row=0,column=1)

        buttonMag = Button(ventana_derecha,text="Bode Magnitude")
        buttonMag.grid(row=0, column=0,padx=10,pady=10)
        buttonPhase = Button(ventana_derecha,text="Bode Phase")
        buttonPhase.grid(row=0, column=1,padx=10,pady=10)
        buttonStep = Button(ventana_derecha,text="Step")
        buttonStep.grid(row=0, column=2,padx=10,pady=10)
        buttonImp = Button(ventana_derecha,text="Impulse")
        buttonImp.grid(row=0, column=3,padx=10,pady=10)
        buttonPZ = Button(ventana_derecha,text="Poles and Zeros")
        buttonPZ.grid(row=0, column=4,padx=10,pady=10)
        buttonGD = Button(ventana_derecha,text="Group Delay")
        buttonGD.grid(row=0, column=5,padx=10,pady=10)
       

        graph = Canvas(ventana_derecha, bg="blue")
        graph.grid(row=1, columnspan=100,padx=10,pady=10)

        f = Figure()
        self.axis = f.add_subplot(111)

        self.dataPlot = FigureCanvasTkAgg(f, master=graph)
        self.dataPlot.draw()
        self.dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        #nav = NavigationToolbar2Tk(self.dataPlot, ventana_derecha)
        #nav.update()
        self.dataPlot._tkcanvas.pack(side=TOP, expand=True)

       
      
        self.root.mainloop()

if __name__ == "__main__":
    ex = graphs()