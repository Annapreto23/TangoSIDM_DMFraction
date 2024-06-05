from scipy.integrate import fixed_quad
import numpy as np 
import profiles as pr



def dens(r, density, radius):
    return np.interp(r, radius, density)

mass = lambda r, density, radius: 4*np.pi*dens(r, density, radius)*r**2

def calculate_mass(r, density, radius):
    return fixed_quad(mass, 0, r, args=(density, radius))[0]

def findr1(halo_contra, disk, fDM, r, Reff):   
    gap = np.inf
    rho_iso_r1 = 0
    r1 = 0
    for i in np.logspace(-1,3, 50):
       rhodm0,sigma0,rho_iso,Vc,radius = pr.stitchSIDMcore(i,halo_contra,disk)
       rho_iso = np.concatenate((rho_iso, halo_contra.rho(np.arange(radius[-1], r[-1]))[1:]))
       radius = np.concatenate((radius, np.arange(radius[-1], r[-1])[1:]))
       Mdm = calculate_mass(Reff, rho_iso, radius)
       Ms = calculate_mass(Reff, disk.rho(r), r)
       f = Mdm/(Ms+Mdm)

       if abs(f-fDM) < gap:
           r1 = i
           rho_iso_r1 = rho_iso
           radius_r1 = radius
           gap = abs(f-fDM)
           final_f = f
           vel_disp = sigma0

    return r1, rho_iso_r1, radius_r1, gap, final_f, vel_disp

