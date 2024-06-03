######################## set up the environment #########################

#---standard python stuff
import numpy as np 
import matplotlib.pyplot as plt
import random

#---user modules
from sigma import GalaxyCrossSectionCalculator
from data_process import classhalo
from findingr1 import calculate_mass

file_path = "../TangoSIDM_DMFraction/data/Simulation_datasets/TangoSIDM/Halo_data_L025N376ReferenceSigmaVelDep60Anisotropic.hdf5"
type = 'disk'
halo = classhalo(file_path, type)

i = random.randint(0, len(halo.Mstar)-1)
#i = 10
log_stellar_mass =  halo.Mstar[i]
Reff = halo.GalaxyProjectedHalfLightRadius[i]
calculator = GalaxyCrossSectionCalculator(file_path, i, type)
sigma, true_sigma, r1, rho_iso, r_iso = calculator.run()
print(f"r1 found is : {r1:.2f}")
gap_percentage = np.abs(true_sigma - sigma) / true_sigma * 100
halo_init, halo_contra, disk = calculator.compute_profiles()
radius = np.logspace(-3, 3, 200)
halo_init = halo_init.rho(radius)
halo_contra = halo_contra.rho(radius)
disk = disk.rho(radius)

# Printing the galaxy's propreties and model predictions

print("Galaxy's index ", i)
print(r"Galaxy's $log_{10}$ stellar mass [$M_\odot$] ", log_stellar_mass)
print("Galaxy's effective radius Reff [kpc] ", Reff)

print(f"The cross section following the semi-analytic model is {sigma:.2f} cm^2/g")
print(f"The simulated galaxy's cross section (mean cross section at R1) is {true_sigma:.2f} cm^2/g")
print(f"The difference represents {gap_percentage:.2f}% of the expected value.")


# --- Plotting

#Plot with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 15))

# Plot dark matter velocity dispersion
ax1.plot(calculator.halo.AxisRadius, calculator.halo.Dark_matter_Velocity_dispersion[9:, i])
ax1.axvline(x=r1, color='r', linestyle='--', label=f"r1 = {r1:.2f} kpc")
ax1.axvline(x=Reff, color='b', linestyle='--', label=f"Reff = {Reff:.2f} kpc")
ax1.set_xlabel('radius [kpc]')
ax1.set_ylabel(r'$vel_{disp}$ [$km.s^{-1}$]')
ax1.set_yscale('log')
ax1.set_xscale('log')
ax1.legend()
ax1.set_title(f'Galaxy Index: {i}, $log_{{10}}$ Stellar Mass: {halo.Mstar[i]:.2f}, Effective Radius: {Reff:.2f} kpc')

# Plot mean cross section
ax2.plot(calculator.halo.AxisRadius[:-1], calculator.halo.CrossSection[:, i])
ax2.axvline(x=r1, color='r', linestyle='--', label=f"r1 = {r1:.2f} kpc")
ax2.axvline(x=Reff, color='b', linestyle='--', label=f"Reff = {Reff:.2f} kpc")
ax2.axhline(sigma, color='r', linestyle='-', label="cross section within the semi-analytical model")
ax2.set_xscale('log')
ax2.set_ylabel(r'mean $\sigma_\mathrm{T}$/m [$\mathrm{cm}^2$.$\mathrm{g}^{-1}$]')
ax2.set_xlabel('radius [kpc]')
ax2.legend()
ax2.set_title(f'Galaxy Index: {i}, $log_{{10}}$ Stellar Mass: {halo.Mstar[i]:.2f}, Effective Radius: {Reff:.2f} kpc')

plt.tight_layout()
#plt.show()


plt.figure()
plt.plot(calculator.halo.Density_radial_bins, calculator.halo.Dark_matter_Density_profile[:, i])
plt.plot(radius, halo_contra, label = r'$\rho_{\mathrm{contracted halo}}$')
plt.plot(r_iso, rho_iso, label = r'$\rho_{iso}$')
plt.axvline(x=r1, color='r', linestyle='--', label=f"r1 = {r1:.2f} kpc")
plt.axvline(x=Reff, color='b', linestyle='--', label=f"Reff = {Reff:.2f} kpc")
plt.xlabel('radius [kpc]')
plt.ylabel(r'$\rho$')
plt.yscale('log')
plt.xscale('log')
plt.title(f'Galaxy Index: {i}, $log_{{10}}$ Stellar Mass: {log_stellar_mass:.2f}, Effective Radius: {Reff:.2f} kpc')
plt.legend()
plt.show()


