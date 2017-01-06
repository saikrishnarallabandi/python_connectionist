#!/usr/bin/python
'''
/*************************************************************************
This file is implementaion of neural network class which contains the 
necessary modules to train a neural network model.

Author: Sai Krishna Rallabandi
Affiliation: LTI, CMU. 
Date of Last Modification: November 2016

**************************************************************************/
'''
import sys, numpy, random
import numpy as np
 
class ANN:

    def __init__(self):

        self.input_dimensions = 0
	self.output_dimensions = 0
        self.output_layer = 1
        self.total_layers = 2
        self.eta = 0.01
        self.previous_MSE = 0
        self.A = 1.176
        self.B = 2.0 / 3.0  # 0.666
        self.Bb2A = self.B / (2.0 * self.A)   ## 0.283
        self.units_in_layer = numpy.zeros(self.total_layers)   
        self.param = 'param'

    def get_input_dimensions(self):
	    return self.input_dimensions
    
    def get_output_dimensions(self):
	    return self.output_dimensions    	

    def get_units_of_output_layer(self):
	    return self.units_in_layer[self.output_layer]

    def get_total_layers(self):
	    return self.total_layers    
	    
    def get_eta(self):
	    return self.eta
	    
    def get_eta_layer(self, layer_num):
	    return self.layerdetails_eta[layer_num]
	    
    def set_eta(self, eta_new):
	    self.eta = eta_new 
	    
    def set_eta_layer(self, layer_num, eta_new):
	    self.layerdetails_eta[layer_num] = eta_new 
	    
    def store_MSE(self, mse):
	    self.previous_MSE = mse

 
    def initialize_weights_nielson(self):
  
        k = [self.input_dimensions] + self.units_in_layer[:-1] + [self.output_dimensions] 
        #print "I am printing k " + str(k)
        max_weight = 3.0 / float(self.input_dimensions)

        self.biases = [numpy.random.randn(y, 1)*0.01 for y in k[1:]]
        self.weights = [numpy.random.randn(y,x)*0.01
                        for x, y in zip(k[:-1], k[1:])]

        #self.weights = 2 * max_weight * self.weights - max_weight
        #self.biases = 2 * max_weight * self.biases - max_weight
        '''
        w_backup = self.weights
        b_backup = self.biases
        count = 0
        for w,b in zip(self.weights, self.biases):
 
               w = 2 * max_weight * w - max_weight
               b = 2 * max_weight * b - max_weight
               w_backup[count] = w
               b_backup[count] = b
               count = count + 1
        self.weights = w_backup
        self.biases = b_backup

        print "Weights: " + str(w)
        '''
    
    def activation(self, Sum, layer_num, derivative_flag):
          
            if self.type_of_layer[layer_num] == "L":
                   if derivative_flag == 1:
                       return 1.0
                   else:
                       return Sum

            elif  self.type_of_layer[layer_num] == "N":
                   if derivative_flag == 1:
                           #print self.Bb2A * (self.A - Sum) * (self.A + Sum)
                       return self.Bb2A * (self.A - Sum) * (self.A + Sum)
                   else:    
                       #print self.A * numpy.tanh(self.B*Sum) 
                       return self.A * numpy.tanh(self.B*Sum) 
            
            elif self.type_of_layer[layer_num] == "S":
                    if derivative_flag == 1:
                       return self.B * self.error_at_output_layer * ( 1- self.error_at_output_layer)
                    else:   
                       #print 1.0 / ( 1 + A * exp(-(B*Sum))) 
                       return 1.0 / ( 1 + self.A * np.exp(-(self.B*Sum))) 
            else:
                   print "I dont seem to find this activation function. Sorry :("
                   sys.exit(0)

    def activation_vector(self, Sum, layer_num, derivative_flag):
          
            if self.type_of_layer[layer_num] == "L":
            	   if derivative_flag == 1:
            	   	   return numpy.ones(len(Sum))
            	   else:
                       return Sum

            elif  self.type_of_layer[layer_num] == "N":
            	   if derivative_flag == 1:
            	   	   return self.Bb2A * (self.A - Sum) * (self.A + Sum)
            	   else:	
                       #print self.A * numpy.tanh(self.B*Sum) 
                       return self.A * numpy.tanh(self.B*Sum) 
            
            elif self.type_of_layer[layer_num] == "S":
            	    if derivative_flag == 1:
            	   	   return B * Sum * ( 1- Sum)
            	    else:	
                       #print 1.0 / ( 1 + A * exp(-(B*Sum))) 
            	       return 1.0 / ( 1 + self.A * np.exp(-(self.B*Sum))) 
            else:
                   print "I dont seem to find this activation function. Sorry :("
                   sys.exit(0)
   

    def ANN(self, input_file, output_file):
      
        param_file = self.param
        self.input_layer = -1
        self.output_layer = 0
        self.input_dimensions = 0
        self.read_params(param_file)
        self.initialize_weights_nielson()
        self.input_pattern = numpy.loadtxt(input_file)
        self.output_pattern = numpy.loadtxt(output_file)
        self.print_parameters()       
        
        from sklearn.cross_validation import train_test_split
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(self.input_pattern, self.output_pattern, train_size=0.83)
        training_data = zip(Xtrain, Ytrain)
        test_data = zip(Xtest, Ytest)
        #given_input = self.input_pattern[0].reshape(self.input_dimensions, 1)
        given_input = Xtest[2].reshape(self.input_dimensions, 1)
        self.predicted_pattern = self.compute_output_new(given_input)
        print "Prediction:"
        print self.predicted_pattern.transpose()
        print "Original:"
        print Ytest[2]
        
        self.SGD(training_data, test_data)

        given_input = self.input_pattern[0].reshape(self.input_dimensions, 1)
        self.predicted_pattern = self.compute_output_new(given_input)
        print "Prediction:"
        print self.predicted_pattern
        print "Original:"
        print self.output_pattern[0]

    def read_params(self, param_file):

        f = open(param_file)
        lines = f.readlines()
        self.total_layers = int(lines[0].split('\n')[0])
        self.input_layer = int(lines[1].split('\n')[0].split()[0])
        self.input_dimensions = int(lines[1].split('\n')[0].split()[1])
        self.output_layer = int(lines[2].split('\n')[0])
        self.type_of_layers = lines[3].split('\n')[0].split()
        self.number_of_layers = len(self.type_of_layers) + 1
        temp = lines[3].split('\n')[0]
        self.type_of_layer = []
        for k in range(0, len(temp.split())):
            self.type_of_layer.append(temp.split()[k])         
        temp = lines[4].split('\n')[0]
        self.units_in_layer = []
        for k in range(0, len(temp.split())):
            self.units_in_layer.append(int(temp.split()[k]))
        self.output_dimensions = int(self.units_in_layer[int(self.output_layer) -1 ])
        self.output = numpy.zeros(self.output_dimensions)
        self.eta = float(lines[5].split()[0])
        self.epochs = int(lines[6].split()[0])
        self.batch_size = int(lines[7].split()[0])
        return

    def print_parameters(self):
        print "Input Dimensions: "  + str(self.input_dimensions) 
        print 'Input Layer: ' + str(self.input_layer)
        print "Output Dimensions: " + str(self.output_dimensions)
        print "Output Layer: " + str(self.output_layer)
        print "Number of layers: " + str(self.number_of_layers)
        print "Learning Rate: " + str(self.eta)
        print "Type of Layers: "  + str(self.type_of_layers)
        print "Units in Layers: " + str(self.units_in_layer)
        print "Shapes of weights: " 
        for w in self.weights:
            print w.shape
        print "Shapes of biases: " 
        for b in self.biases:
            print b.shape    

    def get_inout_dimensions(self):
        return self.input_dimensions, self.output_dimensions  

    def compute_output_vector(self, mini_batch):
        self.outputs = []
        batch_outputs = []
        for a in mini_batch:
            count = 0
            #print "a: " + str(a)
            a = a.reshape(self.input_dimensions,1)  
            for b, w in zip(self.biases, self.weights):
               Sum = np.dot(w, a)+b
               a = self.activation_vector(Sum, count, 0)
               self.outputs.append(a)
               count = count + 1
            batch_outputs.append(a)
        return batch_outputs 

    def compute_output_new(self, given_input):
        count = 0
        self.outputs = []
        a = given_input.reshape(self.input_dimensions,1)
        for b, w in zip(self.biases, self.weights):
         
            Sum = np.dot(w, a)+b
            a = self.activation_vector(Sum, count, 0)
            self.outputs.append(a)
            count = count + 1
        return a

    def compute_output(self,  input_pattern):
        Sum = 0.0
        layer_num = self.input_layer + 1
        unit_num = 0
        iDim = 0
        self.outputs = []
        w = self.weights[0]
        b = self.biases[0]
        output = numpy.zeros(self.units_in_layer[layer_num])
 
        for unit_num in range(0, self.units_in_layer[layer_num]):
          
             if self.input_layer == -1:
             	 iDim = self.input_dimensions
             else:
                 iDim = self.units_in_layer[input_layer]

             for k in range(0,iDim):
                 Sum = b[k]
                 t = numpy.asarray(input_pattern)
                 Sum = Sum + numpy.dot(t , w[unit_num]) 
                 output[unit_num] = self.activation(Sum, layer_num, 0)
        self.outputs.append(output)
        current_output = output

        for layer_num in range(self.input_layer+2 , self.total_layers):
             previous_output = current_output
             current_output = numpy.zeros(self.units_in_layer[layer_num])
             w = self.weights[layer_num]
             b = self.biases[layer_num]
             
             for unit_num in range(0, self.units_in_layer[layer_num]):
                 Sum = b[unit_num]
                 for k in range(0, self.units_in_layer[layer_num-1]):
                     Sum = Sum + previous_output[k] * w[unit_num][k]            	 
                 current_output[unit_num] = self.activation(Sum, layer_num, 0)
             self.outputs.append(current_output)
        
        return current_output       


    def compute_error_vector(self, test_data):
    
        error = 0
        normalize_denominator = 0
        count = 0
        for x,y in test_data:
            count = count + 1
            prediction = self.compute_output_new(x)
            error = error + self.compute_error(x, prediction)
            #print error
        #print error
        #print "Error: " + str(float(error/count))
        #return error/count

    def compute_error_test(self, test_data):

        error = 0
        normalize_denominator = 0
        
        for x,y in test_data:
            x = x.reshape(self.input_dimensions,1)
            prediction = self.compute_output_new(x)
            #if self.flag_test == 1:
	      #print test_data
	      #print str(y) + ' ' + str(prediction)
            error_single = prediction - y
            squared_error = error_single * error_single
            error = error + squared_error
            normalize_denominator = normalize_denominator + y*y
#            print "printing normalie den", normalize_denominator            
        self.flag_test = 0
        #if normalize_denominator == 0:
             #print "Normalizing"
             #print "Denominator is 0. I am exiting"
             #sys.exit()
             #print " I have exited"
             
        error = error / normalize_denominator    
        MSE = error / len(test_data)  * 100 
        MSE = np.mean(MSE)
        print "MSE: " + str(MSE) 


    def compute_error(self, desired_pattern, predicted_pattern):
    
         error = 0
         normalize_denominator = 0         
         for unit_num in range(0, self.units_in_layer[self.output_layer]):
	      #print "Predicted Pattern : " + str(predicted_pattern)
	      #print "Desired Pattern : " + str(desired_pattern)
              self.error_at_output_layer = desired_pattern - predicted_pattern
              #print "Error at o/p Layer: " + str(self.error_at_output_layer)
              error = error + (self.error_at_output_layer * self.error_at_output_layer) 
              normalize_denominator = normalize_denominator + (desired_pattern* desired_pattern)             
         if  normalize_denominator == 0:
           print "Denominator is 0. Something Wrong. I am exiting" 
           sys.exit(0) 
         #print "Error: " + str(error)
         error = error / normalize_denominator
         MSE = error
         return MSE


 

    def update_parameters_batch(self, batch_input, batch_output):

         training_data = zip(batch_input, batch_output)
         mini_batches = [training_data[k:k+self.batch_size] for k in xrange(0, len(batch_input), self.batch_size)]
         for batch in mini_batches:
           for i, o in batch:
             i = i.reshape(self.input_dimensions, 1)
             db,dw = self.backprop(i,o)
             self.weights = self.weights - np.asarray(self.eta) * dw / len(batch)
             self.biases = self.biases - np.asarray(self.eta) * db / len(batch)
            # print "printing Weights"
            # print self.weights[-1]



    def SGD(self, training_data, test_data):
        
        eta = self.eta
        epochs = self.epochs
        mini_batch_size = self.batch_size
        if test_data: n_test = len(test_data)
        n = len(training_data)

        for j in xrange(epochs):

            if ( j > 10):
                eta = eta / 2
                print " I have halved the learning rate"
            random.shuffle(training_data)
            mini_batches = [ training_data[k:k+mini_batch_size] for k in xrange(0, n, mini_batch_size)]
 
            count = 1
            for mini_batch in mini_batches:
	        #print "Processing Minibatch " + str(count)
	        count = count +1
                self.update_mini_batch(mini_batch, eta)        ######################
            print "Epoch: " + str(j)
            print "Test Error:"
            self.flag_test = 1
            self.compute_error_test(test_data)
            print "Training Error:"
            self.compute_error_test(training_data)
            print '\n'
    
         
    def update_mini_batch(self, mini_batch, eta):
        k = [self.input_dimensions] + self.units_in_layer[:-1] + [self.output_dimensions]           
        nabla_b =   [numpy.zeros(y) for y in k[1:]]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        #for b in nabla_b:
	   #print "printign b.shape",  b.shape
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        #print "printing nabla_b", numpy.shape(nb),  numpy.shape(dnb)
        
        w_backup = self.weights
        b_backup = self.biases
        
        self.weights = [w- ((eta/len(mini_batch))*nw)
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b- ((eta/len(mini_batch))*nb).transpose()
                       for b, nb in zip(self.biases, nabla_b)]
        #print "am adding biases to", b.shape, nb.shape	
	#print "I have updated the parameters"
	# Check if any is nan or inf and if yes, self.weights = w_backup ; self.biases = b_backup 
	# Check and put flag to 1
	#print self.weights[-1]
	#print '\n'
	
    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        count = 0
        a = a.reshape(self.input_dimensions,1)

        for b, w in zip(self.biases, self.weights):

            z = np.dot(w,a) + b
            a = self.activation(z, count,0)
            #print a.shape
            count = count + 1

        return a    

    # def ununpdate_mini_batch():
      
    def backprop(self, x, y):
     
        x = x.reshape(self.input_dimensions, 1)
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
       
        # feedforward
        a = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
   
        count = 0
        #print "primtng inital w8", numpy.shape(self.weights)
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, a)+b            
            zs.append(z)
            a = self.activation_vector(z, count, 0)
            activations.append(a)
            count = count + 1
        
        self.error_at_output_layer = self.cost_derivative(y,activations[-1])
        delta = self.error_at_output_layer * self.activation_vector(zs[-1],count-1,1) 

        nabla_b[-1] = delta
        nabla_w[-1] = np.transpose(np.dot(activations[-2], delta))
        
        for l in xrange(2, self.total_layers):
            z = zs[-l]
            sp = self.activation_vector(z, self.number_of_layers - l, 1)
            sp = sp.reshape(1,self.units_in_layer[self.number_of_layers-l-1])
            delta = np.dot(delta, self.weights[-l+1]) * sp
            nabla_b[-l] = delta
            try:
              nabla_w[-l] = np.transpose(np.dot(activations[-l-1], delta) )
            except AttributeError:
              nabla_w[-l] = np.transpose(np.dot(delta, activations[-l-1]) )
        return (nabla_b, nabla_w)
      
        

    def cost_derivative(self, y, output_activations):
#        print "y: " + str(y)
#        print "Activation: " + str(output_activations)
 
       #print (numpy.transpose(output_activations) - y), numpy.shape(numpy.transpose(output_activations) - y)
       return (numpy.transpose(output_activations) - y) 
    

   
