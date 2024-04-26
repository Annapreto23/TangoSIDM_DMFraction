## Dataset Description


| Units | Label         | Explanations                       |
|-------|---------------|------------------------------------|
| ---   | Galaxy        | Galaxy Name                        |
| Msun  | M*            | Stellar Mass                       |
| kpc   | Reff          | Effective Radius at [3.6]          |
| ---   | fDM(Reff)     | Dark Matter Fraction within Reff   |



Data from Pizagno et al. (2007) (https://ui.adsabs.harvard.edu/abs/2007AJ....134..945P/abstract):

> The catalog derived by Pizagno et al. (2007) consists of 163 spiral galaxies featuring resolved H-alpha rotation curves. We utilized the 
effective radius and circular velocity at the effective radius directly from this catalog and estimated stellar masses using the 𝑖-band
magnitudes, assuming a constant I-band mass-to-light ratio of 1.2. The mass-to-light-ratio is adopted for a Chabrier IMF and it assumes the 
contribution of disc+bulge (Portinari et al. 2004). The effective radius for this sample is defined as the radius at 2.2 × 𝑅disk, where 𝑅disk 
is the disc exponential scale length.


> Caution! We estimated the stellar mass within the half-light radii by dividing by 2 the total stellar masses. This may produce uncertainties
in the dark matter fraction of the order of 20%.

The dark matter fraction, fDM, is then calculated as follows

$$f_{DM} = \frac{M_{total} - M_{stellar}}{M_{total}}$$

where M_{total} = Vcirc^2 Reff / G.