import numpy as np
from sklearn.model_selection import train_test_split
from neuralnet import NeuralNetwork
from plotter import PLOT_NN
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from neuralnet import adjusted_R_squared
from input_data import TangoSIDM, ObservationalDataset, EagleSimulations

# Input/Output details for plot
xnames= ['$\log_{10} M_{*} [M_{\odot}]$','$\log_{10} R_{\mathrm{eff}}$ [kpc]', '$f_{DM}$']
ynames=['$\sigma/m_{\chi}$']
xcols = ['Mstellar','Reff', "fDM"]
xcols_string = ','.join(xcols)

sampling = 'none'

seed = 7
np.random.seed(seed) # fix seed for reproducibility

# ML settings GridSearch
optimizer = 'Adam'
h_nodes = [40, 50, 30]
activation = ['linear', 'tanh', 'linear', 'tanh']
dropout = [0.0, 0.0, 0.0]
perc_train = 0.8
loss = 'mean_squared_error'
epochs = 15
batch_size = 128

# read data
tango = TangoSIDM('SigmaVelDep30Anisotropic', 'Reference', 'L025N376',
                  "Halo_data_DMFractionsReferenceSigmaVel30.hdf5")

# scale data
tango.scaling()

# divide into train and test set
x_train, x_test, y_train, y_test = train_test_split(tango.x, tango.y, test_size=1-perc_train, random_state=seed, shuffle=True)

input_size = len(x_train[0])
output_size = len(y_train[0])
nodes = [input_size] + h_nodes + [output_size]

# read hyperparameters
nn = NeuralNetwork(input_size, output_size, h_nodes, activation, dropout, loss, epochs, batch_size, optimizer)
nn.NN_model()

#------------------------------------------ Train and test --------------------------------------------------------------
# Train, evaluate, predict, postprocess
result = nn.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=0, validation_data=(x_test, y_test)) #train
score = nn.model.evaluate(x_test, y_test, verbose=0) #evaluate
y_pred = nn.model.predict(x_test) #predict

print("Errors: MSE = %.3e ; R^2 = %.3f"%tuple(score))

x_test_log, y_test_log, y_pred = tango.postprocess(x_test, y_test, y_pred) #postprocess

# plotting
plot = PLOT_NN(tango, nn, xnames, ynames, dataname='tangoSIDM', N=len(y_test),
               xcols_string=xcols_string, sampling=str(sampling), score=score, epochs=epochs)
plot.plot_input_output(x_test_log, y_test_log, y_pred)
plot.plot_true_predict(y_test_log, y_pred)

#-------------------------------------- Test in other samples -----------------------------------------------------------

tango_cdm = TangoSIDM('SigmaConstant00', 'WeakStellarFB', 'L025N376',
                      "Halo_data_DMFractionsWeakStellarFBSigmaConstant00.hdf5")

tango_cdm.scaling()
new_y_pred = nn.model.predict(tango_cdm.x) #predict
x_test_log, y_test_log, y_pred = tango_cdm.postprocess(tango_cdm.x, tango_cdm.y, new_y_pred) #postprocess

# plotting
plot = PLOT_NN(tango_cdm, nn, xnames, ynames, dataname='tangoSIDM_CDM_WeakStellarFB', N=len(y_pred),
               xcols_string=xcols_string, sampling=str(sampling), score=score, epochs=epochs)
plot.plot_input_output(x_test_log, y_test_log, y_pred)
plot.plot_true_predict(y_test_log, y_pred)


#-------------------------------------- Test in other samples -----------------------------------------------------------
tango_sigma30_weak = TangoSIDM('SigmaVelDep30Anisotropic', 'WeakStellarFB', 'L025N376',
                               "Halo_data_DMFractionsWeakStellarFBSigmaVel30.hdf5")

tango_sigma30_weak.scaling()
new_y_pred = nn.model.predict(tango_sigma30_weak.x) #predict
x_test_log, y_test_log, y_pred = tango_sigma30_weak.postprocess(tango_sigma30_weak.x, tango_sigma30_weak.y, new_y_pred) #postprocess

# plotting
plot = PLOT_NN(tango_sigma30_weak, nn, xnames, ynames, dataname='tangoSIDM_Sigma30_WeakStellarFB', N=len(y_pred),
               xcols_string=xcols_string, sampling=str(sampling), score=score, epochs=epochs)
plot.plot_input_output(x_test_log, y_test_log, y_pred)
plot.plot_true_predict(y_test_log, y_pred)


#-------------------------------------- Test in other samples -----------------------------------------------------------
eagle = EagleSimulations()

eagle.scaling()
new_y_pred = nn.model.predict(eagle.x) #predict
x_test_log, y_test_log, y_pred = eagle.postprocess(eagle.x, eagle.y, new_y_pred) #postprocess

# plotting
plot = PLOT_NN(eagle, nn, xnames, ynames, dataname='eagleSimulations', N=len(y_pred),
               xcols_string=xcols_string, sampling=str(sampling), score=score, epochs=epochs)
plot.plot_input_output(x_test_log, y_test_log, y_pred)
plot.plot_true_predict(y_test_log, y_pred)


#-------------------------------------- Test in other samples -----------------------------------------------------------
observations = ObservationalDataset()

observations.scaling()
new_y_pred = nn.model.predict(observations.x) #predict
x_test_log, y_test_log, y_pred = observations.postprocess(observations.x, observations.y, new_y_pred) #postprocess

print(len(y_test_log))

# plotting
plot = PLOT_NN(observations, nn, xnames, ynames, dataname='Observations', N=len(y_pred),
               xcols_string=xcols_string, sampling=str(sampling), score=score, epochs=epochs)
plot.plot_input_output(x_test_log, y_test_log, y_pred)
plot.plot_true_predict(y_test_log, y_pred)
