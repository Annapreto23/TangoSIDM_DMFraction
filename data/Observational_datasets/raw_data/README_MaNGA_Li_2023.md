#To complete

## Datasets Description

| Units | Label     | Explanations 
|-------|-----------|--------------
| ---   | PlateIFU  | Plate IFU
| ---   | MaNGAID   | MaNGA ID
| Msun  | M*        | Stellar Mass 
| ---   | fDM(Reff) | Dark Matter Fraction within Reff 
| kpc   | Reff      | Effective Radius        
| ---   | Q         | Quality Flag (Q<2 == poor)      

MaNGA dataset taken from https://github.com/Shubo143/MaNGADensitySlope/tree/main
based on the analysis of Li et al. (2023) (https://ui.adsabs.harvard.edu/abs/2024MNRAS.tmp..878L/abstract)

Li et al. use the results from the best Jeans Anisotropic Modelling of the integral-field stellar kinematics 
for near 6000 galaxies from the MaNGA DynPop project, with stellar masses between 10^9-10^12 Msun. The database
includes both early-type and late-type galaxies.

We convert stellar masses to a Chabrier IMF.

We follow Li et al. and select galaxies with a quality flag > 1 to ensure that the modelling of the mass profile is reliable.
For these approximately 6000 galaxies, we require the difference in the mass-weighted total density slope between 
JAMcyl and JAMsph modelling is smaller than three times of 0.079, which is the observed root-mean-square scatter of the dynamical property among different model assumptions for galaxies with Qual = 1. Finally, we add a filtering condition: 
|𝑓DM,cyl − 𝑓DM,sph| < 0.1, to improve the accuracy of the dark matter fraction estimations.
