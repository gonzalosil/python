import sympy as sp
from scipy import signal
from decimal import *
from numpy import roots, nditer
import numpy

DESMIN= 1e-6

def Obtener_coef(expr,var):
    num, denom = expr.as_numer_denom()

    return [sp.Poly(num, var).all_coeffs(), sp.Poly(denom, var).all_coeffs()]

def Expandir_coef(expr,var):
    data=Obtener_coef(expr,var)
    return data


def conseguir_tf(exp, var, poles = []):

    value = Expandir_coef(exp, var)

    my_subs = dict()
    my_subs[sp.I] = 1j

    for i in range(len(value[0])):
        value[0][i] = complex(value[0][i].evalf(subs=my_subs))
    for i in range(len(value[1])):
        value[1][i] = complex(value[1][i].evalf(subs=my_subs))
    print(value[0], value[1])

    tf = signal.lti(value[0], value[1])

    return tf


def comparar(a,b):
    result=numpy.abs(a-b)
    return (result < DESMIN)