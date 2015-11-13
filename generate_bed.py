import tools
import random
import matplotlib.pyplot as mp
import numpy as np

nodes = 58
base = tools.load_nolan_bedrock()


def local_smoother1D(line,repeat):
    
	if (repeat<1):
		return line

	length=len(line)

	calcspace=np.zeros(length)

	#averages each point with neighbors, recursive for levels of smoothing
	calcspace[0]=(line[0]+line[1])/2.   
	calcspace[length-1]=(line[length-1]+line[length-2])/2. 

	for i in range(1,length-1):
		calcspace[i]=(line[i-1]+line[i]+line[i+1])/3.

	return local_smoother1D(calcspace,repeat-1)

def generate_bed(parameters): #length=1,levels=1,minz=0,maxz=1,smoother=0
	zrange = parameters[0] * 50
	smoothing_levels = parameters[1]
		
	bed = [0]
	for i in range(1, nodes-1):
		bed.append(random.uniform(-zrange, zrange)) 
	bed.append(0)
	for i in range(smoothing_levels):
		new = bed[:]
		new[0]=(bed[0]+bed[1])/2.   
		new[nodes-1]=(bed[nodes-1]+bed[nodes-2])/2. 

		for j in range(1,nodes-1):
			new[j]=(bed[j-1]+bed[j]+bed[j+1])/3.
		bed = new[:]
	for i in range(nodes):
		bed[i] += base[i]
	return bed #this needs to be a LIST not a numpy array

	#also consider: quadratic regression of some kind on randomly generated data points???

def topohandler(parameters):
	levels=parameters[0]
	length=nodes

	calcspace=np.zeros((levels,length))
	topo=np.zeros((length))
	zrange=parameters[2]-parameters[1]

	#calculates random value for every index in calcspace (length * levels)
	for i in range(levels):
		for j in range(length):
			calcspace[i,j]=random.random()
        
	for i in range(levels):    
		#print (levels-i)-1
		calcspace[i]=local_smoother1D(calcspace[i],i+parameters[3])
		scale=1./(2**(levels-1-i)) 
		#print "i "+str(i)+" scale"+str(scale)
		maxval=np.amax(calcspace[i])
		minval=np.amin(calcspace[i])  
		scale=scale/(maxval-minval)
		calcspace[i]=(calcspace[i]-minval)*scale

		#print
		#print calcspace[i]


	for j in range(length):       
		topo[j]=np.sum(calcspace[0:levels,j])

	maxval=np.amax(topo)
	minval=np.amin(topo)

	if (maxval==minval):
		valrange=1.
	else:
		valrange=1./(maxval-minval)

	topo=(((topo-minval)*valrange)*zrange)+parameters[1]

	return topo


def main():
	test = generate_bed((10, 5))
	real = tools.load_nolan_bedrock()
	print len(test)
	print len(real)
	mp.plot(range(58), real, 'green')
	mp.plot(range(58), test, 'red')


	mp.show()



if __name__=='__main__':
    main()