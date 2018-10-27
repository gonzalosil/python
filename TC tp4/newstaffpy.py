
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

      #def Se_Apreto_Graph_Etapas_Polos(self):

      # aux=[]
      # arreglo_TF=[]
      # for i in range (0,self.List_Etapas_Polos.size()):
      #     extra=complex(self.List_Etapas_Polos.get(i))
      #     control=np.conjugate(extra)
      #     if( cuentas.comparar(extra,control)):
      #        aux.append(extra)
      #        self.TransferFun_Etapa2=scipy.signal.ZerosPolesGain([],[(np.abs(np.real(extra)))],(np.abs(np.real(extra))))
      #        arreglo_TF.append(self.TransferFun_Etapa2)

      #     else:
      #         aux.append(extra)
      #         aux.append(np.conjugate(extra))
      #         self.TransferFun_Etapa2=scipy.signal.ZerosPolesGain([],[np.conjugate(extra),extra],(np.abs(extra))**2)
      #         arreglo_TF.append(self.TransferFun_Etapa2)