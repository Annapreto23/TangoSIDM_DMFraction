## Datasets Description

| Units | Label     | Explanations 
|-------|-----------|--------------
| ---   | Name      | Galaxy Name
| Msun  | M*        | Stellar Mass 
| kpc   | Reff      | Effective Radius 
| ---   | fDM(Reff) | Dark Matter Fraction within Reff 
| ---   | ErrorfDM  | Error on fDM(Reff)         
| ---   | Q         | Quality Flag (Q<2 == poor)         



###  ATLAS3D


Dataset from the ATLAS3D project compiled from: 
- Capellari et al. (2013a)[https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C/abstract], 
- Capellari et al. (2013b)[https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1862C/abstract], and
- Capellari et al. (2011)[https://ui.adsabs.harvard.edu/abs/2011MNRAS.413..813C/abstract].
  
This ATLAS3D sample consists of 258 early-type galaxies (elliptical and lenticular galaxies). 
The stellar mass range covered by this dataset is $>= 6\times 10^9$ $M_{\odot}$.
 
We read the dark matter fractions from the dataset, the stellar mass-to-light ratio (which assumes a Salpeter IMF)
and the luminosity in the r-band. We derive the stellar masses as well as the effective radii. 

Cappellari employs the model 'JAM with NFW dark halo:' and assumes that the halo is spherical, characterized by a two-parameter 
double power-law NFW profile. They adopt the mass-concentration M200-c200 relation (Navarro et al. 1996) provided by Klypin et al.
(2011) to make the halo profile a unique function of its mass M200, thus extracting the fraction of dark matter and (M/L)_stars.
