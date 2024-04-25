## Dataset Description


| Units | Label         | Explanations                       |
|-------|---------------|------------------------------------|
| ---   | Name          | SDSS galaxy identifier.            |
| Msun  | M*            | Stellar Mass                       |
| ---   | fDM(Reff)     | Dark Matter Fraction within Reff   |
| ---   | +ErrorfDM     | High error on fDM(Reff)            |
| ---   | -ErrorfDM     | Low error on fDM(Reff)             |

### Barnabé+11 [link](https://ui.adsabs.harvard.edu/abs/2011MNRAS.415.2215B/abstract)

Barnabé et al. investigated the internal mass distribution, amount of dark matter, and dynamical structure of sixteen early-type lens galaxies from the SLACS Survey, at z = 0.08 − 0.33. They analyzed the galaxies' inner regions, i.e., within one effective radius. They assumed both, a Chabrier (2003) and a Salpeter (1955) IMF. We construct our dataset using their dark matter fractions based on a Chabrier IMF. Their stellar mass values are taken from the stellar population analysis performed by Auger et al. (2009) [link](https://ui.adsabs.harvard.edu/abs/2009ApJ...705.1099A/abstract) (also under Chabrier IMF). 

Barnabé et al. calculated the dark matter fraction as follows:

$$ f_{\text{DM}} \equiv 1 - \frac{M_{\ast,e}}{M_{\text{tot},e}} $$

Here, 'e' denotes 'within the effective radius'. 
