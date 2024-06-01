
#---user modules credits : Arthur Fangzhou Jiang 2020 Caltech
import profiles as pr
import galhalo as gh

#---standard python stuff
import numpy as np

#---for simulation data
from data_process import classhalo


#---to find r1
from findingr1 import findr1


class GalaxyCrossSectionCalculator:
    def __init__(self, file_path, i, type = 'all'):
        self.file_path = file_path
        self.i = i
        self.halo = classhalo(file_path, type)
        self.r_FullRange = np.logspace(-3, 3, 200)  # [kpc] for plotting the full profile
        self.load_galaxy_data()

    def load_galaxy_data(self):
        i = self.i
        self.lgMv = self.halo.M200c[i]  # [M_sun]
        self.c = self.halo.c200c[i]
        self.lgMb = self.halo.Mstar[i]  # [M_sun]
        self.r0 = self.halo.GalaxyHalfLightRadius[i] / (1 + np.sqrt(2))  # [kpc]

    def compute_profiles(self):
        Mv = 10. ** self.lgMv
        Mb = 10. ** self.lgMb

        # Prepare the CDM profile
        halo_init = pr.NFW(Mv, self.c, Delta=100., z=0.)
        # Prepare the baryonic profile
        disk = pr.Hernquist(Mb, self.r0)
        # Prepare the contracted DM halo profile
        halo_contra = gh.contra(self.r_FullRange, halo_init, disk)[0]  # <<< adiabatically contracted CDM halo
        return halo_init, halo_contra, disk

    def find_r1(self, halo_init, halo_contra):
        r1, dist = findr1(halo_contra.rho(self.r_FullRange), halo_init.rho(self.r_FullRange), self.r_FullRange)
        return r1, dist

    def calculate_sigma(self, r1):
        kpctocm = 3.086e16 * 1e5
        kmtocm = 1e5

        # Velocity dispersion
        vel_disp = np.interp(r1, self.halo.AxisRadius, self.halo.Dark_matter_Velocity_dispersion[:-9, self.i])  # km/s
        vel_disp *= kmtocm  # cm/s

        # Galaxy's age
        tage = 10 * 1e9  # years
        tage *= 60 * 60 * 24 * 365  # seconds

        # Density at r1 using halo.contra
        rhor1 = np.interp(r1, self.halo.Density_radial_bins, self.halo.Dark_matter_Density_profile[:,self.i])
        rho = rhor1
        rho *= 2e30 * 1e3  # g/kpc^3
        rho /= kpctocm ** 3  # g/cm^3

        # Function to compute the cross section
        def sigm(rho, vel, tage):
            return np.sqrt(np.pi) / (rho * vel * 4 * tage)

        sigma = sigm(rho, vel_disp, tage)
        true_sigma = np.interp(r1, self.halo.AxisRadius[:-1], self.halo.MeanCrossSection[:, self.i])

        return sigma, true_sigma

    def run(self):
        halo_init, halo_contra, disk = self.compute_profiles()
        r1, dist = self.find_r1(halo_init, halo_contra)
        sigma, true_sigma = self.calculate_sigma(r1)
        return sigma, true_sigma, r1, dist

