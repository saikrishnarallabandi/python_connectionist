#!/usr/bin/python

from nn_f0nDuration import ANN
import pandas as pd
import  numpy as np

flag_arctic_duration = 1


if flag_arctic_duration == 1:
      
     X = pd.read_csv('../data/arctic/arctic_train_input.vector',sep=' ',header=None)
     X = np.array(X)

     Y = pd.read_csv('../data/arctic/arctic_train_output.vector',sep=' ',header=None)
     Y = np.array(Y)

     print 'Loaded Data successfully'

     from sklearn import  preprocessing

     min_max_scaler = preprocessing.MinMaxScaler()
     Y_train_minmax=min_max_scaler.fit_transform(Y)
     Y = Y_train_minmax
     print ' Training Data normalized'
     np.savetxt('../data/arctic/arctic_train_output_normalized.vector',Y,fmt='%1.3f')
     
     NN = ANN()
     #NN.ANN('../data/arctic/arctic_train_input.vector', '../data/arctic/arctic_train_output_normalized.vector')
     NN.ANN('../data/arctic/arctic_train_input.vector', '../data/arctic/arctic_train_input.vector') 
     #training_data = zip(Xtrain,Ytrain)
     #test_data = zip(Xtest,Ytest)
     
     #NN.SGD(training_data, num_epochs, mini_batch_size, eta, test_data) 

  
