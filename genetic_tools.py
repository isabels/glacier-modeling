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


#using creep mutation (mutate by adding/subtracting from current number)
def mutate(s, rate, zmin, zmax):
	temp = []
	for i in range(len(s)):
		if(random.random() <= rate):
			temp.append(s[i] + random.gauss(0, 75)) #SD of 160 should lead to max values of about 500? maybe this should be in general smaller. should i just have it move each by like at most 50 each time???????
			if temp[i] > zmax:
				temp[i] = zmax #can't get out of 500m range
			elif temp[i] < zmin:
				temp[i] = zmin #can't get outside of 500m range
		else:
			temp.append(s[i])
	return temp

#generates a random topo based on the nolan topo with randomized ranges and smoothing levels
def create(length, zmin, zmax):
	zrange = random.randint(zmin, zmax) #picks randomly but does not go over max. difference
	smoothing_levels = random.randint(0, 10)
		
	bed = [0] #first and last vals have to be 0 (constraining exactly at those points)
	for i in range(1, length-1):
		bed.append(random.uniform(-zrange, zrange)) 
	bed.append(0)
	for i in range(smoothing_levels):
		new = bed[:]
		new[0]=(bed[0]+bed[1])/2.   
		new[length-1]=(bed[length-1]+bed[length-2])/2. 

		for j in range(1,length-1):
			new[j]=(bed[j-1]+bed[j]+bed[j+1])/3.
		bed = new[:]
	return bed


