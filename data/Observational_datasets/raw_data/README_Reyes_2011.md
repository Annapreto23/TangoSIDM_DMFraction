## Dataset Description


| Units | Label         | Explanations                       |
|-------|---------------|------------------------------------|
| ---   | Galaxy        | Galaxy Name                        |
| Msun  | M*            | Stellar Mass                       |
| kpc   | Reff          | Effective Radius                   |
| ---   | fDM(Reff)     | Dark Matter Fraction within Reff   |



Data from Reyes et al. (2011) (https://ui.adsabs.harvard.edu/abs/2011MNRAS.417.2347R/abstract):

> The catalog derived by Reyes et al. (2011) consists of disk rotation velocities for a subset of SDSS galaxies. 
This dataset includes the 𝑖-band Petrosian half-light radius, 𝑟-band Petrosian absolute magnitude (𝑀𝑟), and 𝑔 − 𝑟 colour, 
all 𝑘-corrected to 𝑧 = 0 and corrected for Galactic and internal extinction. 

Stellar masses were estimated following Bell et al. (2003), converted to a Chabrier IMF.

> Caution! We estimated the stellar mass within the half-light radii by dividing by 2 the total stellar masses. 
This may produce uncertainties in the dark matter fraction of the order of 20%.

The dark matter fraction, fDM, is then calculated as follows

$$f_{DM} = \frac{M_{total} - M_{stellar}}{M_{total}}$$

where M_{total} = Vcirc^2 Reff / G, here Vcirc = Vcirc(Reff).