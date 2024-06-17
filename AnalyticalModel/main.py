from model_pred import Predictions

# Setting up arguments
file_path = "../TangoSIDM_DMFraction/data/Simulation_datasets/TangoSIDM/Halo_data_L025N376ReferenceSigmaVelDep30Anisotropic.hdf5"
df_file_path = 'AnalyticalModel/data_pred/SigmapredReferenceSigmaVelDep30.csv'

predictions = Predictions(file_path, df_file_path)

# Plot predictions
predictions.plot_predictions(plot_errors=False)
#predictions.plot_fDM()
#predictions.hist()
