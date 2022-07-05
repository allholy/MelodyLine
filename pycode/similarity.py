'''
Find the similarities between the selected shape and the melody contours.
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from sympy import solve, Symbol

def coefs_function(coefs):
    ''' Makes a function from coefficients.
    Args:
        coefs (list): A list of coefficients. The size depends of the degree of the function.
    '''
    coefs.reverse()
    return lambda x: sum(c * x**degree for degree, c in enumerate(coefs))

def coefs_function_simple(x,coefs):
    coefs.reverse()
    return sum(c * x**degree for degree, c in enumerate(coefs))


def substract_integrals(function1, function2, high_border, low_border=0):
    ''' Take 2 functions and return the distance integral of it.
    '''
    print(function1,function2)

    I1,_ = integrate.quad(function1, low_border, high_border)
    I2,_ = integrate.quad(function2, low_border, high_border)
    return I2 - I1




def similarity(coefs, border, shape):
    '''
    Args:
        contour_coefs: Coefficients to make function of the contour.
        border:
        shape: Function of the shape given by the user.
    Returns:
        distance:
    '''
    contour = coefs_function(coefs) #contour function
    distance = substract_integrals(contour,shape,border)
    print("Distance:",distance)
    return distance


def distance_integral(y1_coefs, shape, b, a,low_border,high_border):
    '''
    '''

    # functions (callable)
    x = Symbol('x')
    y1 = coefs_function_simple(x,y1_coefs)
    y2 = shape_functions_simple(x,shape,b,a)

    # root of the difference of the functions.
    roots = solve(y1 - y2)
    print(roots)
    # keep the roots in the area we will calculate.
    roots_filtered = list(filter(lambda r: r > low_border and r < high_border, roots))
    print(roots_filtered)
    roots_filtered = [1,5,49]
    if not roots_filtered:
        distance = integrate(abs(y1 - y2), (x,low_border,high_border))
    else:
        distance = 0
        start = low_border
        for root in roots_filtered:
            distance =+ integrate(abs(y1 - y2), (x,start,root))
            start = root
            print(distance)
        distance = integrate(abs(y1 - y2), (x,root,high_border))

    norm_distance = distance / abs(high_border-low_border)
    return distance


def similarity_all(contour_coefs, borders, shape):
    ''' Similarity function for all the contours.
    Args:
    contour_coefs (list):
    '''
    distances = []
    for coefs, border in zip(contour_coefs,borders):
        distance = similarity(coefs, border, shape)
        distances.append(distance)
    print(" ..similarity computed \n -----------------------------------------------")
    return distances


def plot_similarity():
    #...plot
    #plt.plot(x, y_pred, color='red')
    #plt.plot(f2y, f2x)
    return 0


def return_sorted(data, paths):
    ''' Find maximum similarity. Sort from smaller to bigger number and map to their paths.
    Args:
        data (list): A list of values.
        paths (list): A list of paths of the same length.
    '''
    sorted_list = sorted((value, idx) for idx, value in enumerate(data))
    sorted_path_list = []
    for _,pos in sorted_list:
        sorted_path_list.append(paths[pos])
    return sorted_path_list



if __name__ == '__main__':
    #test

    from melody_extraction import final_contour,final_contours_all
    from default_shapes import shape_functions

    sounds = ['/mnt/DATA/thesis/mirlc2/sounds/Tin Whistle, Flutter, A (H1).ogg', '/mnt/DATA/thesis/code_extra/mirlc2/sounds/17Oboe.ogg', '/mnt/DATA/thesis/code_extra/mirlc2/sounds/120 oboe.ogg']

    #SHAPE = input("give a shape:")
    SHAPE="ascend"
    sh = shape_functions(SHAPE,440)
    # --one sound--
    c,b = final_contour(sounds[0])
    similarity(c,b,sh)

    # --all sounds--
    #c,b = final_contours_all(sounds)
    #similarity_all(c,b,sh)
    print("done")
