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
import Chevy_1 as Chevy
from matplotlib import pyplot
import Butterworth as Butter

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
        self.axis2.clear()
        for i in range(0,self.pzg[0].size): #plotea los ceros
            self.axis.plot(np.real(self.pzg[0][i]),np.imag(self.pzg[0][i]),'o')
            self.axis2.plot(np.real(self.pzg[0][i]),np.imag(self.pzg[0][i]),'o')
        for i in range(0,self.pzg[1].size): #plotea los polos
            self.axis.plot(np.real(self.pzg[1][i]),np.imag(self.pzg[1][i]),'X')
            self.axis2.plot(np.real(self.pzg[1][i]),np.imag(self.pzg[1][i]),'X')
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis2.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_xlabel("$Real$")
        self.axis.set_ylabel("$Imaginary$")
        self.axis2.set_xlabel("$Real$")
        self.axis2.set_ylabel("$Imaginary$")
        self.dataPlot.draw()
        self.dataPlot2.draw()

#----funciones de seteo de tipo de filtro
#------------------------------------------------------------------------

    def set_filter(self):
        #self.num=[1]
        #self.den=[1,1]
        #self.sys = signal.TransferFunction([1],[1,1])
        #self.sys = TransferFuntion
        self.w,self.mag,self.phase = signal.bode(self.sys)
        self.stepT,self.stepMag = signal.step(self.sys)
        self.impT,self.impMag = signal.impulse(self.sys)
        self.pzg = signal.tf2zpk(self.sys.num, self.sys.den)
        self.GDfreq,self.gd = signal.group_delay((self.sys.num,self.sys.den))
        self.plotMag()


#----------------------------------------------------------------------------------------------
#--Se aprieta el boton Select y se ponen las entrys dependiendo el tipo de filtro y aproximacion
#-------------------------------
    def Se_Apreto_Select(self):

        #--- aca sabemos el tipo de aproximacion y filtro que se selecciono

        ApproxSelected=self.Type_of_approx.get()

        if ApproxSelected=="Butterworth":
           self.hide_label_and_entry_BESSEL()
           #print(ApproxSelected)
        elif  ApproxSelected=="Chebycheff":
            self.hide_label_and_entry_BESSEL()
            #print(ApproxSelected)
        elif  ApproxSelected=="Chebycheff Inverso":
            self.hide_label_and_entry_BESSEL()
            #print(ApproxSelected)
        elif ApproxSelected=="Bessel":
            self.label_and_entry_BESSEL()
            #print(ApproxSelected)
        else:
            print("unknown")



        FilterSelected=self.Type_of_filter.get()

        if FilterSelected=="LP":
           #print(FilterSelected)
           self.labels_and_entrys_LPHP()
           #self.set_low_pass()
        elif  FilterSelected=="HP":
            #print(FilterSelected)
            self.labels_and_entrys_LPHP()
            #self.set_high_pass()
        elif  FilterSelected=="BP":
            #print(FilterSelected)
            self.labels_and_entrys_BPBS()
            #self.set_band_pass()
        elif FilterSelected=="BR":
            #print(FilterSelected)
            self.labels_and_entrys_BPBS()
            #self.set_band_stop()
        else:
            print("unknown")

#------------------------------------
#
#-------------------------------------
    def Se_Apreto_Graph(self):

        #tipo de filtro y aproximacion
        ApproxSelected=self.Type_of_approx.get()
        FilterSelected=self.Type_of_filter.get()
        print(ApproxSelected) #dato
        print(FilterSelected) #dato

        #frecuencia de denormalizacion
        Selected_Denorm_Frec=self.Denormalize_frec.get()
        if Selected_Denorm_Frec=="Wother":
            Denormalize_percentage=self.entry_Denorm_percentage.get()
        elif Selected_Denorm_Frec=="Wp":
            print(self.Denormalize_frec.get())
            Denormalize_percentage=0
        elif Selected_Denorm_Frec=="Wa":
            print(self.Denormalize_frec.get())
            Denormalize_percentage=100
        else:
            Denormalize_percentage=None
        #porcentaje de denormalizacion
        print(Denormalize_percentage) #dato


        #frecuencias y atenuaciones 0
        if len(self.entry_wp0.get()) != 0:
            wp0=int(self.entry_wp0.get())
        else:
            wp0=None
        print(wp0) #dato

        if len(self.entry_wa0.get()) != 0:
            wa0=int(self.entry_wa0.get())
        else:
            wa0=None
        print(wa0) #dato

        if len(self.entry_Ap0.get()) != 0:
            Ap0=int(self.entry_Ap0.get())
        else:
            Ap0=None
        print(Ap0) #dato

        if len(self.entry_Aa0.get()) != 0:
            Aa0=int(self.entry_Aa0.get())
        else:
            Aa0=None
        print(Aa0) #dato

        #frecuencias y atenuaciones 1
        if len(self.entry_wp1.get()) != 0:
            wp1=int(self.entry_wp1.get())
        else:
            wp1=None
        print(wp1) #dato

        if len(self.entry_wa1.get()) != 0:
            wa1=int(self.entry_wa1.get())
        else:
            wa1=None
        print(wa1) #dato



        #orden del filtro

        Selected_checkbotton_orden=self.var_Orden.get()
        if Selected_checkbotton_orden:
            Orden=int(self.entry_orden.get())
        else:
            Orden=None 
        print(Orden) #dato
         
        #Q del filtro

        Selected_checkbotton_Q=self.var_Q.get()
        if Selected_checkbotton_Q:
            Q=int(self.entry_Q.get())
        else:
            Q=None
        print(Q) #dato

        if ApproxSelected=="Butterworth":
            self.Function=Butter.Butterworth(Aa0, Ap0, wp0, wa0, FilterSelected , Orden, Denormalize_percentage, wp0,wp1, wa0, wa1)
            self.sys=Butter.Butterworth.get_transfer(self.Function)
            self.set_filter()
        elif  ApproxSelected=="Chebycheff":

            self.Function=Chevy.Chevy_1(Ap0, Aa0, wp0, wa0, FilterSelected, wp1, wa1)
            self.sys=Chevy.Chevy_1.get_transfer(self.Function)
            self.set_filter()

            #w,mag,phase = signal.bode(TransferFunction, None, 10000)
            #pyplot.semilogx(w,-mag)
            #pyplot.show()

     
            #self.sys=TransferFunction
            #self.w,self.mag,self.phase = signal.bode(self.H, None, 10000)
            #pyplot.semilogx(self.w,-self.mag)
            #pyplot.show()
            #self.set_filter(TransferFuction)
            #print(TransferFuction)
        #elif  ApproxSelected=="Chebycheff Inverso":
        #el
        elif ApproxSelected=="Bessel":
            Tretardo=int(self.entry_Tretardo.get())
            print(Tretardo)
        else:
           print("unknown")



        FilterSelected=self.Type_of_filter.get()

        if FilterSelected=="LP":
           #print(FilterSelected)
           self.labels_and_entrys_LPHP()
           #self.set_low_pass()
        elif  FilterSelected=="HP":
            #print(FilterSelected)
            self.labels_and_entrys_LPHP()
            #self.set_high_pass()
        elif  FilterSelected=="BP":
            #print(FilterSelected)
            self.labels_and_entrys_BPBS()
            #self.set_band_pass()
        elif FilterSelected=="BR":
            #print(FilterSelected)
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


        self.label_wp1.grid_forget()
        self.label_wa1.grid_forget()


        self.entry_wp1.grid_forget()
        self.entry_wa1.grid_forget()


        self.entry_wp1.delete(0, END)
        self.entry_wa1.delete(0, END)

        

        self.label_Hz.grid_forget()
        self.label_Hz1.grid_forget()


        self.label_wp.grid(row=1,column=0)
        self.label_wa.grid(row=2,column=0)


#----entrys para band pass y band stop
    def labels_and_entrys_BPBS(self):

        self.label_wp0.grid(row=1,column=0)
        self.label_wa0.grid(row=2,column=0)
        self.label_Ap0.grid(row=3,column=0)
        self.label_Aa0.grid(row=4,column=0)

        self.label_wp.grid_forget()
        self.label_wa.grid_forget()


        self.label_wp1.grid(row=5,column=0)
        self.label_wa1.grid(row=6,column=0)


        self.entry_wp0.grid(row=1,column=1)
        self.entry_wa0.grid(row=2,column=1)
        self.entry_Ap0.grid(row=3,column=1)
        self.entry_Aa0.grid(row=4,column=1)

        self.entry_wp1.grid(row=5,column=1)
        self.entry_wa1.grid(row=6,column=1)


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


#------------------------
#-- si se presiona Bessel agrega para que le usuario ingrese un tiempo de retardo sino lo oculta
#------------------------
    def label_and_entry_BESSEL(self):

        self.label_Tretardo.grid(row=13, column=0)
        self.entry_Tretardo.grid(row=13,column=1)
        self.label_microsec.grid(row=13,column=1, sticky='e')

    def hide_label_and_entry_BESSEL(self):

        self.label_Tretardo.grid_forget()
        self.entry_Tretardo.grid_forget()
        self.entry_Tretardo.delete(0, END)
        self.label_microsec.grid_forget()
        





    def Selected_Etapa(self, event):

        Etapa_Selected=self.Etapa.get()
        if Etapa_Selected=="Etapa 1":
            self.ventana_segunda_etapa.grid_forget()
            self.ventana_primera_etapa.grid()
        elif Etapa_Selected=="Etapa 2":
            self.ventana_primera_etapa.grid_forget()
            self.ventana_segunda_etapa.grid()
            self.plotPZ()

        


#------------------
#-----frames
#------------------
    def __init__(self):
        self.root = Tk()
        self.root.title("TP 4 - Grupo 6 - Teoria de Circuitos - 2018")


        self.ventana=Frame(self.root)
        self.ventana.grid()


        values_Etapa=["Etapa 1","Etapa 2"]
        self.Etapa=ttk.Combobox(self.ventana,values=values_Etapa, width=30,state="readonly")
        self.Etapa.set("Etapa 1")
        self.Etapa.grid(row=0,column=0)

        self.Etapa.bind("<<ComboboxSelected>>", self.Selected_Etapa)



        self.ventana_primera_etapa=Frame(self.ventana)
        self.ventana_primera_etapa.grid()

        self.ventana_segunda_etapa=Frame(self.ventana)
        
        #---------
        #-- Frames de la vetnana de la primera etapa
        #----------
        self.ventana_superior=Frame(self.ventana_primera_etapa)
        self.ventana_superior.pack(side=TOP)

        self.ventana_inferior=Frame(self.ventana_primera_etapa)
        self.ventana_inferior.pack(side=BOTTOM)

        self.ventana_izquierda=Frame(self.ventana_superior)
        self.ventana_derecha=Frame(self.ventana_superior)
        self.ventana_izquierda.grid(row=1,column=1)
        self.ventana_derecha.grid(row=1,column=0)

                #---------
        #-- Frames de la vetnana de la segunda etapa
        #----------
        self.ventana_superior2=Frame(self.ventana_segunda_etapa)
        self.ventana_superior2.pack(side=TOP)

        self.ventana_inferior2=Frame(self.ventana_segunda_etapa)
        self.ventana_inferior2.pack(side=BOTTOM)

        self.ventana_izquierda2=Frame(self.ventana_superior2)
        self.ventana_derecha2=Frame(self.ventana_superior2)
        self.ventana_izquierda2.grid(row=1,column=1)
        self.ventana_derecha2.grid(row=1,column=0)

        



#---VENTANA IZQUIERDA ETAPA 1
#------------------------------------------------------------------------
   

#Seleccionador de aproximacion
        
        values_approx=["Butterworth","Chebycheff","Chebycheff Inverso","Bessel"]
        self.Type_of_approx=ttk.Combobox(self.ventana_izquierda,values=values_approx, width=30,state="readonly")
        self.Type_of_approx.set("Select Appoximation")
        self.Type_of_approx.grid(row=0,column=0,padx=10,pady=10)
   
#Seleccionador de tipo de filtro

        values_filter=["LP","HP","BP","BR"]
        self.Type_of_filter=ttk.Combobox(self.ventana_izquierda,values=values_filter, width=20,state="readonly")
        self.Type_of_filter.set("Select Type of Filter")
        self.Type_of_filter.grid(row=0,column=1,padx=10,pady=10)


#boton seleccionador
        button_select=Button(self.ventana_izquierda, text="   Select   ", command=self.Se_Apreto_Select)
        button_select.grid(row=0,column=3)




#Frecuencias y atenuaciones 

        self.label_wp0=Label(self.ventana_izquierda,text="Wp(-):")
        self.label_wa0=Label(self.ventana_izquierda,text="Wa(-):")
        self.label_Ap0=Label(self.ventana_izquierda,text="Ap:")
        self.label_Aa0=Label(self.ventana_izquierda,text="Aa:")

        self.label_wp=Label(self.ventana_izquierda,text="Wp:")
        self.label_wa=Label(self.ventana_izquierda,text="Wa:")

        self.label_wp1=Label(self.ventana_izquierda,text="Wp(+):")
        self.label_wa1=Label(self.ventana_izquierda,text="Wa(+):")




        self.entry_wp0=Entry(self.ventana_izquierda)
        self.entry_wa0=Entry(self.ventana_izquierda)
        self.entry_Ap0=Entry(self.ventana_izquierda)
        self.entry_Aa0=Entry(self.ventana_izquierda)


        self.entry_wp1=Entry(self.ventana_izquierda)
        self.entry_wa1=Entry(self.ventana_izquierda)




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


#tiempo de retardo para Bessel

        self.label_Tretardo=Label(self.ventana_izquierda,text="Tiempo de retardo:")
        self.entry_Tretardo=Entry(self.ventana_izquierda)
        self.label_microsec=Label(self.ventana_izquierda,text="microsec")

#boton graficar
        button_select=Button(self.ventana_izquierda, text="       Graph       ", command=self.Se_Apreto_Graph)
        button_select.grid(row=14,columnspan=20, padx=2, pady=2)

#-----------------------------------------------------------

        
#---VENTANA DERECHA ETAPA 1
#------------------------------------------------------------------------
    

        


        buttonMag = Button(self.ventana_derecha,text="Bode Magnitude",command=self.plotMag)
        buttonMag.grid(row=0, column=0,padx=40,pady=10)
        buttonPhase = Button(self.ventana_derecha,text="Bode Phase",command=self.plotPhase)
        buttonPhase.grid(row=0, column=1,padx=10,pady=10)
        buttonStep = Button(self.ventana_derecha,text="Step",command=self.plotStep)
        buttonStep.grid(row=0, column=2,padx=10,pady=10)
        buttonImp = Button(self.ventana_derecha,text="Impulse",command=self.plotImp)
        buttonImp.grid(row=0, column=3,padx=10,pady=10)
        buttonPZ = Button(self.ventana_derecha,text="Poles and Zeros",command=self.plotPZ)
        buttonPZ.grid(row=0, column=4,padx=10,pady=10)
        buttonGD = Button(self.ventana_derecha,text="Group Delay",command=self.plotGroupDelay)
        buttonGD.grid(row=0, column=5,padx=10,pady=10)
       



        graph = Canvas(self.ventana_derecha)
        graph.grid(row=1, columnspan=1000,padx=10,pady=10)

        f = Figure()
        self.axis = f.add_subplot(111)

        self.dataPlot = FigureCanvasTkAgg(f, master=graph)
        self.dataPlot.draw()
        self.dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.nav = NavigationToolbar2Tk(self.dataPlot, self.ventana_inferior)
        self.nav.update()
        self.dataPlot._tkcanvas.pack(side=TOP, expand=True)
       


#-----------------------------------------------------------------------------------------
#-----VENTANA IZQUIERDA ETAPA 2
#-----------------------------------------------------------------------------------------

        graph_polos = Canvas(self.ventana_izquierda2)
        graph_polos.grid(row=0, column=0,padx=10,pady=10)

        fig = Figure()
        self.axis2 = fig.add_subplot(111)

        self.dataPlot2 = FigureCanvasTkAgg(fig, master=graph_polos)
        self.dataPlot2.draw()
        self.dataPlot2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.nav2 = NavigationToolbar2Tk(self.dataPlot2, self.ventana_inferior2)
        self.nav2.update()
        self.dataPlot2._tkcanvas.pack(side=TOP, expand=True)
        
        

        self.root.mainloop()

if __name__ == "__main__":
    ex = graphs()