import random
import tools

#a bunch of methods to change specific strings

def cross(a, b, cross_probability):
	if(random.random() <= cross_probability):
		cross_point = random.randint(0, len(a)-1)
		#TODO should this return one or two children? as in, should it return just one kid or that kid and it's inverse 
		x = a[:cross_point] + b[cross_point:]
		#y = b[:cross_point] + a[cross_point:]
		return x
	else:
		return a #is this a source of bias??? is this weird???? help.....
	# 	return (x,y)
	# else:
	# 	return (a,b)

def mutate(s, rate, poss_range):
	temp = []
	for i in range(len(s)):
		if(random.random() <= rate):
			temp.append(random.randint(0, poss_range-1))
		else:
			temp.append(s[i])
	return temp

#generates a random topo based on the nolan topo with randomized ranges and smoothing levels
def create(length, zmin, zmax):
	zrange = random.randint(zmin, zmax) * 10
	smoothing_levels = random.randint(0, 10)
		
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
	return bed


