## Datasets Description

#================================================================================
#Description of file: ../dataset/BEZANSON15.csv
#--------------------------------------------------------------------------------
#    Units         Label                  Explanations
#--------------------------------------------------------------------------------
#    ---           Galaxy                 Galaxy Name
#    Msun          M*                     Stellar Mass
#    kpc           Reff                   Effective Radius at [3.6]
#    ---           fDM(Reff)              Dark Matter Fraction within Reff
#    ---           sigma_fdm(Reff)        Error on fDM(Reff)
#================================================================================

### Bezanson+15

The dataset from Bezanson et al. 2015 includes 103  early- and late-type, or alternatively quiescent an 
star-forming, galaxies. They use a Chabrier IMF for the stellar mass M*. We use their velocity dispersion measurements (details in section 2.5 https://ui.adsabs.harvard.edu/abs/2015ApJ...799..148B/abstract) and then calculate the fDM within the effective radius $R_e$ with : 

$f_{DM} = 1 - \frac{M*}{M_{dyn}}$

with $M_{dyn}$ extracted from the Virial theorem : 

$M_{dyn}(r \textless R_e) = \frac{K R_e\sigma^2(r\textless R_e)}{G}$

and assuming $K = 5$ (http://dx.doi.org/10.1111/j.1365-2966.2005.09981.x).
