import math
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd



def tanh(z):
    return np.tanh(z)
def sigmoid(z):
    return 1.0/(1 + np.exp(-z))
def tanh(z):
    return np.tanh(z)
def sigmoid_der(z):
    return sigmoid(z)*(1.0-sigmoid(z))
def tanh_der(z):
    return 1.0 - np.power(z,2)
def relu(z):
    return z * (z>0)
def relu_der(x):
    x[x<0] = 0
    x[x>0] = 1
    return x
def f(x) :
    return np.sin(x)

import copy
def normalize(data):
    data2=copy.deepcopy(data)
    #print "data",data
    for i in range(len(data)):
        max_elem=np.max(data[i])
        min_elem=np.min(data[i])
        su=max_elem+min_elem
        diff=max_elem-min_elem
        #print su,diff
        if data.shape[1]>1:
            for j in range(len(data[i])):    
                num=2*data[i][j]-su
                #print "dd", data[i][j],"num", num
                data2[i][j]=num/(1.0*diff)     
        else:
            num=2*data[i]-su
            data2[i]=num/(1.0*diff)   
    return data2

def denormalize(data,data2): #data is actual, data2 is normalized
    data3=copy.deepcopy(data2)
    for i in range(len(data2)):
        max_elem=np.max(data[i])
        min_elem=np.min(data[i])
        su=float(max_elem+min_elem)
        diff=float(max_elem-min_elem)
        if data.shape[1]>1:
            for j in range(len(data2[i])):
                data3[i][j]=(data2[i][j]*(diff)+su)/2
        else:
            data3[i]=(data2[i]*(diff)+su)/2
    return data3

def gen_data():
    

    pi = math.pi
    ll = -2*pi
    ul = 2*pi
    incr = (ul-ll)/1000
    x_data = np.arange(ll,ul,incr)
    y_data = f(x_data)
    incr = (ul-ll)/300
    x_valid = np.arange(ll,ul,incr)
    y_valid = f(x_valid)

    x_test = x_data[800:]
    y_test = y_data[800:]

    x_data = x_data[:800]
    y_data = y_data[:800]

    # x_d=normalize(x_data)
    x_d = np.array(np.reshape(x_data,(1,800)))
    # print("xd",x_d.shape)
    # print ("x_d",x_d)
    # y_d=normalize(y_data)
    # y_d = np.array(y_data)
    y_d = np.array(np.reshape(y_data,(1,800)))
    # x_v=normalize(x_valid)
    x_v = np.array(x_valid)
    # y_v=normalize(y_valid)
    y_v = np.array(y_valid)
    # x_t=normalize(x_test)
    x_t = np.array(x_test)
    # y_t=normalize(y_test)
    y_t = np.array(y_test)

    return x_d,y_d,x_v,y_v,x_t,y_t  , x_data,y_data,x_valid,y_valid,x_test,y_test

def initialise_parameters(num_layers,layer_neurons):
    weights = []
    biases = []
    for l in range(0,num_layers-1) :
        w = (1.0/np.sqrt(layer_neurons[l]))*np.random.randn(layer_neurons[l+1],layer_neurons[l])
        b = np.zeros((layer_neurons[l+1],1))
        weights.append(w)
        biases.append(b)
        l = l+1
    return weights,biases  
def forward_pass(xdata,weights,biases,act_func):
    I = len(weights)
    i = 0
    zs = []
    acts = []
    z = np.dot(weights[i],xdata)+biases[i]
    a = act_func(z)
    zs.append(z)
    acts.append(a)
    i = i+1
    while i<I-1 :
        z = np.dot(weights[i],acts[i-1])+biases[i]
        a = act_func(z)
        zs.append(z)
        acts.append(a)
        i = i+1
    z = np.dot(weights[i],acts[i-1])+biases[i]
    a = z   #last layer activation function control
    acts.append(a)
    return zs,acts

def denn(val,max_elem,min_elem):
    op=(val*(max_elem-min_elem)+(max_elem+min_elem))/2
    return op

def calculate_cost(acts,ydata,data_norm_y,data_norm_x):#data for denormalizing
    # y = denormalize(data_norm_y,ydata)
    y = ydata
    yp = acts[-1]
    # yp = denormalize(data_norm_y,acts[-1])
    # y=ydata
    # yp=acts[-1]
    m = y.shape[1]
    cost = np.sqrt(np.sum(np.square(yp-y))/m)
    return cost
def backward_pass(xdata,ydata,zs,acts,weights,biases,act_flag):
    dzs = []
    dws = []
    dbs = []
    i = len(weights)-1
    for k in range(i+1):
        dzs.append(0)
        dws.append(0)
        dbs.append(0)
    m = ydata.shape[1]
    dz = acts[i] - ydata
    dw = np.dot(dz,acts[i-1].T)/m
    db = np.sum(dz,axis=1,keepdims=True)/m
    dzs[i] = dz
    dws[i] = dw
    dbs[i] = db
    i = i-1
    while i>0 :
        if act_flag == "tanh" :
            dz = np.multiply(np.dot(weights[i+1].T,dz),tanh_der(acts[i]))
        if act_flag == "sigmoid":
            dz = np.multiply(np.dot(weights[i+1].T,dz),sigmoid_der(acts[i]))
        if act_flag == "relu" :
            dz = np.multiply(np.dot(weights[i+1].T,dz),relu_der(acts[i]))
        
        dw = np.dot(dz,acts[i-1].T)/m
        db = np.sum(dz,axis=1,keepdims=True)/m
        i = i-1
    if act_flag == "tanh" :
            dz = np.multiply(np.dot(weights[i+1].T,dz),tanh_der(acts[i]))
    if act_flag == "sigmoid":
            dz = np.multiply(np.dot(weights[i+1].T,dz),sigmoid_der(acts[i])) 
    if act_flag == "relu" :
            dz = np.multiply(np.dot(weights[i+1].T,dz),relu_der(acts[i]))
    dw = np.dot(dz,xdata.T)/m
    db = np.sum(dz,axis=1,keepdims=True)/m
    dzs[i] = dz
    dws[i] = dw
    dbs[i] = db
    return dzs,dws,dbs

def update_param(weights,biases,dw,db,learning_rate):
    for i in range(len(weights)) :
        weights[i] = weights[i] - learning_rate*dw[i]
        biases[i] = biases[i] - learning_rate*db[i]
        # #added weights cap
        # for j in range(len(weights[i])):
        #     for k in range(len(weights[i][j])):
        #         if weights[i][j][k]>1:
        #             weights[i][j][k]=1
        #         if weights[i][j][k]<-1:
        #             weights[i][j][k]=-1
                
    return weights,biases
def predict(xdata,weights,biases,act_func):
    zs,acts = forward_pass(xdata,weights,biases,act_func)
    yp = acts[-1]
    yp = np.squeeze(yp)
    return acts



#learning_rate = float(input("enter the value of learning rate - "))
learning_rate=0.001
#n means not normlalized
xdata_ok,ydata_ok,x_valid,y_valid,xtest,ytest,nx_data,ny_data,nx_valid,ny_valid,nx_test,ny_test = gen_data()
print(xtest.shape)
print(x_valid.shape)
print(xdata_ok.shape)
#l1 = int(input("enter total number of layer (including input layer and output layer) - "))
l = []

#print("layer 0 is the input layer and layer %s is the output layer"%(l1-1))
#for i in range(l1) :
 #   l.append(int(input("enter the number of neurons in layer %s "%i)))
# weights,biases = initialise_parameters(5,[1,32,128,32,1])
l1=5
l=[1,64,128,32,1]
weights,biases = initialise_parameters(l1,l)
#e = int(input("enter number of epochs - "))
# print(xdata_ok.shape[1])
batch_size = 256
costs_maps = []

costs_map = []
iter_map = []
num_of_batches=xdata_ok.shape[1]/batch_size
print( "len_x",xdata_ok.shape[1],"num_batches",num_of_batches)
e=1000
k=zip(xdata_ok.T,ydata_ok.T)

max_elem=np.max(ny_data)
min_elem=np.min(ny_data)
for i in range(e) :
    
    random.shuffle(k)
    xdata_full,ydata_full=zip(*k)
    xdata_full=np.array(xdata_full).T
    ydata_full=np.array(ydata_full).T
    
    for batch_num in range(num_of_batches):

        #xdata=np.array(xdata_full[batch_size*batch_num:batch_size*(batch_num+1)])
        xdata=xdata_full[:,batch_size*batch_num:batch_size*(batch_num+1)]
        #print "Xxx",xdata.shape
        #exit()
        #print X[batch_size*batch_num:batch_size*(batch_num+1):1]
        #ydata=np.array([ydata_full[batch_size*batch_num:batch_size*(batch_num+1)]])
        ydata=ydata_full[:,batch_size*batch_num:batch_size*(batch_num+1)]

        zs,acts = forward_pass(xdata,weights,biases,relu)
        # cost = calculate_cost(acts,ydata_full)
        # acts_valid = predict(x_valid,weights,biases,tanh)
        # cost_valid = calculate_cost(acts_valid,y_valid)
        dzs,dws,dbs = backward_pass(xdata,ydata,zs,acts,weights,biases,"relu")
        weights,biases = update_param(weights,biases,dws,dbs,learning_rate)
    
        
        
        if i%10 == 0 and batch_num==num_of_batches-1:
            # acts_valid = predict(x_valid,weights,biases,relu)
            # cost_valid = calculate_cost(acts_valid,y_valid,ny_valid,nx_data)
            #print("cost at iteration",i,denn(cost,max_elem,min_elem))
            zs,acts = forward_pass(xdata_full,weights,biases,relu)
            cost = calculate_cost(acts,ydata_full,ny_data,nx_data)
            print("cost at iteration",i,cost)
            #print("validation cost at iteration",i,denn(cost_valid,max_elem,min_elem))
            # print("validation cost at iteration",i,cost_valid)
    
    zs,acts = forward_pass(xdata_full,weights,biases,relu)
    cost = calculate_cost(acts,ydata_full,ny_data,nx_data)
    costs_map.append(cost)
  
costs_maps.append(costs_map) #relu cost append



costs_map = []
iter_map = []
num_of_batches=xdata_ok.shape[1]/batch_size
print( "len_x",xdata_ok.shape[1],"num_batches",num_of_batches)
k=zip(xdata_ok.T,ydata_ok.T)

max_elem=np.max(ny_data)
min_elem=np.min(ny_data)
for i in range(e) :
    
    random.shuffle(k)
    xdata_full,ydata_full=zip(*k)
    xdata_full=np.array(xdata_full).T
    ydata_full=np.array(ydata_full).T
    
    for batch_num in range(num_of_batches):

        #xdata=np.array(xdata_full[batch_size*batch_num:batch_size*(batch_num+1)])
        xdata=xdata_full[:,batch_size*batch_num:batch_size*(batch_num+1)]
        #print "Xxx",xdata.shape
        #exit()
        #print X[batch_size*batch_num:batch_size*(batch_num+1):1]
        #ydata=np.array([ydata_full[batch_size*batch_num:batch_size*(batch_num+1)]])
        ydata=ydata_full[:,batch_size*batch_num:batch_size*(batch_num+1)]

        zs,acts = forward_pass(xdata,weights,biases,tanh)
        # cost = calculate_cost(acts,ydata_full)
        # acts_valid = predict(x_valid,weights,biases,tanh)
        # cost_valid = calculate_cost(acts_valid,y_valid)
        dzs,dws,dbs = backward_pass(xdata,ydata,zs,acts,weights,biases,"tanh")
        weights,biases = update_param(weights,biases,dws,dbs,learning_rate)
    
        
        
        if i%10 == 0 and batch_num==num_of_batches-1:
            # acts_valid = predict(x_valid,weights,biases,relu)
            # cost_valid = calculate_cost(acts_valid,y_valid,ny_valid,nx_data)
            #print("cost at iteration",i,denn(cost,max_elem,min_elem))
            zs,acts = forward_pass(xdata_full,weights,biases,relu)
            cost = calculate_cost(acts,ydata_full,ny_data,nx_data)
            print("cost at iteration",i,cost)
            #print("validation cost at iteration",i,denn(cost_valid,max_elem,min_elem))
            # print("validation cost at iteration",i,cost_valid)
    
    zs,acts = forward_pass(xdata_full,weights,biases,tanh)
    cost = calculate_cost(acts,ydata_full,ny_data,nx_data)
    costs_map.append(cost)

  
costs_maps.append(costs_map) #tanh cost convergence




costs_map = []
iter_map = []
num_of_batches=xdata_ok.shape[1]/batch_size
print( "len_x",xdata_ok.shape[1],"num_batches",num_of_batches)
k=zip(xdata_ok.T,ydata_ok.T)

max_elem=np.max(ny_data)
min_elem=np.min(ny_data)
for i in range(e) :
    
    random.shuffle(k)
    xdata_full,ydata_full=zip(*k)
    xdata_full=np.array(xdata_full).T
    ydata_full=np.array(ydata_full).T
    
    for batch_num in range(num_of_batches):

        #xdata=np.array(xdata_full[batch_size*batch_num:batch_size*(batch_num+1)])
        xdata=xdata_full[:,batch_size*batch_num:batch_size*(batch_num+1)]
        #print "Xxx",xdata.shape
        #exit()
        #print X[batch_size*batch_num:batch_size*(batch_num+1):1]
        #ydata=np.array([ydata_full[batch_size*batch_num:batch_size*(batch_num+1)]])
        ydata=ydata_full[:,batch_size*batch_num:batch_size*(batch_num+1)]

        zs,acts = forward_pass(xdata,weights,biases,sigmoid)
        # cost = calculate_cost(acts,ydata_full)
        # acts_valid = predict(x_valid,weights,biases,tanh)
        # cost_valid = calculate_cost(acts_valid,y_valid)
        dzs,dws,dbs = backward_pass(xdata,ydata,zs,acts,weights,biases,"sigmoid")
        weights,biases = update_param(weights,biases,dws,dbs,learning_rate)
    
        
        
        if i%10 == 0 and batch_num==num_of_batches-1:
            # acts_valid = predict(x_valid,weights,biases,relu)
            # cost_valid = calculate_cost(acts_valid,y_valid,ny_valid,nx_data)
            #print("cost at iteration",i,denn(cost,max_elem,min_elem))
            zs,acts = forward_pass(xdata_full,weights,biases,relu)
            cost = calculate_cost(acts,ydata_full,ny_data,nx_data)
            print("cost at iteration",i,cost)
            #print("validation cost at iteration",i,denn(cost_valid,max_elem,min_elem))
            # print("validation cost at iteration",i,cost_valid)
    
    zs,acts = forward_pass(xdata_full,weights,biases,relu)
    cost = calculate_cost(acts,ydata_full,ny_data,nx_data)
    costs_map.append(cost)
  
costs_maps.append(costs_map) #sigmoid cost convergence



iter_map = []
for ee in range(e):
    iter_map.append(ee)
p1 = plt.plot(iter_map,costs_maps[0],color="green")
p2 = plt.plot(iter_map,costs_maps[1],color="blue")
p3 = plt.plot(iter_map,costs_maps[2],color="red")
# p4 = plt.plot(iter_map,costs_maps[3],color="blue")    
plt.gca().legend(( 'relu', 'tanh','sgmd'))
plt.show()  


 

    

