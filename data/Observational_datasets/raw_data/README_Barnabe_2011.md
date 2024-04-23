## Datasets Description


| Units | Label         | Explanations                       |
|-------|---------------|------------------------------------|
| Msun  | M*            | Stellar Mass                       |
| ---   | fDM(Reff)     | Dark Matter Fraction within Reff   |
| ---   | +sigma_fdm(Reff) | High error on fDM(Reff)         |
| ---   | -sigma_fdm(Reff) | Low error on fDM(Reff)          |

### Barnabé+11 [link](https://arxiv.org/pdf/1102.2261.pdf)

Barnabé et al. investigated the internal mass distribution, amount of dark matter, and dynamical structure of sixteen early-type lens galaxies from the SLACS Survey, at z = 0.08 − 0.33. They analyzed the inner regions of the galaxies, i.e., within one effective radius. They assumed either a Chabrier (2003) or a Salpeter (1955) IMF. We construct our dataset using their dark matter fractions based on a Chabrier IMF. Their stellar mass values are taken from the stellar population analysis performed by Auger et al. (2009), and their total mass values are derived from a model of the total mass density profile of the lens galaxy with an axially symmetric power-law distribution. Then, they calculated the dark matter fraction as follows:

$$ f_{\text{DM}} \equiv 1 - \frac{M_{\ast,e}}{M_{\text{tot},e}} $$

Here, 'e' denotes 'within the effective radius'. 

We also took the stellar masses used by Barnabé in 2011 from Auger et al. (2009). With this dataset, we also checked the galaxy types in our sample and decided to exclude one galaxy with an S type.
