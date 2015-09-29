#implements the transient inverse method of approximating bedrock topography from Michel-Griesser et al 2014

def compare_bedrock(b0, b): #sums up the difference between each point to get a total difference
	difference = 0
	for i in len(b):
		difference += abs(b[i]-b0[i])
	return difference

#using JamesO's bedrock guess as the initial bedrock topography. This may be a bad call since I tuned the model to it, but we'll see.
f = open ('beddata.txt', 'r')
b0 = [float(line) for line in f.readlines()] #topmost point is at 1250 m
f.close()
b = np.zeros(len(b0)) #initializing it to all zeros so difference will be greater than delta, so it won't just skip the model part entirely.
s = np.zeros(len(b0))#figure out some way to more or less guess at entire surface topography.

#TODO
#create observed surface file w/ height at each node.
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

while(compare_bedrock(b0, b) > 10): #i have no idea about this parameter i'm just screwing around
	#solve forward problem
	run = isothermalISM(55, 1000, 0.0002, 'run1.nc', b0) 
	for i in range(5000): #5000 years
    	run1.timestep(1, mbal)
    	if(i%100==0): 
        	print ('on timestep', i)
	h = run.get_ice_thickness()
	#superimpose bedrock calculated from surface on bedrock now


	#set bedrock to surface - height


