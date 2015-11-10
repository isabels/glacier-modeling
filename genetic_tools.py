import random

#a bunch of methods to change specific strings

def cross(a, b, cross_probability):
	if(random.random() <= cross_probability):
		cross_point = random.randint(0, len(a)-1)
		#TODO should this return one or two children? as in, should it return just one kid or that kid and it's inverse (yes)
		x = a[:cross_point] + b[cross_point:]
		y = b[:cross_point] + a[cross_point:]
		return (x,y)
	else:
		return (a,b)

def mutate(s, rate, poss_range):
	temp = []
	for i in range(len(s)):
		if(random.random() <= rate):
			temp.append(random.randint(0, poss_range-1))
		else:
			temp.append(s[i])
	return tuple(temp)

def create(length, poss_range):
	temp = []
	for i in range(length):
		temp.append(random.randint(0, poss_range-1))
	return tuple(temp)

