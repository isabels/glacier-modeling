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
f = open ('beddata.txt', 'r')
bedrock = [float(line) for line in f.readlines()] #topmost point is at 1250 m
f.close()
b0 = np.zeros(len(bedrock)) #initializing it to all zeros so difference will be greater than delta, so it won't just skip the model part entirely.
s = np.zeros(len(bedrock))#figure out some way to more or less guess at entire surface topography.
b = bedrock[:] #keeps unchanged copy for plotting
#TODO
#try a different b0 estimate?
#probably should create a file with the actual known bedrock points
#read adhikari and marshall
#frickin email kiya
#look into better A value
#maaaaaaaybe pester allen?
#maaaaaaaaybe ask kiya for DEM?
#ALSO ALSO ALSO try running the model w/ full number of nodes (dunno what to do about bedtopo though)

#import observed surface data
f = open('first_guess_surface.csv', 'r')
observed_surface=[]
for line in f.readlines():
    data = line.split(',')
    observed_surface.append(float(data[1]))
f.close()

relaxation = 1 #value from paper
regularization = 1 #100 is value from paper. adjust?

iterations = 0 #to keep track of about how long it runs

x_distances = range(0, 55000, 1000) #for plotting

while(compare_bedrock(b0, b) > 550): #i have no idea about this parameter i'm just screwing around
	iterations += 1

	#solve forward problem
	b0 = b[:]
	run = basic_model.isothermalISM(55, 1000, 0.0002, b0[:]) 
	for i in range(5000): #5000 years
    		run.timestep(1)
    	if(i%100==0): 
        	print ('on timestep', i)
	h = run.get_ice_thickness()
	h = h[0:55] #remove extra part of model (move to w/in model thing?)

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



