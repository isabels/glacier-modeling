#implements the transient inverse method of approximating bedrock topography from Michel-Griesser et al 2014

import numpy as np
import basic_model
import tools

def compare_bedrock(b0, b): #sums up the difference between each point to get a total difference
	difference = 0
	for i in range(len(b)):
		difference += abs(b[i]-b0[i])
	return difference

#using JamesO's bedrock guess as the initial bedrock topography. This may be a bad call since I tuned the model to it, but we'll see.
f = open ('beddata.txt', 'r')
b = [float(line) for line in f.readlines()] #topmost point is at 1250 m
f.close()
b0 = np.zeros(len(b)) #initializing it to all zeros so difference will be greater than delta, so it won't just skip the model part entirely.
s = np.zeros(len(b))#figure out some way to more or less guess at entire surface topography.

#TODO
#X create observed surface file w/ height at each node.
#make sure to account/de-account for extra 20 nodes past end of glacier in various calculations
#try a different b0 estimate?
#probably should create a file with the actual known bedrock points
#read adhikari and marshall
#conference grant writeup
#frickin email kiya
#look into better A value
#maaaaaaaybe pester allen?
#maaaaaaaaybe ask kiya for DEM?
#actually implement the rest of this
#ALSO ALSO ALSO try running the model w/ full number of nodes (dunno what to do about bedtopo though)

#import observed surface data
f = open('first_guess_surface.csv', 'r')
observed_surface=[]
for line in f.readlines():
    data = line.split(',')
    observed_surface.append(float(data[1]))
f.close()

relaxation = 1 #value from paper
regularization = 100 #value from paper. adjust?

iterations = 0 #to keep track of about how long it runs

while(compare_bedrock(b0, b) > 100): #i have no idea about this parameter i'm just screwing around
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
	delta_h = tools.calculate_slopes(h, 1000)
	print len(h), len(delta_h), len(observed_surface), len(b0)
	for i in range(len(h)):
		h[i] = h[i] + relaxation*(b0[i] + h[i] - observed_surface[i]) + regularization*relaxation*delta_h[i] #what is this last part, i don't even know

	#set bedrock to surface - height
	for i in range(len(b)):
		b[i] = observed_surface[i] - h[i]

print b



