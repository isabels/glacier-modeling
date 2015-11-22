import random
import tools
import matplotlib.pyplot as mp
import operator
import basic_model
import evaluate

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
			temp.append(s[i] + random.gauss(0, 40)) #SD of 160 should lead to max values of about 500? maybe this should be in general smaller. should i just have it move each by like at most 50 each time???????
			if temp[i] > zmax:
				temp[i] = zmax #can't get out of 500m range
			elif temp[i] < zmin:
				temp[i] = zmin #can't get outside of 500m range
		else:
			temp.append(s[i])
	return temp

#generates a random topo based on the nolan topo with randomized ranges and smoothing levels
def create(length, zmin, zmax):
	zrange = random.randint(0, zmax) #picks randomly but does not go over max. difference
	smoothing_levels = random.randint(2, 10)
		
	bed = [0] #first and last vals have to be 0 (constraining exactly at those points)
	for i in range(1, length-1):
		bed.append(random.uniform(-zrange, zrange)) 
	bed.append(0)
	for i in range(smoothing_levels):
		new = bed[:]
		for j in range(1,length-1):
			new[j]=(bed[j-1]+bed[j]+bed[j+1])/3.
		bed = new[:]
	return bed


def main():
	ff = evaluate.FitnessFunction()
	base = tools.load_nolan_bedrock()
	surf = tools.load_first_guess_surface()
	for i in range(9):
		mp.plot(range(58), base, 'red')
		params = create(58, -500, 500)
		bed = map(operator.add, params, base)
		mp.plot(range(58), bed, 'blue')
		run1 = basic_model.isothermalISM(58, 1000, 0.0015, .0005, 0.00022, bed[:]) #55 nodes, 1000-meter spacing,  basal slip was .0005

		for i in range(1500): #5000 years
			run1.timestep(1)
			if(i%100==0): 
				print 'on timestep', i
		mp.plot(range(58), run1.get_surface_elev()[:58])
		mp.plot(range(57), surf, 'red')
		mp.scatter([1,5, 12, 20, 32],[-70,-200, -500, -600, -250], )
		print 'surface difference:', tools.calculate_surface_difference(surf, run1.get_surface_elev()[:58])
		print 'evaluate surface difference:', ff.evaluate(bed, run1.get_surface_elev())
		mp.show()

if __name__ == '__main__':
	main()


