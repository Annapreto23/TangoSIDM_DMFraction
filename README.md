# TangoSIDM_DMFraction


The TangoSIDM_DMFraction project in this repository is part of the project led by C. Correa (see tangosidm.com). The goal is to extract the dark matter fraction information within massive galaxies from simulation data and observations and compare them. Below, the reader will find information about the datasets included in the 'data' folder: it consists of 3 CSV files as we use 3 different samples to construct it.


## Datasets Description

### SPARC 
Only the SPARC dataset contains an array of radii, so we can only make this plot with this dataset. The dataset description is available on the website (http://astroweb.cwru.edu/SPARC/), here is an excerpt :
> SPARC is a database of 175 late-type galaxies (spirals and irregulars) with Spitzer photometry at 3.6 µm (tracing the stellar mass distribution) and high-quality HI+Hα rotation curves (tracing the gravitational potential out to large radii). SPARC spans a wide range in stellar masses (5 dex), surface brightnesses (>3 dex), and gas fractions.

Fore more, check the master paper "http://astroweb.cwru.edu/SPARC/".
The following quantities are extracted from the dataset:

- <span style="background-color: lightgray">fDM</span>: This represents the dark matter fraction.
- <span style="background-color: lightgray">radius</span>: This represents the radius (kpc).
- <span style="background-color: lightgray">sigma_fdm</span>: This represents the uncertainty on the dark matter fraction.

These quantities are obtained using the following code:
```python
fDM = string_to_array(df['fDM'][i])
radius = string_to_array(df['Radius'][i])
sigma_fdm = string_to_array(df['sigma_fdm'][i])
radius = string_to_array(df['Radius'][i])
sigma_fdm = string_to_array(df['sigma_fdm'][i])
```

For our analysis, we employ a constant mass-to-light ratio of $Γ = 0.5 M⊙/L⊙$, as determined by stellar population synthesis models (Schombert & McGaugh 2014) based on a Chabrier IMF. Following Lelli et al. (2016) and utilizing their rotation curve calculations, we compute the fraction of dark matter using, with $\Gamma_{bul} = 1.4\Gamma_{disk}$ and $\Gamma_{disk} = 0.5$ : 

$V_{bar}^2 = V_{gas}|V_{gas}| + \Gamma_{disk}V_{disk}|V_{disk}| + \Gamma_{bul}V_{bul}|V_{bul}|$

$f_{DM} = \frac{{V_{obs}^2 - V_{bar}^2}}{{V_{obs}^2}}$


###  Cappellari+16


The dataset from Cappellari (merged from 2 datasets : https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C/abstract and https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1862C/abstract) consists of early-type galaxies, which include elliptical galaxies (Es) and lenticular galaxies (S0s). The dataset specifically includes a sample of 260 such galaxies. The stellar mass range covered by this dataset is approximately greater than or equal to $6 \times 10^9$ solar masses ($M_{\odot}$). We directly use the dark matter fraction from the dataset and the mass-to-light ratio (Cappellari assuming a Salpeter IMF) and using also the luminosity in the r-band, we derive the stellar mass. To have the stellar masses calculated assuming a Chabrier IMF we need to substract the stellar mass from 0.25 dex (section 4.1 in this work https://ui.adsabs.harvard.edu/abs/2024MNRAS.tmp..878L/abstract). Cappellari employs the model 'JAM with NFW dark halo:' and assumes that the halo is spherical, characterized by a two-parameter double power-law NFW profile. They adopt the mass-concentration M200-c200 relation (Navarro et al. 1996) provided by Klypin et al. (2011) to make the halo profile a unique function of its mass M200, thus extracting the fraction of dark matter and (M/L)_stars.



### Bezanson+15

The dataset from Bezanson et al. 2015 includes 103  early- and late-type, or alternatively quiescent an 
star-forming, galaxies. They use a Chabrier IMF for the stellar mass M*. We use their velocity dispersion measurements (details in section 2.5 https://ui.adsabs.harvard.edu/abs/2015ApJ...799..148B/abstract) and then calculate the fDM within the effective radius $R_e$ with : 

$f_{DM} = 1 - \frac{M*}{M_{dyn}}$

with $M_{dyn}$ extracted from the Virial theorem : 

$M_{dyn}(r \textless R_e) = \frac{K R_e\sigma^2(r\textless R_e)}{G}$

and assuming $K = 5$ (http://dx.doi.org/10.1111/j.1365-2966.2005.09981.x).
