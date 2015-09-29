#implements the transient inverse method of approximating bedrock topography from Michel-Griesser et al 2014

def compare_bedrock(b0, b): #sums up the difference between each point to get a total difference
	difference = 0
	for i in len(b):
		difference += abs(b[i]-b0[i])
	return difference

#using JamesO's bedrock guess as the initial bedrock topography. This may be a bad call since I tuned the model to it, but we'll see.
f = open ('beddata.txt', 'r')
b0 = [float(line) for line in infile.readlines()] #topmost point is at 1250 m
f.close()
b = np.zeros(len(b0)) #initializing it to all zeros so difference will be greater than delta, so it won't just skip the model part entirely.

while(compare_bedrock(b0, b) > 10): #i have no idea about this parameter i'm just screwing around
	#solve forward problem
	#solve weird equation thing
	#set bedrock to surface - height

