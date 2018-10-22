import math as m


class General_aprox(object):
    def __init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas, tipo, a):
        self.As=As
        self.Ap=Ap
        self.wp=wp
        self.ws=ws
        self.wpMenos=wpMenos
        self.wpMas=wpMas
        self.wsMenos=wsMenos
        self.wsMas=wsMas
        self.tipo=tipo
        self.wsn=0
        self.b=0 #ancho de banda
        self.a=a #porcentaje de desnormalizacion
        self.polos=[]
        self.zeros=[]
        if (self.tipo == "BP") or (self.tipo == "BR"):
            self.b=(self.wpMas-self.wpMenos)/m.sqrt(self.wpMas*self.wpMenos)
        self.normalizacion()
        return;

    def normalizacion(self):
        if (self.tipo == "LP"):
            self.wsn=((self.ws)/(self.wp))
        elif (self.tipo == "HP"):
            self.wsn=((self.wp)/(self.ws))
        elif(self.tipo == "BP"):
            self.wsn=(self.wsMas-self.wsMenos)/(self.wpMas-self.wpMenos)
        elif(self.tipo=="BR"):
            self.wsn=(self.wpMas-self.wpMenos)/(self.wsMas-self.wsMenos)
        else:
            wsn=1
        return;



        

        
   


