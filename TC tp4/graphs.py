import matplotlib, sys
matplotlib.use('TkAgg')
import math 
import scipy
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.pyplot import plot,xscale,show
import matplotlib.patches as patches
from tkinter import *
from tkinter import ttk
import numpy as np
import Chevy_1 as Chevy
from matplotlib import pyplot
import Butterworth as Butter
import Chevy_2 as chevy2
import bessel as Bessel
import Transfer_Maker as TF
import cuentas
from numpy import *
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

        wp0=float(self.entry_wp0.get())
        wa0=float(self.entry_wa0.get())
        Ap=float(self.entry_Ap0.get())
        Aa=float(self.entry_Aa0.get())
        


        if self.Type_of_filter.get()=="LP" and self.Type_of_approx.get()!="Bessel":
            self.axis.add_patch(patches.Rectangle((0,Ap),wp0/(2*math.pi),50, color='magenta'))
            self.axis.set_ylim(0)
            self.axis.set_xlim(wp0/(4*math.pi),5*wa0/(2*math.pi))
            self.axis.add_patch(patches.Rectangle((wa0/(2*math.pi),0),5*wa0/(2*math.pi),Aa, color='magenta'))
        elif self.Type_of_filter.get()=="HP"and self.Type_of_approx.get()!="Bessel":
            self.axis.add_patch(patches.Rectangle((wp0/(2*math.pi),Ap),2*wp0/(2*math.pi),1000, color='magenta')) #rectangulo de la banda pasante
            self.axis.add_patch(patches.Rectangle((wa0/(8*math.pi),0),wa0/(2*math.pi),Aa, color='magenta'))
            self.axis.set_ylim(0)
            self.axis.set_xlim(wa0/(8*math.pi),2*wp0/(2*math.pi))
        elif self.Type_of_filter.get()=="BP"and self.Type_of_approx.get()!="Bessel":

            wp1=float(self.entry_wp1.get())#mas
            wa1=float(self.entry_wa1.get())
            wc_a=math.sqrt(wa0*wa1)
            wc_p=math.sqrt(wp0*wp1)
            self.axis.add_patch(patches.Rectangle((0,0),wa0/(2*math.pi),Aa, color='magenta')) #rectangulo de la primera banda atenuada
            self.axis.add_patch(patches.Rectangle((wc_p/(2*math.pi),Ap),wp1/(8*math.pi),1000, color='magenta')) #rectangulo de la banda pasante
            self.axis.add_patch(patches.Rectangle((wa1/(2*math.pi),0),10*wa1/(2*math.pi),Aa, color='magenta')) #rectangulo del ultima banda atenuada
        elif self.Type_of_filter.get()=="BR"and self.Type_of_approx.get()!="Bessel":
            wp1=float(self.entry_wp1.get())#mas
            wa1=float(self.entry_wa1.get())
            wc_a=math.sqrt(wa0*wa1)
            wc_p=math.sqrt(wp0*wp1)
            self.axis.add_patch(patches.Rectangle((0,Ap),wp0/(2*math.pi),1000, color='magenta')) #rectangulo de la primera banda pasante
            self.axis.add_patch(patches.Rectangle((wa0/(2*math.pi),0),wa1/(2*math.pi),Aa, color='magenta')) #rectangulo de la banda atenuada
            self.axis.add_patch(patches.Rectangle((wp1/(2*math.pi),Ap),10*wp1/(2*math.pi),1000, color='magenta')) #rectangulo del ultima banda pasante
        self.dataPlot.draw()



    def plotMag_Etapa2(self,w,mag):
        self.axis3.semilogx((w/(2*(math.pi))),-mag)
        self.axis3.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis3.set_xlabel("$f (Hz)$")
        self.axis3.set_ylabel("$Attenuation (dB)$")
        self.dataPlot3.draw()

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
        self.axis.plot(range(0,len(self.gd)),self.gd)
        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)
        self.axis.set_ylabel("$Group delay [ms]$")
        self.axis.set_xlabel("$Frequency [Hz]$")
        self.axis.set_xlim(0,200)
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

    def plotQ(self):
        self.axis.clear()

        print("Q")
        n=len(self.array_Q)
        self.axis.set_xlim(0,10)
        for i in range(0,n): #plotea los ceros
            self.axis.plot(n+5/(n+1)*i,self.array_Q[i],'o')

        self.axis.grid(color='grey',linestyle='-',linewidth=0.1)

        #self.axis.set_xlabel("$Real$")
        self.axis.set_ylabel("$Q$")

        self.dataPlot.draw()


#----funciones de seteo de tipo de filtro
#------------------------------------------------------------------------

    def set_filter(self):

        self.w,self.mag,self.phase = signal.bode(self.sys,None,10000)
        self.stepT,self.stepMag = signal.step(self.sys)
        self.impT,self.impMag = signal.impulse(self.sys)
        self.pzg = signal.tf2zpk(self.sys.num, self.sys.den)
        w,h=signal.freqs(self.sys.num,self.sys.den,worN=np.logspace(-1,50,1000))
        g=-diff(unwrap(angle(h)))/diff(w)
        self.gd = g      
        self.plotMag()
    
    def set_filter_etapa2(self,arreglo_de_tf):
        self.axis3.clear()
        for i in range(0,len(arreglo_de_tf)):
            print(arreglo_de_tf[i])
            w,mag,phase = signal.bode(arreglo_de_tf[i])
            self.plotMag_Etapa2(w,mag)

    
    def set_filter_superponer(self,tf):
         self.axis3.clear()
         w,mag,phase=signal.bode(tf)
         self.plotMag_Etapa2(w,mag)
        
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

        
        self.label_WARNING.grid_forget()

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
            wp0=float(self.entry_wp0.get())
        else:
            wp0=None

        if len(self.entry_wa0.get()) != 0:
            wa0=float(self.entry_wa0.get())
        else:
            wa0=None

        if len(self.entry_Ap0.get()) != 0:
            Ap0=float(self.entry_Ap0.get())
        else:
            Ap0=None

        if len(self.entry_Aa0.get()) != 0:
            Aa0=float(self.entry_Aa0.get())
        else:
            Aa0=None

        #frecuencias y atenuaciones 1
        if len(self.entry_wp1.get()) != 0:
            wp1=float(self.entry_wp1.get())
        else:
            wp1=None

        if len(self.entry_wa1.get()) != 0:
            wa1=float(self.entry_wa1.get())
        else:
            wa1=None

        #chequep que los datos sean dados correctamente\
        OK=0

        if FilterSelected=="LP":
            if wp0>wa0:
                OK=1
            elif Ap0>Aa0:
                OK=1
        elif  FilterSelected=="HP":
            if wa0>wp0:
                OK=1
            elif Ap0>Aa0:
                OK=1
        elif  FilterSelected=="BP":
            if wa0>wa1:
                OK=1
            elif wp0>wp1:
                OK=1
            elif wa0>wp0:
                OK=1
            elif Ap0>Aa0:
                OK=1
        elif FilterSelected=="BR":
            if wa0>wa1:
                OK=1
            elif wp0>wp1:
                OK=1
            elif wp0>wa0:
                OK=1
            elif Ap0>Aa0:
                OK=1
        else:
            OK=0

        
        if OK==1:
            self.label_WARNING.grid(row=16,columnspan=20)
        else:
            self.label_WARNING.grid_forget()

        print(wp0) #dato
        print(wa0) #dato
        print(wp1) #dato
        print(wa1) #dato
        print(Ap0) #dato
        print(Aa0) #dato

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

        self.Function=None

        if ApproxSelected=="Butterworth" and OK==0:

            self.Function=Butter.Butterworth(Aa0, Ap0, wp0, wa0, FilterSelected , Orden, Q, Denormalize_percentage, wp0,wp1, wa0, wa1)
            self.sys=Butter.Butterworth.get_transfer(self.Function)
            self.set_filter()
            self.array_Q=(self.Function.get_q())[:]
            
        elif  ApproxSelected=="Chebycheff"and OK==0:

            self.Function=Chevy.Chevy_1(Ap0, Aa0, wp0, wa0, FilterSelected, Orden, Q, wp1, wa1)
            self.sys=Chevy.Chevy_1.get_transfer(self.Function)
            self.set_filter()

        elif  ApproxSelected=="Chebycheff Inverso"and OK==0:

            self.Function=chevy2.Chevy_2(Ap0, Aa0, wp0, wa0, FilterSelected, Orden, Q, wp1, wa1)
            self.sys=chevy2.Chevy_2.get_transfer(self.Function)
            self.set_filter()

        elif ApproxSelected=="Bessel"and OK==0:

            #if(FilterSelected=="LP"):
            Tretardo=int(self.entry_Tretardo.get())
            print(Tretardo)
            self.Function=Bessel.Bessel(Aa0, Ap0, wp0, wa0,FilterSelected , Orden, Tretardo, wp0,wp1, wa0, wa1)
            self.sys=Bessel.Bessel.getTransfer(self.Function)
            self.set_filter()
        else:
           print("unknown")



        FilterSelected=self.Type_of_filter.get()

        if FilterSelected=="LP":
            

           self.labels_and_entrys_LPHP()
        elif  FilterSelected=="HP":
            self.labels_and_entrys_LPHP()
        elif  FilterSelected=="BP":
            self.labels_and_entrys_BPBS()
        elif FilterSelected=="BR":
            self.labels_and_entrys_BPBS()
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

        #-

        self.entry_wp1.grid_forget()
        self.entry_wa1.grid_forget()


        self.entry_wp1.delete(0, END)
        self.entry_wa1.delete(0, END)

        

        self.label_Hz.grid_forget()
        self.label_Hz.grid_forget()


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
        self.label_Hz=Label(self.ventana_izquierda,text="rad/s")
        self.label_Hz.grid(row=6,column=2)


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
            self.TransferMaker=TF.Transfer_Maker(self.sys.poles,self.sys.zeros)
            self.SegundaEtapa()

    def SegundaEtapa(self):
        
        self.values_Polos=self.TransferMaker.get_polos_separados()
        self.values_Ceros=self.TransferMaker.get_zeros_separados()


        self.combo_Polos=ttk.Combobox(self.Polos_Ceros,values=self.values_Polos, width=60,state="readonly")
        self.combo_Polos.set("Etapas de los Polos")
        self.combo_Polos.grid(row=1,column=0,padx=10,pady=10)
        self.combo_Polos.bind("<<ComboboxSelected>>", self.Selected_Polo_to_Graph)

        self.combo_Ceros=ttk.Combobox(self.Polos_Ceros,values=self.values_Ceros, width=60,state="readonly")
        self.combo_Ceros.set("Etapas de los Ceros")
        self.combo_Ceros.grid(row=1,column=1,padx=10,pady=10)
        self.combo_Ceros.bind("<<ComboboxSelected>>", self.Selected_Cero_to_Graph)



#funciones parte 2


    def Selected_Cero_to_Graph(self, event):
        Etapa_Selected=self.combo_Ceros.get()
        self.List_Etapas_Ceros.insert(END,Etapa_Selected)
    def Selected_Polo_to_Graph(self, event):
        Etapa_Selected=self.combo_Polos.get()
        self.List_Etapas_Polos.insert(END,Etapa_Selected)


    def Se_Apreto_Graph_Etapas_Polos(self):

      aux=[]
      arreglo_TF=[]
      for i in range (0,self.List_Etapas_Polos.size()):
          extra=complex(self.List_Etapas_Polos.get(i))
          control=np.conjugate(extra)
          if( cuentas.comparar(extra,control)):
             aux.append(extra)
             self.TransferFun_Etapa2=scipy.signal.ZerosPolesGain([],[(np.abs(np.real(extra)))],(np.abs(np.real(extra))))
             arreglo_TF.append(self.TransferFun_Etapa2)

          else:
              aux.append(extra)
              aux.append(np.conjugate(extra))
              self.TransferFun_Etapa2=scipy.signal.ZerosPolesGain([],[np.conjugate(extra),extra],(np.abs(extra))**2)
              arreglo_TF.append(self.TransferFun_Etapa2)

      self.set_filter_etapa2(arreglo_TF)



    def Se_Apreto_Graph_Etapas_Ceros(self):

       aux=[]
       arreglo_TF=[]
       for i in range (0,self.List_Etapas_Ceros.size()):
           extra=complex(self.List_Etapas_Ceros.get(i))
           control=np.conjugate(extra)
           if( cuentas.comparar(extra,control)):
              aux.append(extra)
              self.TransferFun_Etapa2=scipy.signal.ZerosPolesGain([(np.abs(np.real(extra)))],[],1/(np.abs(np.real(extra))))
              arreglo_TF.append(self.TransferFun_Etapa2)

           else:
               aux.append(extra)
               aux.append(np.conjugate(extra))
               self.TransferFun_Etapa2=scipy.signal.ZerosPolesGain([np.conjugate(extra),extra],[],1)
               arreglo_TF.append(self.TransferFun_Etapa2)

       self.set_filter_etapa2(arreglo_TF)

    def Click_Limpiar_Polos(self):
        self.axis3.clear()
        self.dataPlot3.draw()
        self.List_Etapas_Polos.delete(0,END)

    def Click_Limpiar_Ceros(self):
        self.axis3.clear()
        self.dataPlot3.draw()
        self.List_Etapas_Ceros.delete(0,END)

    def Click_ordenar(self):
        self.List_Orden_Q.delete(0,END)
        aux=[]
        for i in range (0,self.List_Etapas_Polos.size()):
           extra=complex(self.List_Etapas_Polos.get(i))
           aux.append(extra)
        if(self.List_Etapas_Ceros.size()):
           for i in range (0,self.List_Etapas_Ceros.size()):
                extra=complex(self.List_Etapas_Polos.get(i))
                aux.append(extra)
        test=TF.ordenar_a_partir_de_los_q(aux)
        for i in range (0,len(test)):
           self.List_Orden_Q.insert(END,test[i])
      
    def Se_Apreto_Superponer(self):
       aux=[]
       arreglo_TF=[]
       for i in range (0,self.List_Etapas_Polos.size()):
           extra=complex(self.List_Etapas_Polos.get(i))
           control=np.conjugate(extra)
           if( cuentas.comparar(extra,control)):
              aux.append(extra)
           else:
               aux.append(extra)
               aux.append(np.conjugate(extra))
               
       arreglo_TF=scipy.signal.ZerosPolesGain([],extra,1)
       self.set_filter_superponer(arreglo_TF) 

    def Se_Apreto_superponer_ceros(self):
       aux=[]
       arreglo_TF=[]
       for i in range (0,self.List_Etapas_Ceros.size()):
           extra=complex(self.List_Etapas_Ceros.get(i))
           control=np.conjugate(extra)
           if( cuentas.comparar(extra,control)):
              aux.append(extra)
           else:
               aux.append(extra)
               aux.append(np.conjugate(extra))
               
       arreglo_TF=scipy.signal.ZerosPolesGain(extra,[],1)
       self.set_filter_superponer(arreglo_TF) 

#------------------
#-----frames
#------------------
    def __init__(self):
        self.root = Tk()
        self.root.title("TP 4 - Grupo 6 - Teoria de Circuitos - 2018")

        self.Function=None
        self.array_Q=[]
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


        self.label_WARNING=Label(self.ventana_izquierda,text="Los datos no cumplen plantilla, vuelva a ingresarlos! ", font='arial', fg='red')

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
        button_Graph=Button(self.ventana_izquierda, text="       Graph       ", command=self.Se_Apreto_Graph)
        button_Graph.grid(row=15,columnspan=20, padx=2, pady=2)

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
        buttonQ = Button(self.ventana_derecha,text="Q",command=self.plotQ)
        buttonQ.grid(row=0, column=6,padx=10,pady=10)



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

        


        self.Polos_Ceros=Frame(self.ventana_izquierda2)
        self.Polos_Ceros.grid(row=0, column=0,padx=10,pady=10)

        self.Frame_Botones_Graficos_Sup=Frame(self.ventana_derecha2)
        self.Frame_Botones_Graficos_Sup.grid(row=0,column=0,padx=10,pady=10)





        #seleccionar las etapas que deseas graficar
        label_Select_etapa=Label(self.Polos_Ceros,text="Selecciona la etapa que deseas agregar a la lista:")
        label_Select_etapa.grid(row=0,columnspan=20)


        self.List_Etapas_Polos=Listbox(self.Polos_Ceros, width=50, height=7)
        self.List_Etapas_Polos.grid(row=2,column=0)
        self.List_Etapas_Polos.delete(0,END)

        self.List_Etapas_Ceros=Listbox(self.Polos_Ceros, width=50, height=7)
        self.List_Etapas_Ceros.grid(row=2,column=1)
        self.List_Etapas_Ceros.delete(0,END)

        self.Frame_botones_abajo_de_list=Frame(self.Polos_Ceros)
        self.Frame_botones_abajo_de_list.grid(row=3, column=0)
        self.Frame_botones_abajo_de_list_Z=Frame(self.Polos_Ceros)
        self.Frame_botones_abajo_de_list_Z.grid(row=3, column=1)
        self.Frame_botones_abajo_de_list_izq=Frame(self.Frame_botones_abajo_de_list)
        self.Frame_botones_abajo_de_list_izq.grid(row=0,column=0)
        self.Frame_botones_abajo_de_list_der=Frame(self.Frame_botones_abajo_de_list_Z)
        self.Frame_botones_abajo_de_list_der.grid(row=0,column=1)


        self.Limpiar_Lista_Polos = Button(self.Frame_botones_abajo_de_list_izq,text="Limpiar Polos", command=self.Click_Limpiar_Polos) 
        self.Limpiar_Lista_Polos.grid(row=0, column=0,padx=10,pady=10)
        self.Graph_List_Etapas_Polos = Button(self.Frame_botones_abajo_de_list_izq,text="Graficar Polos", command=self.Se_Apreto_Graph_Etapas_Polos) 
        self.Graph_List_Etapas_Polos.grid(row=0, column=1,padx=10,pady=10)
        self.Boton_Superpuesto_Polos = Button(self.Frame_botones_abajo_de_list_izq,text="Superponer Polos" ,command=self.Se_Apreto_Superponer)
        self.Boton_Superpuesto_Polos.grid(row=0, column=2,padx=10,pady=10)

        self.Limpiar_Lista_Ceros = Button(self.Frame_botones_abajo_de_list_der,text="Limpiar Ceros", command=self.Click_Limpiar_Ceros)  
        self.Limpiar_Lista_Ceros.grid(row=0, column=0,padx=10,pady=10)
        self.Graph_List_Etapas_Ceros = Button(self.Frame_botones_abajo_de_list_der,text="Graficar Ceros", command=self.Se_Apreto_Graph_Etapas_Ceros) 
        self.Graph_List_Etapas_Ceros.grid(row=0, column=1,padx=10,pady=10)
        self.Boton_Superpuesto_Ceros= Button(self.Frame_botones_abajo_de_list_der,text="Superponer Ceros", command=self.Se_Apreto_superponer_ceros) 
        self.Boton_Superpuesto_Ceros.grid(row=0, column=2,padx=10,pady=10)

        #grafico de polos
        graph_polos = Canvas(self.ventana_izquierda2, width=10, height=10)
        graph_polos.grid(row=1, column=0,padx=10,pady=10)
        fig = Figure()
        self.axis2 = fig.add_subplot(111)
        self.dataPlot2 = FigureCanvasTkAgg(fig, master=graph_polos)
        self.dataPlot2.draw()
        self.dataPlot2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.dataPlot2._tkcanvas.pack(side=TOP, expand=True)
        
#----------------------------------
#VENTANA DERECHA ETAPA 2
#---------------------------------
        label_OrdenEtapas=Label(self.ventana_derecha2,text="Ordenar etapas automaticamente")
        label_OrdenEtapas.grid(row=0,columnspan=20)


        self.List_Orden_Q=Listbox(self.ventana_derecha2, width=50, height=7)
        self.List_Orden_Q.grid(row=1,columnspan=20)
        self.List_Orden_Q.delete(0,END)

        self.boton_Odenar = Button(self.ventana_derecha2,text="Ordenar",command=self.Click_ordenar) 
        self.boton_Odenar.grid(row=2, columnspan=20)
        

        graph_Superpuestos = Canvas(self.ventana_derecha2)
        graph_Superpuestos.grid(row=3, column=0,padx=10,pady=10)
        figura = Figure()
        self.axis3 = figura.add_subplot(111)
        self.dataPlot3 = FigureCanvasTkAgg(figura, master=graph_Superpuestos)
        self.dataPlot3.draw()
        self.dataPlot3.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.nav3 = NavigationToolbar2Tk(self.dataPlot3, self.ventana_inferior2)
        self.nav3.update()
        self.dataPlot3._tkcanvas.pack(side=TOP, expand=True)

        self.root.mainloop()

if __name__ == "__main__":
    ex = graphs()
