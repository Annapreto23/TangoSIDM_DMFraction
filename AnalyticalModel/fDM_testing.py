# File to test if the semi-analytic model produces the same range of values for the dark matter fraction within Reff

######################## set up the environment #########################

#---standard python stuff
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import math

#---user modules
from sigma import GalaxyCrossSectionCalculator
from data_process import classhalo
from findingr1 import calculate_mass
import profiles as pr


params = {
    "font.size": 15,
    "font.family": "Arial Black",
    "text.usetex": True,
    "mathtext.fontset": "custom",
    "figure.figsize": (5, 6),
    "figure.subplot.left": 0.15,
    "figure.subplot.right": 0.95,
    "figure.subplot.bottom": 0.16,
    "figure.subplot.top": 0.95,
    "figure.subplot.wspace": 0.3,
    "figure.subplot.hspace": 0.3,
    "lines.markersize": 2,
    "lines.linewidth": 1.5,
}
plt.rcParams.update(params)


folder = "../TangoSIDM_DMFraction/data/Simulation_datasets/TangoSIDM/"
file_paths = glob.glob(folder + "*.hdf5")

files_to_remove = glob.glob(folder + "*old.hdf5")


for file in files_to_remove:
    if file in file_paths:
        file_paths.remove(file)

file_names = ["Reference SigmaVel30", "WSFB SigmaVel30","WSFB CDM","Reference CDM","WSFB SigmaVel60","Reference SigmaVel60"]

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

        r1 = pr.r1(halo_contra,sigmamx=halo.ReCrossSection[i],tage=10)
        radius = np.logspace(-3, 3, 200)
        rhodm0,sigma0,rho_iso,Vc,rad = pr.stitchSIDMcore(r1,halo_contra,disk)
        rho_iso = np.concatenate((rho_iso, halo_contra.rho(np.arange(rad[-1], radius[-1]))[1:]))
        rad = np.concatenate((rad, np.arange(rad[-1], radius[-1])[1:]))

        
        halo_init = halo_init.rho(radius)
        halo_contra = halo_contra.rho(radius)
        disk = disk.rho(radius)

        
        # Calculate the masses within the effective radius Reff
        Ms_val = calculate_mass(Reff, disk, radius)
        Mdm_val = calculate_mass(Reff, rho_iso, rad)
        if halo.ReCrossSection[i] == 0:
            Mdm_val = calculate_mass(Reff, halo_contra, radius)

        # Calculate the dark matter fraction (fDM)
        fDM_val = Mdm_val / (Mdm_val + Ms_val)
        fDM_sim_val = np.interp(Reff, halo.AxisRadius, halo.fDM[:, i])
        Mb_tot_sim_val = log_stellar_mass
        Mb_tot_val = 2 * calculate_mass(R12, disk, radius) # Mb(R1/2) = Mb/2

        # Store the values in the arrays
        Mb_tot.append(Mb_tot_val)
        Mb_tot_sim.append(10 ** Mb_tot_sim_val)
        Ms.append(Ms_val)
        Mdm.append(Mdm_val)
        fdm.append(fDM_val)
        fdm_sim.append(fDM_sim_val)
    
    return Ms, Mdm, fdm, fdm_sim, Mb_tot, Mb_tot_sim

def plot_fDM_vs_Mb_tot(fdm, fdm_sim, Mb_tot, Mb_tot_sim, ax):
    df = pd.DataFrame({
        'fDM': fdm,
        'fDM_sim': fdm_sim,
    })
    y = np.linspace(-1, 2, 20)
    x = y
    ax.plot(x, y, linestyle = '--', label='x = y', linewidth= 2)

    # Plot using seaborn
    #sns.scatterplot(data=df, x='fDM_sim', y='fDM', ax=ax)
    sns.regplot(data=df, x='fDM_sim', y='fDM', ax=ax, ci = None, scatter=True, color='red', scatter_kws={'linewidths':0.1,'edgecolor':'white'}, line_kws={'linewidth':2}, label ='linear regression')

    ax.set_xlabel(r'$f_{\mathrm{DM, sim}}$')
    ax.set_ylabel(r'$f_{\mathrm{DM}}$')
    ax.set_xticks(np.arange(0, 1.1, 0.2)) 
    ax.set_yticks(np.arange(0, 1.1, 0.2)) 
    ax.set_ylim([0, 1])
    ax.set_xlim([0, 1])
    ax.grid(alpha = 0.5)

def compute_and_plot(file_path, type='all', ax=None):
    halo = classhalo(file_path, type)
    # Process all galaxies
    Ms, Mdm, fdm, fdm_sim, Mb_tot, Mb_tot_sim = process_all_galaxies(halo, file_path, type)
    # Plot the results
    plot_fDM_vs_Mb_tot(np.array(fdm), fdm_sim, Mb_tot, Mb_tot_sim, ax)





if __name__ == "__main__":
    num_files = len(file_paths)
    ncols = 3
    nrows = math.ceil(num_files / ncols)  # Calculate the number of rows needed

    fig, axes = plt.subplots(nrows, ncols)

    for i, file in enumerate(file_paths):
        row = i // ncols
        col = i % ncols
        ax = axes[row, col]
        compute_and_plot(file, ax=axes[row, col])
        ax.set_title(file_names[i])  # Set the title to the filename

    # Hide any unused subplots
    for i in range(num_files, nrows * ncols):
        row = i // ncols
        col = i % ncols
        fig.delaxes(axes[row, col])

    
    fig.subplots_adjust(hspace=0.5, wspace=0.4, top=0.90)
    handles = [plt.Line2D([], [], color='red', label='linear regression'),
           plt.Line2D([], [], color='blue', linestyle='--', label='x = y')]

    fig.legend(handles, ['Linear regression', 'x = y'], loc='upper center', ncol=2, borderaxespad=0.1, framealpha=0)
    plt.tight_layout(pad = 30)
    plt.show()




