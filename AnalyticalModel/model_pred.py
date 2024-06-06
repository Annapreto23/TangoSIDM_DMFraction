import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns

# Setting up the environment
params = {
    "font.size": 15,
    "font.family": "Arial Black",
    "text.usetex": True,
    "mathtext.fontset": "custom",
    "figure.subplot.left": 0.15,
    "figure.subplot.right": 0.95,
    "figure.subplot.bottom": 0.16,
    "figure.subplot.top": 0.95,
    "figure.subplot.wspace": 0.3,
    "figure.subplot.hspace": 0.3,
    "lines.markersize": 2,
    "lines.linewidth": 1.5,
}
plt.rcParams.update(params)

# Importing user modules
from sigma import GalaxyCrossSectionCalculator
from data_process import classhalo
from findingr1 import calculate_mass
from fDM_testing import process_all_galaxies

class Predictions:
    def __init__(self, file_path, df_file_path, halo_type='all'):
        self.file_path = file_path
        self.df_file_path = df_file_path
        self.halo_type = halo_type
        self.halo = classhalo(file_path, halo_type)
        self.df = None
        self.load_or_generate_data()

    def load_or_generate_data(self):
        if os.path.exists(self.df_file_path) and os.path.getsize(self.df_file_path) > 0:
            self.df = pd.read_csv(self.df_file_path)
            print("DataFrame loaded from file:")
            print(self.df.head())
        else:
            self.generate_data()

    def generate_data(self):
        y_true = []
        y_pred = []
        gapp = []
        maxi = len(self.halo.Mstar)
        for i in range(0, maxi):
            print(i)
            calculator = GalaxyCrossSectionCalculator(self.file_path, i, self.halo_type)
            sigma, true_sigma, r1, rho_iso, r_iso, gap, fDM = calculator.run()
            gap_percentage = (true_sigma - sigma) / true_sigma * 100

            y_true.append(true_sigma)
            y_pred.append(sigma)
            gapp.append(gap_percentage)

        error = self.calculate_errors(y_pred, y_true)
        
        data = {
            'y_true': y_true,
            'y_pred': y_pred,
            'error': error
        }

        self.df = pd.DataFrame(data)
        self.df.to_csv(self.df_file_path, index=False)
        print("DataFrame saved to file")

    def calculate_errors(self, y_pred, y_true):
        Ms, Mdm, fdm, fdm_sim, Mb_tot, Mb_tot_sim = process_all_galaxies(self.halo, self.file_path, self.halo_type)
        error = 2 * abs(np.array(fdm) - np.array(fdm_sim)) * np.array(y_pred) / (np.array(fdm) * (1 - np.array(fdm)))
        return error

    def plot_predictions(self, plot_errors = False):
        if self.df is None:
            print("No data to plot.")
            return

        y_true = self.df['y_true'].values
        y_true = self.halo.ReCrossSection
        y_pred = self.df['y_pred'].values
        error = self.df['error'].values

        select = y_pred < 60  # select non-aberrant values
        y_true = y_true[select]
        y_pred = y_pred[select]
        error = error[select]

        plt.rcParams.update({"font.size": 20})

        g = sns.jointplot(x=y_true, y=y_pred, kind='reg', marginal_kws=dict(bins=200, fill=True))
        if plot_errors:
            g.ax_joint.errorbar(y_true, y_pred, yerr=error, color='black', linestyle='None', alpha=0.5, linewidth = 0.7, capsize=1)
        g.ax_joint.plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100), linestyle='--', label='x = y', linewidth=0.5)
        g.ax_joint.set_xlim(0, 10)
        g.ax_joint.set_ylim(-3, 40)
        g.ax_joint.set_xlabel(r'$(\sigma$/$m_x)_\mathrm{sim}$ [$\mathrm{cm}^{2}\mathrm{g}^{-1}$]')
        g.ax_joint.set_ylabel(r'$\sigma$/$m_x$ [$\mathrm{cm}^{2}\mathrm{g}^{-1}$]')
        g.fig.suptitle("Reference SigmaVel60 with c from the simulation", fontsize=15)
        g.ax_joint.legend()
        g.ax_joint.grid(True)
        plt.tight_layout()
        plt.show()

