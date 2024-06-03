######################## set up the environment #########################

import profiles as pr
import galhalo as gh
from findingr1 import calculate_mass

# --standard python stuff
import numpy as np

# --for plot
import matplotlib.pyplot as plt

# -- parameters to explore
params = {
    'tage': 10., # [Gyr]
    'sigmamx': 0.5, # [cm^2/g]
    'lgMv': np.log10(2e12), # [M_sun]
    'c': 9.7,
    'lgMb': np.log10(6.2e10), # [M_sun]
    'Reff': 3. # [kpc]
}

param_labels = {
    'tage': r'tage $[Gyr]$',
    'sigmamx': r'$\sigma$/$m_x$ $[cm^2/g]$',
    'lgMv': r'lgMv $[M_\odot]$',
    'c': r'c',
    'lgMb': r'lgMb $[M_\odot]$',
    'Reff': r'Reff $[kpc]$'
}

r_FullRange = np.logspace(-3, 3, 200) # [kpc] for plotting the full profile


def computation(params):
    # Extract parameters
    tage, sigmamx, lgMv, lgMb, c, Reff = params.values()
    r0 = Reff / (1 + np.sqrt(2))

    # Initialize with baryons
    Mv = 10.**lgMv
    Mb = 10.**lgMb
    halo_init = pr.NFW(Mv, c, Delta=100., z=0.)
    disk = pr.Hernquist(Mb, r0)
    halo_contra = gh.contra(r_FullRange, halo_init, disk)[0] # Adiabatically contracted CDM halo

    # Find r_1
    r1 = pr.r1(halo_contra, sigmamx=sigmamx, tage=tage)

    # With baryon
    rhodm0, sigma0, rho, Vc, r = pr.stitchSIDMcore(r1, halo_contra, disk)
    rho = np.concatenate((rho, halo_contra.rho(np.arange(r[-1], r_FullRange[-1]))[1:]))
    radius = np.concatenate((r, np.arange(r[-1], r_FullRange[-1])[1:]))

    return disk.rho(radius), rho, radius

def calculate_fDM(params):
    # Compute densities
    rho_disk, rho, r = computation(params)

    # Calculate masses
    Mdm = calculate_mass(params['Reff'], rho, r)
    Ms = calculate_mass(params['Reff'], rho_disk, r)
    fDM = Mdm / (Mdm + Ms)

    return fDM

def plot_fDM(quantities, varying_params, params):
    primary_var = varying_params[0]  # Primary variable to vary
    primary_values = quantities[0]   # Values for the primary variable

    plt.figure(figsize=(10, 6))
    
    # Loop over any additional quantities (if provided)
    for i, secondary_values in enumerate(quantities[1:], start=1):
        for secondary_val in secondary_values:
            fDM_values = []
            if secondary_val is not None:
                params[varying_params[i]] = secondary_val  # Set secondary variable
            for x in primary_values:
                params[primary_var] = x  # Set primary variable
                fDM = calculate_fDM(params)
                fDM_values.append(fDM)
            
            # Label for the secondary variable
            label = f'{param_labels[varying_params[i]]}={secondary_val:.2f}' if secondary_val is not None else None
            plt.plot(primary_values, fDM_values, marker='o', linestyle='-', label=label)
    
    # Generate title excluding the varying parameters
    title_parts = [f'{key}={value:.2f} {param_labels[key]}' for key, value in params.items() if key not in varying_params]
    title = ', '.join(title_parts)
    
    plt.xlabel(param_labels[primary_var])
    plt.ylabel(r'$f_{DM}$')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


# -- quantity on the xaxis
quantity1 =  np.linspace(8, 12, 10) 

# -- quantity of the different lines
quantity2 = np.linspace(8.5, 11.5, 5)

# -- quantities to plot 
quantities = [quantity1, quantity2]

# -- name of the quantities to plot
varying_params = ['c','lgMb']    

# -- plot
plot_fDM(quantities, varying_params, params)