import numpy as np
import random

class population(object):

	def __init__(self, size, length, fitness_function):
		self.n = size
		self.individuals = np.array(size) #individuals would be tuple of params. but, also needs to include bedtopo, surface (for finding best one. probably will need its own wrapper class)
		for i in range(size):
			#TODO initialize each individual randomly
		self.mutation_rate = 1.0/length
		self. pool_size = 10
		self.fitness_function = fitness_function

	def bestFitness(self):
		int best = float("inf")
		for i in range(self.n):
			current = self.fitness_function.evaluate_bed(self.individuals[i])
			if(current < best):
				best = current
		return best

	def choose(self): #returns the index in self.individuals of the fittest of the 10
		best = float("inf")
		best_index = -1
		for i in range(self.pool_size):
			index = random.randint(0, self.n-1)
			current = self.fitness_function.evaluate_bed(self.individuals[index])
			if(current > best):
				best = current
				best_index = index
		return(self.individuals[best_index])

	def evolve(self):
		new_generation = np.array(self.n)
		for i in range(self.n): #this completely replaces each generation. ???
			a = choose()
			b = choose()
			child = #TODO create cross function in the tools
			new_generation[i] = #TODO create mutate function in tools
		self.individuals = new_generation

	#TODO some kind of run function that runs all the models, however that's going to work