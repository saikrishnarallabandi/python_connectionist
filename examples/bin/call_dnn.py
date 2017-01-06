from nn_f0nDuration import ANN
import numpy as np
NN = ANN()

from sklearn import  preprocessing

X = np.loadtxt('dur_input_train.vector')
X_scaled = preprocessing.scale(X)
np.savetxt('dur_input_train_normalized.vector',X_scaled,fmt='%1.3f')

Y = np.loadtxt('dur_output.train')
min_max_scaler = preprocessing.MinMaxScaler()
Y_train_minmax=min_max_scaler.fit_transform(Y)
Y = Y_train_minmax
#numpy.save('min_max', )
np.savetxt('dur_output_normalized.train',Y,fmt='%1.3f')
NN.ANN('dur_input_train.vector', 'dur_output_normalized.train')
