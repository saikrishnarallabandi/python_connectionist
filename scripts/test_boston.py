#!/usr/bin/python

from nn_f0nDuration import ANN
import pandas as pd
import  numpy as np
from sklearn.datasets import  load_boston

flag_arctic_duration = 0
flag_boston_prices = 1

  
if flag_boston_prices == 1:
 
     boston = load_boston()
     print 'Loaded Data successfully'

     X = boston.data
     Y = boston.target

     from sklearn import  preprocessing

     xscaler = preprocessing.StandardScaler().fit(X)
     X_mean = xscaler.mean_
     X_std = xscaler.scale_
     X = xscaler.transform(X)

     #min_max_scaler = preprocessing.MinMaxScaler()
     #Y_train_minmax=min_max_scaler.fit_transform(Y)
     #Y = Y_train_minmax 
     print ' Training Data normalized'

     np.savetxt('../data/boston/boston.data',X, fmt='%1.3f')
     np.savetxt('../data/boston/boston.target',Y,fmt='%1.3f')

     NN = ANN()
     NN.ANN('../data/boston/boston.data', '../data/boston/boston.target')
         
 
