#!/usr/bin/python

from nn_iris import ANN
import pandas as pd
import  numpy as np
import numpy
from sklearn import datasets
iris = datasets.load_iris()
X, y = iris.data, iris.target

#X = numpy.array([numpy.array(xi) for xi in X])
#y = numpy.array([numpy.array(xi) for xi in y])
X = numpy.asarray(X)
y = numpy.asarray(y)

print X[0]
print y[0]

from sklearn import  preprocessing

xscaler = preprocessing.StandardScaler().fit(X)

X_mean = xscaler.mean_#
X_std = xscaler.scale_
X = xscaler.transform(X)

np.savetxt('../data/iris/iris.data',X, fmt='%1.3f')
np.savetxt('../data/iris/iris.target',y,fmt='%1.3f')

flag_arctic_duration = 0
flag_iris_recognition = 1

if flag_arctic_duration == 1:
   
     NN = ANN()
     NN.ANN('../data/iris/iris.data', '../data/iris/iris.target')
     
if flag_iris_recognition == 1:

     NN = ANN()
     NN.ANN('../data/iris/iris.data', '../data/iris/iris.target')
     

