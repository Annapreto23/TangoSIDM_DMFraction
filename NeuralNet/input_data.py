import numpy as np
import h5py
import pandas as pd
from numpy.lib.recfunctions import structured_to_unstructured
from sklearn.preprocessing import MinMaxScaler

# Utility functions
def to_structured_array(data, col_names, dtype):
    return np.core.records.fromarrays(data.T, names=','.join(col_names), formats=','.join(dtype))

def read_h5_data(filename, dataset_path):
    try:
        with h5py.File(filename, "r") as file:
            return {key: file[dataset_path + key][:] for key in file[dataset_path].keys()}
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def read_tangodata(name, sim_type, sim_volume, filename):
    folder = f"/Users/cc276407/Simulation_data/snellius/TangoSIDM/{sim_volume}/{sim_type}/{name}/"
    filename = folder + filename

    data = read_h5_data(filename, "Halo_data/")
    if data:
        Ms = data["Mstar"]
        Reff = np.log10(data["GalaxyProjectedHalfLightRadius"])
        fDM = data["fDM_Reff"]
        sigma = data["avg_cross_section_R200"]
        return np.column_stack((Ms, Reff, fDM, sigma))
    return None

def read_eagledata():
    data = np.genfromtxt("../eagle-DMFractions/EAGLE_simulations_DMfractions.txt")
    fDM = data[:, 9]
    select = np.where(fDM > 0)[0]
    Mstellar = data[select, 2]
    Reff = np.log10(data[select, 8])
    fDM = data[select, 9]
    num_galaxies = len(select)
    sigma = np.zeros(num_galaxies)
    return np.column_stack((Mstellar, Reff, fDM, sigma))

class MLData:
    def __init__(self, data, xcols, ycols):
        self.xcols = xcols
        self.ycols = ycols
        self.datacols = self.xcols + self.ycols
        self.data = to_structured_array(data, self.datacols, dtype=len(self.datacols) * ['<f8'])
        self.x = structured_to_unstructured(self.data[self.xcols])
        self.y = structured_to_unstructured(self.data[self.ycols])
        self.xscaler = None
        self.yscaler = None

    def scaling(self):
        if self.x.ndim == 1:
            self.x = self.x.reshape(-1, 1)
        self.y = self.y.reshape(-1, 1)
        self.xscaler = MinMaxScaler(feature_range=(-1, 1)).fit(self.x)
        self.yscaler = MinMaxScaler(feature_range=(-1, 1)).fit(self.y)
        self.x = self.xscaler.transform(self.x)
        self.y = self.yscaler.transform(self.y)

    def postprocess(self, x_test, y_test, y_pred):
        x_test = self.xscaler.inverse_transform(x_test)
        y_test = self.yscaler.inverse_transform(y_test)
        y_pred = self.yscaler.inverse_transform(y_pred)
        return x_test, y_test, y_pred

class TangoSIDM(MLData):
    def __init__(self, name, sim_type, sim_volume, filename):
        data = read_tangodata(name, sim_type, sim_volume, filename)
        if data is not None:
            super().__init__(data, ['Mstellar', 'Reff', 'fDM'], ['sigma'])
        else:
            raise ValueError("Failed to read TangoSIDM data")

class EagleSimulations(MLData):
    def __init__(self):
        data = read_eagledata()
        super().__init__(data, ['Mstellar', 'Reff', 'fDM'], ['sigma'])

def read_observational_dataset():
    folder = "../TangoSIDM_DMFraction/data/Observational_datasets/dataset/"

    # Helper function to load data from CSV and convert to numpy array
    def load_csv_to_numpy(filename):
        return pd.read_csv(folder + filename).to_numpy()

    # Helper function to extract and filter data
    def extract_data(data, mass_idx, fDM_idx, Reff_idx, Q_idx=None, Q_threshold=None):
        mass = np.array(data[:, mass_idx], dtype=np.float32)
        fDM = np.array(data[:, fDM_idx], dtype=np.float32)
        Reff = np.array(data[:, Reff_idx], dtype=np.float32)
        if Q_idx is not None and Q_threshold is not None:
            Q = np.array(data[:, Q_idx], dtype=np.float32)
            select = np.where(Q >= Q_threshold)[0] if Q_threshold > 1 else np.where(Q == Q_threshold)[0]
            return mass[select], fDM[select], Reff[select]
        return mass, fDM, Reff

    # Load datasets
    sparc = load_csv_to_numpy('SPARC.csv')
    atlas3D = load_csv_to_numpy('ATLAS3D.csv')
    barnabe = load_csv_to_numpy('BARNABE11.csv')
    manga = load_csv_to_numpy('MANGA.csv')
    reyes = load_csv_to_numpy('Reyes2011.csv')
    pizagno = load_csv_to_numpy('Pizagno2007.csv')
    slacs = load_csv_to_numpy('Shajib21.csv')
    Yang = load_csv_to_numpy('YANG24.csv')

    # Extract and filter data from each dataset
    sparc_mass, sparc_fDM, sparc_Reff = extract_data(sparc, 1, 3, 2, 5, 1)
    atlas3D_mass, atlas3D_fDM, atlas3D_Reff = extract_data(atlas3D, 1, 3, 2, 5, 3)
    barnabe_mass, barnabe_fDM, barnabe_Reff = extract_data(barnabe, 1, 2, 5)
    manga_mass, manga_fDM, manga_Reff = extract_data(manga, 2, 4, 3)
    reyes_mass, reyes_fDM, reyes_Reff = extract_data(reyes, 1, 3, 2)
    pizagno_mass, pizagno_fDM, pizagno_Reff = extract_data(pizagno, 1, 3, 2)
    Yang_mass, Yang_fDM, Yang_Reff = extract_data(Yang, 1, 2, 4)
    slacs_mass, slacs_fDM, slacs_Reff = extract_data(slacs, 1, 3, 2)

    # Concatenate all data
    Mstellar = np.concatenate([sparc_mass, reyes_mass, pizagno_mass, Yang_mass, slacs_mass, barnabe_mass, atlas3D_mass, manga_mass])
    Reff = np.concatenate([sparc_Reff, reyes_Reff, pizagno_Reff, Yang_Reff, slacs_Reff, barnabe_Reff, atlas3D_Reff, manga_Reff])
    fDM = np.concatenate([sparc_fDM, reyes_fDM, pizagno_fDM, Yang_fDM, slacs_fDM, barnabe_fDM, atlas3D_fDM, manga_fDM])

    # Filter out invalid fDM values and take the logarithm of Mstellar and Reff
    select = np.where(fDM > 0)[0]
    Mstellar = np.log10(Mstellar[select])
    Reff = np.log10(Reff[select])
    fDM = fDM[select]

    # Initialize sigma as zeros
    sigma = np.zeros(len(fDM))

    return np.column_stack((Mstellar, Reff, fDM, sigma))

class ObservationalDataset(MLData):
    def __init__(self):
        data = read_observational_dataset()
        super().__init__(data, ['Mstellar', 'Reff', 'fDM'], ['sigma'])