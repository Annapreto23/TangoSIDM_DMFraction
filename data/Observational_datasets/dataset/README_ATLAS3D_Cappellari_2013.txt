## Datasets Description

#================================================================================
#Description of file: ATLAS3D.csv
#--------------------------------------------------------------------------------
#    Units         Label                  Explanations
#--------------------------------------------------------------------------------
#    Msun          M*                     Stellar Mass
#    kpc           Reff                   Effective Radius at [3.6]
#    ---           fDM(Reff)              Dark Matter Fraction within Reff
#    ---           sigma_fdm(Reff)        Error on fDM(Reff)
#================================================================================

###  Cappellari+13


The dataset from Cappellari (merged from 2 datasets : https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C/abstract and 
https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1862C/abstract) consists of early-type galaxies, which include elliptical galaxies
(Es) and lenticular galaxies (S0s). The dataset specifically includes a sample of 260 such galaxies. The stellar mass range covered
by this dataset is approximately greater than or equal to $6\times 10^9$ solar masses ($M_{\odot}$). We directly use the dark 
matter fraction from the dataset and the mass-to-light ratio (Cappellari assuming a Salpeter IMF) and using also the luminosity in 
the r-band, we derive the stellar mass. To have the stellar masses calculated assuming a Chabrier IMF we need to substract the 
stellar mass from 0.25 dex (section 4.1 in this work https://ui.adsabs.harvard.edu/abs/2024MNRAS.tmp..878L/abstract). 
Cappellari employs the model 'JAM with NFW dark halo:' and assumes that the halo is spherical, characterized by a two-parameter 
double power-law NFW profile. They adopt the mass-concentration M200-c200 relation (Navarro et al. 1996) provided by Klypin et al.
(2011) to make the halo profile a unique function of its mass M200, thus extracting the fraction of dark matter and (M/L)_stars.

