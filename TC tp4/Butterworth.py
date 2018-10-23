import General_aprox as General

class Butterworth(object):
    def __init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas, tipo, a):
        
        General.General_aprox.__init__(self, As, Ap, wp, ws, wpMenos, wpMas, wsMenos, wsMas, tipo, a)
        self.epButter()
        self.nButter()
        self.polosButter()



