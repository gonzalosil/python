import math as m
from scipy import signal
#import control as c

class General_aprox(object):

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

    def __init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas,orden, tipo, a):
        super().__init__()
        self.As=As
        self.Ap=Ap
        self.wp=wp
        self.ws=ws
        self.n=orden   #ORDEN EN LA QUE SE QUIERE EL FILTRO
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

    def denormalization (self, type, W, n, poles=None, zeros=None, Wpmas=None, Wamenos=None, Wamas=None): #type se refiere al tipo de filtro que se desea
        #si es BP o BR W se usa como Wp- 
        if type == "LP":
            s = c.tf([1,0],[W])
            tf = c.tf([1],[1])
            if zeros != None:
                for k in range (0,len(zeros)):
                    tf = tf * (s-zeros(k))
            if poles != None:
                for k in range (0,len(poles)):
                    tf = tf * 1/(s-poles[k])
            #print(tf.den[0][0][len(tf.den[0][0])-1])
            k = tf.den[0][0][len(tf.den[0][0])-1]/tf.num[0][0][len(tf.num[0][0])-1]
            tf = signal.TransferFunction(k*tf.num[0][0], tf.den[0][0])
          #  k = tf.den[0][0][0]#/tf.num[0][0][len(tf.num[0][0])-1]

        elif type == "HP":
            s = c.tf([W],[1,0])
            tf = c.tf([1],[1])
            if zeros != None:
                for k in range (0,len(zeros)):
                    tf = tf * (s-zeros(k))
            if poles != None:
                for k in range (0,len(poles)):
                    tf = tf * 1/(s-poles[k])
            #print(tf.num[0][0])
            k = tf.den[0][0][0]/tf.num[0][0][0]
            tf = signal.TransferFunction(k*tf.num[0][0], tf.den[0][0])

        elif type == "BP":
            Wo=m.sqrt(Wpmas*W)
            B=(Wpmas-W)/Wo
            s1=c.tf([1,0],[Wo])
            s2=c.tf([Wo],[1,0])
            s=1/B*(s1+s2)
            tf = c.tf([1],[1])

            if zeros != None:
                for k in range (0,len(zeros)):
                    tf = tf * (s-zeros(k))
            if poles != None:
                for k in range (0,len(poles)):
                    tf = tf * 1/(s-poles[k])

            k =1# tf.den[0][0][len(tf.den[0][0])-1]/tf.num[0][0][0]

            tf = signal.TransferFunction(k*tf.num[0][0], tf.den[0][0])

        elif type == "BR":
            Wo=m.sqrt(Wpmas*W)
            B=(Wpmas-W)/Wo
            s1=c.tf([1,0],[Wo])
            s2=c.tf([Wo],[1,0])
            s=1/(1/B*(s1+s2))
            tf = c.tf([1],[1])

            if zeros != None:
                for k in range (0,len(zeros)):
                    tf = tf * (s-zeros(k))
            if poles != None:
                for k in range (0,len(poles)):
                    tf = tf * 1/(s-poles[k])

            k =1# tf.den[0][0][len(tf.den[0][0])-1]/tf.num[0][0][0]

            tf = signal.TransferFunction(k*tf.num[0][0], tf.den[0][0])
            
        return tf

    




        

        
   


