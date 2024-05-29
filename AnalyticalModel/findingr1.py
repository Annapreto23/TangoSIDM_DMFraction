from scipy.integrate import fixed_quad
import numpy as np



def calculate_derivative(density, r):
    """Calculate the numerical derivative of the density profile."""
    return np.gradient(density, r)

def calculate_distance(deriv1, deriv2):
    """Calculate the distance between two derivative profiles."""
    return np.mean((np.abs(deriv1 - deriv2)) / np.abs(deriv1) * 100)

def dens(r, density, radius):
    return np.interp(r, radius, density)

mass = lambda r, density, radius: 4*np.pi*dens(r, density, radius)*r**2

def findr1(density1, density2, r):
    
    n = len(density1)
    best_r = []
    thresold = 3
    best_distance = []

    for i in range(0, n - thresold):
        deriv1 = calculate_derivative(density1[i:i+thresold], r[i:i+thresold])
        deriv2 = calculate_derivative(density2[i:i+thresold], r[i:i+thresold])
        dist = calculate_distance(deriv1, deriv2)
        M1 = fixed_quad(mass, 0, r[i], args=(density1, r))[0]
        M2 = fixed_quad(mass, 0, r[i], args=(density2, r))[0]
        #print("masses are ", M1/1e8, " and ",M2/1e8)
        distM = calculate_distance(M1, M2)
        #print("distM is ", distM)
        if dist < 25 and distM < 25:
            print("Condition completed")
            return r[i], dist
        else:
            best_distance.append(dist)
            best_r.append(i)

    mini = np.argmin(best_distance)

    return r[best_r[mini]], best_distance[mini]

