######################## set up the environment #########################

#---standard python stuff
import numpy as np 
import matplotlib.pyplot as plt
import random

#---user modules
from sigma import GalaxyCrossSectionCalculator
from data_process import classhalo

file_path = "../TangoSIDM_DMFraction/data/Simulation_datasets/TangoSIDM/Halo_data_L025N376ReferenceSigmaVelDep60Anisotropic.hdf5"
type = 'disk'
halo = classhalo(file_path, type)


# --- plotting the cross section as a function of radius
i = random.randint(0, len(halo.Mstar))
calculator = GalaxyCrossSectionCalculator(file_path, i, type)
sigma, true_sigma, r1, dist = calculator.run()
gap_percentage = np.abs(true_sigma - sigma) / true_sigma * 100
Reff = calculator.halo.GalaxyProjectedHalfLightRadius[i]

print(f"The cross section following the semi-analytic model is {sigma:.2f} cm^2/g")
print(f"The simulated galaxy's cross section (mean cross section at R1) is {true_sigma:.2f} cm^2/g")
print(f"The difference represents {gap_percentage:.2f}% of the expected value.")


plt.figure()
halo_init, halo_contra = calculator.compute_profiles()
radius = np.logspace(np.log(min(calculator.halo.Density_radial_bins)), 3, 200)
halo_init = halo_init.rho(radius)
halo_contra = halo_contra.rho(radius)


plt.plot(calculator.halo.Density_radial_bins, calculator.halo.Dark_matter_Density_profile[:, i])
plt.plot(radius, halo_contra, label = r'$\rho_{\mathrm{contracted halo}}$')
plt.plot(radius, halo_init, label = r'$\rho_{NFW}$')
plt.axvline(x=r1, color='r', linestyle='--', label=f"r1 = {r1:.2f} kpc")
plt.axvline(x=Reff, color='b', linestyle='--', label=f"Reff = {Reff:.2f} kpc")
plt.xlabel('radius [kpc]')
plt.ylabel(r'$\rho$')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.show()

plt.figure()
plt.plot(calculator.halo.AxisRadius[:-1], calculator.halo.MeanCrossSection[:, i])
plt.axvline(x=r1, color='r', linestyle='--', label=f"r1 = {r1:.2f} kpc")
plt.axvline(x=Reff, color='b', linestyle='--', label=f"Reff = {Reff:.2f} kpc")

plt.axhline(sigma, color='r', linestyle='-', label="cross section within the semi-analytical model")
plt.xscale('log')
plt.ylabel(r'mean $\sigma_\mathrm{T}$/m [$\mathrm{cm}^2$.$\mathrm{g}^{-1}$]')
plt.xlabel('radius [kpc]')
plt.legend()
plt.show()






y_true = []
y_pred = []
error = []


for i in range(0, len(halo.Mstar)):
    calculator = GalaxyCrossSectionCalculator(file_path, i, type)
    sigma, true_sigma, r1, dist = calculator.run()
    gap_percentage = (true_sigma - sigma) / true_sigma * 100
    

    y_true.append(true_sigma)
    y_pred.append(sigma)
    error.append(gap_percentage)
   



    #print(f"The cross section following the semi-analytic model is {sigma:.2f} cm^2/g")
    #print(f"The simulated galaxy's cross section (mean cross section at Reff) is {true_sigma:.2f} cm^2/g")
    #print(f"The difference represents {gap_percentage:.2f}% of the expected value.")


y_true = np.array(y_true)
y_pred = np.array(y_pred)

plt.figure()
plt.plot(y_true, 'o')
plt.plot(y_pred, 'x')
plt.ylabel('sigma')
plt.xlabel('Galaxy Index')
plt.yscale('log')
plt.yticks([0,10], ['0','10'])
plt.ylim(0,10)
plt.grid()
#plt.show()


plt.figure()
plt.scatter(y_true, y_pred/y_true)
plt.xlabel('y_true')
plt.ylabel('y_pred/y_true')
plt.yscale('log')
plt.grid()
#plt.show()


plt.figure()
plt.plot(error, 'o')
plt.xlabel('Galaxy Index')
plt.ylabel('Error [%]')
plt.yscale('log')
plt.grid()
#plt.show()






