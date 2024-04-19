## Dataset Description

#================================================================================
#Description of file: ../dataset/SPARC.csv
#--------------------------------------------------------------------------------
#    Units         Label                  Explanations
#--------------------------------------------------------------------------------
#    ---           Galaxy                 Galaxy Name
#    Msun          M*                     Stellar Mass
#    kpc           Reff                   Effective Radius at [3.6]
#    ---           fDM(Reff)              Dark Matter Fraction within Reff
#    ---           sigma_fdm(Reff)        Error on fDM(Reff)
#    ---           fDM                    Dark Matter Fraction at each radius
#    ---           sigma_fdm              Error on fDM
#    kpc           Radius                 Radius fros SPARC_ratational_curves
#================================================================================

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


