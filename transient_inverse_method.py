#implements the transient inverse method of approximating bedrock topography from Michel-Griesser et al 2014

import numpy as np
import basic_model
import tools
import matplotlib.pyplot as mp
import scipy.ndimage.filters as sp

def compare_bedrock(b0, b): #sums up the squared difference between each point to get a total difference
	difference = 0
	for i in range(len(b)):
		difference += (b[i]-b0[i])**2
	return difference

#using JamesO's bedrock guess as the initial bedrock topography. This may be a bad call since I tuned the model to it, but we'll see.

bedrock = tools.load_nolan_bedrock() #initializing it to all zeros so difference will be greater than delta, so it won't just skip the model part entirely.
b0 = np.zeros(len(bedrock))
s = np.zeros(len(bedrock))#figure out some way to more or less guess at entire surface topography.
b = bedrock[:] #keeps unchanged copy for plotting
#TODO
#try a different b0 estimate?

#import observed surface data
observed_surface=tools.load_first_guess_surface()

relaxation = 1 #value from paper
regularization = 100 #100 is value from paper. adjust?

iterations = 0 #to keep track of about how long it runs

x_distances = range(0, 58000, 1000) #for plotting



while(compare_bedrock(b0, b) > 5700): #i have no idea about this parameter i'm just screwing around
	iterations += 1

	#solve forward problem
	b0 = b[:]
	run = basic_model.isothermalISM(58, 1000, 0.0005, b0[:]) 
	for i in range(5000): #5000 years
    		run.timestep(1)
    	if(i%100==0): 
        	print ('on timestep', i)
	h = run.get_ice_thickness()
	h = h[0:58] #remove extra part of model (move to w/in model thing?)

	#superimpose bedrock calculated from surface on bedrock now
	delta_h = np.zeros(len(h))
	sp.laplace(h, delta_h) #i have no idea if this is an appropriate thing to do to calculate laplacian term
	for i in range(len(h)):
		h[i] = h[i] + relaxation*(b0[i] + h[i] - observed_surface[i]) #+ regularization*relaxation*delta_h[i] #what is this last part, i don't even know

	#set bedrock to surface - height
	for i in range(len(b)):
		b[i] = observed_surface[i] - h[i]

	mp.plot(x_distances, observed_surface, 'green')
	mp.plot(x_distances, (b0 + h), 'red')
	mp.plot(x_distances, bedrock, 'blue')
	mp.plot(x_distances, b, 'black')
	mp.title('%f' %compare_bedrock(b, b0))
	mp.savefig('run%d.jpg' %iterations)
	mp.clf() #clear figure??

print b