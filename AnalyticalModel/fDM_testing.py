######################## set up the environment #########################

#---standard python stuff
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#---user modules
from sigma import GalaxyCrossSectionCalculator
from data_process import classhalo
from findingr1 import calculate_mass

file_path = "../TangoSIDM_DMFraction/data/Simulation_datasets/TangoSIDM/Halo_data_L025N376ReferenceSigmaVelDep30Anisotropic.hdf5"
type = 'all'
halo = classhalo(file_path, type)

def process_all_galaxies(halo, file_path, type):
    Ms = []
    Mdm = []
    fdm = []
    fdm_sim = []
    Mb_tot = []
    Mb_tot_sim = []

    for i in range(len(halo.Mstar)):
        log_stellar_mass = halo.Mstar[i]
        Reff = halo.GalaxyProjectedHalfLightRadius[i]
        R12 = halo.GalaxyHalfLightRadius[i]

        calculator = GalaxyCrossSectionCalculator(file_path, i, type)
        halo_init, halo_contra, disk = calculator.compute_profiles()

        radius = np.logspace(-3, 3, 200)
        halo_init = halo_init.rho(radius)
        halo_contra = halo_contra.rho(radius)
        disk = disk.rho(radius)



        # Calculate the masses within the effective radius Reff
        Ms_val = calculate_mass(Reff, disk, radius)
        Mdm_val = calculate_mass(Reff, halo_contra, radius)

        # Calculate the dark matter fraction (fDM)
        fDM_val = Mdm_val / (Mdm_val + Ms_val)
        fDM_sim_val = np.interp(Reff, halo.AxisRadius, halo.fDM[:, i])
        Mb_tot_sim_val = log_stellar_mass
        Mb_tot_val = 2*calculate_mass(R12, disk, radius) #Mb(R1/2) = Mb/2


        # Store the values in the arrays
        Mb_tot.append(Mb_tot_val)
        Mb_tot_sim.append(10**Mb_tot_sim_val)
        Ms.append(Ms_val)
        Mdm.append(Mdm_val)
        fdm.append(fDM_val)
        fdm_sim.append(fDM_sim_val)
    
    return Ms, Mdm, fdm, fdm_sim, Mb_tot, Mb_tot_sim


def plot_fDM_vs_Mb_tot(fdm, fdm_sim, Mb_tot, Mb_tot_sim):
    plt.figure(figsize=(10, 6))
    
    df_model = pd.DataFrame({
        'Mb_tot': Mb_tot,
        'fDM': fdm,
        'type': 'model'
    })

    # Create DataFrame for simulation data
    df_sim = pd.DataFrame({
        'Mb_tot': Mb_tot_sim,
        'fDM': fdm_sim,
        'type': 'simulation'
    })

    # Plot using seaborn
    sns.regplot(data=df_model, x='Mb_tot', y='fDM', label = 'model', scatter = True)
    sns.regplot(data=df_sim, x='Mb_tot', y='fDM', label = 'simulation', scatter = True)

    plt.xlabel(r'Stellar Mass [$M_\odot$]')
    plt.ylabel(r'$f_{\mathrm{DM}}$')
    plt.legend()
    plt.xscale('log')
    plt.ylim([0,1])
    plt.grid(True)
    plt.show()

# Process all galaxies
Ms, Mdm, fdm, fdm_sim, Mb_tot, Mb_tot_sim = process_all_galaxies(halo, file_path, type)

# Plot the results
plot_fDM_vs_Mb_tot(np.array(fdm), fdm_sim, Mb_tot, Mb_tot_sim)