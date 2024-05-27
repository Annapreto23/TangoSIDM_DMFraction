Dark matter fractions from the EAGLE simulation series (Schaye et al. 2015) taken
from the RefL0100N1504 cosmological box.

The first columns in the file correspond to Galaxy ID and Group Number. Here we selected 
only central galaxies more massive than 10^10 Msun in stellar mass (over an aperture of
30 kpc). We extracted from the online EAGLE database stellar masses (2), half-mass
radii (3), 2D projected half mass radii (4), gas masses (5), halo masses (M200) (6), and
the kappa co-rotational parameter (7). See example query below.

From the star database (RefL100N1504_Stars), we read all star particles belonging to a given
galaxy (with a given ID) and extracted their r-band magnitudes. Based on these we calculated 
their r-and luminosities. From the EAGLE simulations, we cross-matched the particles ID, 
determined the star particles positions and calculated their 3D half-light radii (8).

Finally, also from the EAGLE simulations we read all the particle data (DM, gas and stars)
and calculated the dark matter fractions within the half-light radii (9).




Example query for EAGLE database:

myQuery = ("SELECT \
           AP_Star.Mass_Star as mstellar, \
           AP_Star.Mass_Gas as mgas, \
           SH.GalaxyID, \
           SH.GroupNumber as GrNr, \
           SH.SubGroupNumber as SubGrNr, \
           MK.KappaCoRot as kappa, \
           FOF.Group_M_Crit200 as M200, \
           SH_sizes.R_halfmass30 as Rhalf, \
           SH_sizes.R_halfmass30_projected as RProjhalf \
           FROM \
           RefL0100N1504_Subhalo as SH, \
           RefL0100N1504_Aperture as AP_Star, \
           RefL0100N1504_Sizes as SH_sizes, \
           RefL0100N1504_MorphoKinem as MK, \
           RefL0100N1504_FOF as FOF \
           WHERE \
           SH.SnapNum = 28 \
           and SH.GalaxyID = AP_Star.GalaxyID \
           and SH.GalaxyID = SH_sizes.GalaxyID \
           and SH.GalaxyID = MK.GalaxyID \
           and SH.GroupID = FOF.GroupID \
           and SH.SubGroupNumber = 0 \
           and AP_Star.ApertureSize = 30 \
           and AP_Star.Mass_Star > 1.0e10")

for GalID in GalaxyID:

    myQuery = ("SELECT \
               Star.ParticleID, \
               Star.r as r_band_mag \
               FROM \
               RefL0100N1504_Stars as Star \
               WHERE \
               Star.SnapNum = 28 \
               and Star.GalaxyID = %i")%int(GalID)

    myData = sql.execute_query(con, myQuery)
