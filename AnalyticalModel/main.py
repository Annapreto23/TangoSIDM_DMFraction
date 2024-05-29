######################## set up the environment #########################

#---user modules credits : Arthur Fangzhou Jiang 2020 Caltech
import profiles as pr
import galhalo as gh

#---standard python stuff
import numpy as np

#---for plot
import matplotlib.pyplot as plt

#---for simulation data
from data_process import classhalo
import random


#---to find r1
from findingr1 import findr1


########################### simulation data loading ################################
folder = "../TangoSIDM_DMFraction/data/Simulation_datasets/TangoSIDM/"
file_path = folder+"Halo_data_L025N376ReferenceSigmaVelDep60Anisotropic.hdf5"

halo = classhalo(file_path, 'disk')



#---target one galaxy
max_value = len(halo.Mstar)
i = random.randint(0, max_value)
print(f"The galaxy chosen is the number {i}")
lgMv = halo.M200c[i] # [M_sun]
c = halo.c200c[i]
lgMb = halo.Mstar[i] # [M_sun]
r0 = halo.GalaxyHalfLightRadius[i] /(1+np.sqrt(2))# [kpc]
    
r_FullRange = np.logspace(-3,3,200) # [kpc] for plotting the full profile

############################### compute #################################

print('>>> computing SIDM profile ... ')


Mv = 10.**lgMv
Mb = 10.**lgMb

#---prepare the CDM profile 
halo_init = pr.NFW(Mv,c,Delta=100.,z=0.)
#---prepare the baryonic profile 
disk = pr.Hernquist(Mb,r0)
#---prepare the contracted DM halo profile 
halo_contra = gh.contra(r_FullRange,halo_init,disk)[0] # <<< adiabatically contracted CDM halo



############################ Finding r1 ################################

#r1, dist = find_best_match(halo.Dark_matter_Density_profile[:,i], halo_init.rho(halo.Density_radial_bins), halo.Density_radial_bins)
r1, dist = findr1(halo_contra.rho(r_FullRange), halo_init.rho(r_FullRange), r_FullRange)


print(f"r1 is :  {r1:.2f} kpc")
print(f"Distance between the two profiles is :  {dist:.2f}%")



# Visualisation
plt.plot(r_FullRange, halo_contra.rho(r_FullRange), label=r'$\rho_{\mathrm{iso}}$')
plt.plot(r_FullRange, halo_init.rho(r_FullRange), label=r'$\rho_{\mathrm{CDM}}$')
plt.plot(halo.Density_radial_bins, halo.Dark_matter_Density_profile[:,i], label = "simulated galaxy from TangoSIDM")
plt.axvline(x=r1, color='r', linestyle='--', label=f'r1 = {r1:.2f} kpc')
plt.xlabel('radius [kpc]')
plt.ylabel(r'$\rho$ [$M_\odot$.$\mathrm{kpc}^{-3}$]')
plt.legend()
plt.yscale('log')
plt.xscale('log')
plt.show()

#######################################

#---conversion

kpctocm = 3.086e16*1e5
kmtocm = 1e5


#--- velocity dispersion

vel_disp = np.interp(r1, halo.AxisRadius, halo.Dark_matter_Velocity_dispersion[9:,i]) #km/s
print(f"The velocity dispersion at r1 is: {vel_disp:.2f} km/s")

vel_disp *= kmtocm #cm/s


#--- galaxy's age

tage = 10*1e9 #m
tage *= 60*60*24*365

# --- density at r1 using halo.contra

#rho = np.interp(r1, halo.Density_radial_bins, halo.Dark_matter_Density_profile[:,i]) #Msol/kpc3
rhor1 = np.interp(r1, r_FullRange, halo_contra.rho(r_FullRange))
rho = rhor1
rho *= 2e30*1e3 #g/kpc3
rho /= kpctocm**3 #g/cm3

# --- function to compute the cross section 

def sigm(rho, vel, tage):
    return np.sqrt(np.pi)/(rho*vel*4*tage)

sigma = sigm(rho, vel_disp, tage)

print(f"The cross section following the semi-analytic model is {sigma:.2f} cm^2/g")
print(f"The simulated galaxy's cross section (mean cross section at Reff) is {halo.ReMeanCrossSection[i]:.2f} cm^2/g")

gap_percentage = np.abs(halo.ReMeanCrossSection[i] - sigma) / halo.ReMeanCrossSection[i] * 100
print(f"The difference represents {gap_percentage:.2f}% of the expected value.")


# --- plotting the cross section as a function of radius


Reff = halo.GalaxyProjectedHalfLightRadius[i]


plt.figure()
plt.plot(halo.AxisRadius[:-1], halo.MeanCrossSection[:, i])
plt.axvline(x=r1, color='r', linestyle='--', label=f"r1 = {r1:.2f} kpc")
plt.axvline(x=Reff, color='b', linestyle='--', label=f"Reff = {Reff:.2f} kpc")

plt.axhline(sigma, color='r', linestyle='-', label="cross section within the semi-analytical model")
plt.xscale('log')
plt.ylabel(r'mean $\sigma_\mathrm{T}$/m [$\mathrm{cm}^2$.$\mathrm{g}^{-1}$]')
plt.xlabel('radius [kpc]')
plt.legend()
plt.show()