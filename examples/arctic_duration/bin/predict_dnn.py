from nn_f0nDuration import ANN
import numpy as np

NN = ANN()

from sklearn import  preprocessing

Y = np.loadtxt('dur_output.test')
min_max_scaler = preprocessing.MinMaxScaler()
Y_train_minmax=min_max_scaler.fit_transform(Y)
Y = Y_train_minmax

np.savetxt('dur_output_normalized.test',Y,fmt='%1.3f')
NN.ANN_predict('dur_input_test.vector')
