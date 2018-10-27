
    #def combinar_funciones_transferencias(self):
    #   aux=[]
    #   arreglo_TF=[]
    #   for i in range (0,self.List_Etapas_Polos.size()):
    #       extra=complex(self.List_Etapas_Polos.get(i))
    #       control=np.conjugate(extra)
    #       if( cuentas.comparar(extra,control)):
    #          aux.append(extra)
    #       else:
    #           aux.append(extra)
    #           aux.append(np.conjugate(extra))
               
    #   arreglo_TF=scipy.signal.ZerosPolesGain([],[np.conjugate(extra),extra],1)
    #   self.set_filter_superponer(arreglo_TF) 


    #def set_filter_superponer(self,tf):
    #     self.axis3.clear()
    #     w,mag,phase=signal.bode(tf)
    #     self.plotMag_Etapa2(w,mag)