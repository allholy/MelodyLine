"""
Make shape that user asks.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# !! delta, rdelta not work!

def shape_functions_simple(x,shape,b,a=1):
    if shape == 'straight':
        fun = b
    if shape == 'ascend':
        fun = a*x + b
    if shape == 'descend':
        fun = -a*x + b
    if shape == 'delta':
        fun = 1
    if shape == 'rdelta':
        fun = 1
    return fun

def ascend(x,a,b):
    return (lambda x: a*x + b)

def straight(x,b):
    return (lambda x: b)

def descend(x,a,b):
    return (lambda x: -a*x + b)

def delta(x,a,b):
    s = signal.sawtooth(2*np.pi *x, 0.5)
    return (lambda x: a/2*s + b+a/2)

def rdelta(x,a,b):
    s = signal.sawtooth(2*np.pi *x, 0.5)
    return (lambda x: - a/2*s + b+a/2)

def shape_functions(shape,x,b=1,a=0):
    if shape == 'straight':
        fun = straight(x,b)
    if shape == 'ascend':
        fun = ascend(x,a,b)
    if shape == 'descend':
        fun = descend(x,a,b)
    if shape == 'delta':
        fun = delta(x,a,b)
    if shape == 'rdelta':
        fun = rdelta(x,a,b)
    return fun

def make_shape(shape,a,b, plot=False): #a=xmax, b=?
    #points = np.linspace(0, a, 100) #specify no. values
    points = np.arange(0,a,0.1) #the bigger, the more values (steady step)
    if shape == 'ascend':
        y = [ascend(x,a,b)(x) for x in points]
    if shape == 'descend':
        y = [descend(x,a,b)(x) for x in points]
    if shape == 'straight':
        y = [straight(x,b)(x) for x in points]
    if shape == 'delta':
        y = [delta(x,a,b)(x) for x in points]
    if shape == 'rdelta':
        y = [rdelta(x,a,b)(x) for x in points]
    if plot == True:
        plt.plot(y)
    return y

if __name__ == '__main__':
    #test
    make_shape('ascend',10,2, plot=True)
    print('done')
