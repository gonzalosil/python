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
#--Se aprieta el boton Select
#-------------------------------
    def Se_Apreto_Select(self):

        #--- aca sabemos el tipo de aproximacion y filtro que se selecciono

        ApproxSelected=self.Type_of_approx.get()

        if ApproxSelected=="Butterworth":
           print(ApproxSelected)
        elif  ApproxSelected=="Chebycheff":
            print(ApproxSelected)
        elif  ApproxSelected=="Chebycheff Inverso":
            print(ApproxSelected)
        elif ApproxSelected=="Bessel":
            print(ApproxSelected)
        else:
            print("unknown")



        FilterSelected=self.Type_of_filter.get()

        if FilterSelected=="Low Pass":
           print(FilterSelected)
           self.labels_and_entrys_LPHP()
           #self.set_low_pass()
        elif  FilterSelected=="High Pass":
            print(FilterSelected)
            self.labels_and_entrys_LPHP()
            #self.set_high_pass()
        elif  FilterSelected=="Band Pass":
            print(FilterSelected)
            self.labels_and_entrys_BPBS()
            #self.set_band_pass()
        elif FilterSelected=="Band Stop":
            print(FilterSelected)
            self.labels_and_entrys_BPBS()
            #self.set_band_stop()
        else:
            print("unknown")

#---------------
#--aca se eligio la frecuencia de denormalizacion
#--habilito o deshabilito la opcion de poner un porcentaje
#---------------
    def selection_of_DenormFrec_changed(self, event):
        Selected_Denorm_Frec=self.Denormalize_frec.get()
        if Selected_Denorm_Frec=="Wother":
            self.entry_Denorm_percentage.grid(row=9,column=3)
            self.label_percentage.grid(row=9,column=4)
        else:
            self.entry_Denorm_percentage.grid_forget()
            self.label_percentage.grid_forget()
            



    def CheckBotton_Orden_HIGH(self):

        Selected_checkbotton_orden=self.var_Orden.get()
        if Selected_checkbotton_orden:
            self.entry_orden.grid(row=10,column=3)
        else:
            self.entry_orden.grid_forget()

    def CheckBotton_Q_HIGH(self):

        Selected_checkbotton_Q=self.var_Q.get()
        if Selected_checkbotton_Q:
            self.entry_Q.grid(row=11,column=3)
        else:
            self.entry_Q.grid_forget()

#---entrys para low pass y high pass
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#---oculta algunos labels y entry cuando estoy en HP o LP, ojo!! igualmente tomar los datos del ENTRY de w0 porque eso no cambia, solo cambia el label
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    def labels_and_entrys_LPHP(self):
        self.label_wp0.grid_forget()
        self.label_wa0.grid_forget()
        self.label_Ap0.grid_forget()
        self.label_Aa0.grid_forget()

        self.label_wp1.grid_forget()
        self.label_wa1.grid_forget()
        self.label_Ap1.grid_forget()
        self.label_Aa1.grid_forget()

        self.entry_wp1.grid_forget()
        self.entry_wa1.grid_forget()
        self.entry_Ap1.grid_forget()
        self.entry_Aa1.grid_forget()

        self.label_Hz.grid_forget()
        self.label_dB.grid_forget()
        self.label_Hz1.grid_forget()
        self.label_dB1.grid_forget()

        self.label_wp.grid(row=1,column=0)
        self.label_wa.grid(row=2,column=0)
        self.label_Ap.grid(row=3,column=0)
        self.label_Aa.grid(row=4,column=0)

#----entrys para band pass y band stop
    def labels_and_entrys_BPBS(self):

        self.label_wp0.grid(row=1,column=0)
        self.label_wa0.grid(row=2,column=0)
        self.label_Ap0.grid(row=3,column=0)
        self.label_Aa0.grid(row=4,column=0)

        self.label_wp.grid_forget()
        self.label_wa.grid_forget()
        self.label_Ap.grid_forget()
        self.label_Aa.grid_forget()

        self.label_wp1.grid(row=5,column=0)
        self.label_wa1.grid(row=6,column=0)
        self.label_Ap1.grid(row=7,column=0)
        self.label_Aa1.grid(row=8,column=0)

        self.entry_wp0.grid(row=1,column=1)
        self.entry_wa0.grid(row=2,column=1)
        self.entry_Ap0.grid(row=3,column=1)
        self.entry_Aa0.grid(row=4,column=1)

        self.entry_wp1.grid(row=5,column=1)
        self.entry_wa1.grid(row=6,column=1)
        self.entry_Ap1.grid(row=7,column=1)
        self.entry_Aa1.grid(row=8,column=1)

        self.label_Hz=Label(self.ventana_izquierda,text="rad/s")
        self.label_Hz.grid(row=1,column=2)
        self.label_Hz=Label(self.ventana_izquierda,text="rad/s")
        self.label_Hz.grid(row=2,column=2)
        self.label_dB=Label(self.ventana_izquierda,text="dB")
        self.label_dB.grid(row=3,column=2)
        self.label_dB=Label(self.ventana_izquierda,text="dB")
        self.label_dB.grid(row=4,column=2)

        self.label_Hz=Label(self.ventana_izquierda,text="rad/s")
        self.label_Hz.grid(row=5,column=2)
        self.label_Hz1=Label(self.ventana_izquierda,text="rad/s")
        self.label_Hz1.grid(row=6,column=2)
        self.label_dB1=Label(self.ventana_izquierda,text="dB")
        self.label_dB1.grid(row=7,column=2)
        self.label_dB=Label(self.ventana_izquierda,text="dB")
        self.label_dB.grid(row=8,column=2)




#------------------
#-----frames
#---------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.root = Tk()
        self.root.title("TP 4 - Grupo 6 - Teoria de Circuitos - 2018")


#---VENTANA IZQUIERDA
#------------------------------------------------------------------------
    
        self.ventana_izquierda=Frame(self.root)

        self.ventana_izquierda.grid(row=0,column=0)

#Seleccionador de aproximacion
        
        values_approx=["Butterworth","Chebycheff","Chebycheff Inverso","Bessel"]
        self.Type_of_approx=ttk.Combobox(self.ventana_izquierda,values=values_approx, width=30,state="readonly")
        self.Type_of_approx.set("Select Appoximation")
        self.Type_of_approx.grid(row=0,column=0,padx=40,pady=10)
   
#Seleccionador de tipo de filtro

        values_filter=["Low Pass","High Pass","Band Pass","Band Stop"]
        self.Type_of_filter=ttk.Combobox(self.ventana_izquierda,values=values_filter, width=20,state="readonly")
        self.Type_of_filter.set("Select Type of Filter")
        self.Type_of_filter.grid(row=0,column=1,padx=10,pady=10)


#boton seleccionador
        button_select=Button(self.ventana_izquierda, text="   Select   ", command=self.Se_Apreto_Select)
        button_select.grid(row=0,column=3)




#Frecuencias y atenuaciones 

        self.label_wp0=Label(self.ventana_izquierda,text="Wp(+):")
        self.label_wa0=Label(self.ventana_izquierda,text="Wa(+):")
        self.label_Ap0=Label(self.ventana_izquierda,text="Ap(+):")
        self.label_Aa0=Label(self.ventana_izquierda,text="Aa(+):")

        self.label_wp=Label(self.ventana_izquierda,text="Wp:")
        self.label_wa=Label(self.ventana_izquierda,text="Wa:")
        self.label_Ap=Label(self.ventana_izquierda,text="Ap:")
        self.label_Aa=Label(self.ventana_izquierda,text="Aa:")

        self.label_wp1=Label(self.ventana_izquierda,text="Wp(-):")
        self.label_wa1=Label(self.ventana_izquierda,text="Wa(-):")
        self.label_Ap1=Label(self.ventana_izquierda,text="Ap(-):")
        self.label_Aa1=Label(self.ventana_izquierda,text="Aa(-):")



        self.entry_wp0=Entry(self.ventana_izquierda)
        self.entry_wa0=Entry(self.ventana_izquierda)
        self.entry_Ap0=Entry(self.ventana_izquierda)
        self.entry_Aa0=Entry(self.ventana_izquierda)

        self.entry_wp1=Entry(self.ventana_izquierda)
        self.entry_wa1=Entry(self.ventana_izquierda)
        self.entry_Ap1=Entry(self.ventana_izquierda)
        self.entry_Aa1=Entry(self.ventana_izquierda)


        self.labels_and_entrys_BPBS()




#Denormalizacion
        label_frec_denor=Label(self.ventana_izquierda,text="Denormalize Frecuency:")
        label_frec_denor.grid(row=9,column=0)

        values_frec=["Wa","Wp","Wother"]
        self.Denormalize_frec=ttk.Combobox(self.ventana_izquierda,values=values_frec, width=30,state="readonly")
        self.Denormalize_frec.set("Select")
        self.Denormalize_frec.grid(row=9,column=1,padx=10,pady=10)

        self.Denormalize_frec.bind("<<ComboboxSelected>>", self.selection_of_DenormFrec_changed)

        self.entry_Denorm_percentage=Entry(self.ventana_izquierda)

        self.label_percentage=Label(self.ventana_izquierda,text="%")


#Orden del filtro
        label_orden=Label(self.ventana_izquierda,text="Filter Order:")
        label_orden.grid(row=10,column=0)

        label_fixed=Label(self.ventana_izquierda,text="Check if fixed:")
        label_fixed.grid(row=10,column=1, sticky="w")

        self.var_Orden=IntVar()
        self.check_button_orden=Checkbutton(self.ventana_izquierda, variable=self.var_Orden, command=self.CheckBotton_Orden_HIGH)
        self.check_button_orden.grid(row=10,column=1)

        self.entry_orden=Entry(self.ventana_izquierda)





#Q del filtro
        label_Q=Label(self.ventana_izquierda,text="Q of the Filter:")
        label_Q.grid(row=11,column=0)

        label_fixed=Label(self.ventana_izquierda,text="Check if fixed:")
        label_fixed.grid(row=11,column=1, sticky="w")

        self.var_Q=IntVar()
        self.check_button_Q=Checkbutton(self.ventana_izquierda, variable=self.var_Q, command=self.CheckBotton_Q_HIGH)
        self.check_button_Q.grid(row=11,column=1)

        self.entry_Q=Entry(self.ventana_izquierda)



#boton graficar
        button_select=Button(self.ventana_izquierda, text="   Graph   ")#, command=self.Se_Apreto_Graph())
        button_select.grid(row=12,columnspan=50)

#-----------------------------------------------------------

        
#---VENTANA DERECHA
#------------------------------------------------------------------------
    
        self.ventana_derecha=Frame(self.root)

        self.ventana_derecha.grid(row=0,column=1)

        buttonMag = Button(self.ventana_derecha,text="Bode Magnitude")
        buttonMag.grid(row=0, column=0,padx=10,pady=10)
        buttonPhase = Button(self.ventana_derecha,text="Bode Phase")
        buttonPhase.grid(row=0, column=1,padx=10,pady=10)
        buttonStep = Button(self.ventana_derecha,text="Step")
        buttonStep.grid(row=0, column=2,padx=10,pady=10)
        buttonImp = Button(self.ventana_derecha,text="Impulse")
        buttonImp.grid(row=0, column=3,padx=10,pady=10)
        buttonPZ = Button(self.ventana_derecha,text="Poles and Zeros")
        buttonPZ.grid(row=0, column=4,padx=10,pady=10)
        buttonGD = Button(self.ventana_derecha,text="Group Delay")
        buttonGD.grid(row=0, column=5,padx=10,pady=10)
       

        graph = Canvas(self.ventana_derecha, bg="blue")
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