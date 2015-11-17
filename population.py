import numpy as np
import random
import genetic_tools as gt
import basic_model
import evaluate
import generate_bed as bed
import tools
import csv
from operator import add 

class Population(object):

	base = tools.load_nolan_bedrock()

	class Individual(object):

		def __init__(self, parameters):
			self.parameters = parameters
			self.fitness = float("inf")

		def to_string(self):
			print self.parameters, self.fitness

	def __init__(self, size, length, zmin, zmax, fitness_function):
		self.generation = 0
		self.n = size #is NUMBER OF INDIVIDUALS
		self.individuals = np.empty(size, dtype=object)
		self.zmin = zmin
		self.zmax = zmax
		for i in range(self.n):
			self.individuals[i] = self.Individual(gt.create(length, zmin, zmax))#gt.create(length, param_range))
		self.mutation_rate = 1.0/length
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self. pool_size = 10 #CHANGE THIS BACK!!!!!! #this is how many you pick the best for for evolution. NOT the population size.
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.fitness_function = fitness_function

	def best_fitness(self, return_index=False): #will return the index of best one as well when index is true
		best = float("inf")
		index = -1
		for i in range(self.n):
			if(self.individuals[i].fitness < best):
				best = self.individuals[i].fitness
				index = i
		if(return_index):
			return (index, best)
		else:
			return best

	def choose(self): #returns the index in self.individuals of the fittest of the 10
		best = float("inf")
		best_index = -1
		for i in range(self.pool_size):
			index = random.randint(0, self.n-1)
			if(self.individuals[index].fitness < best):
				best = self.individuals[index].fitness
				best_index = index
		return(self.individuals[best_index])

	def evolve(self):
		new_generation = np.empty(self.n, dtype=object)
		for i in range(self.n): #this completely replaces each generation. ???
			a = self.choose()
			b = self.choose()
			child = gt.cross(a.parameters, b.parameters, .7)
			new_generation[i] = self.Individual(gt.mutate(child, self.mutation_rate, self.zmin, self.zmax))
			new_generation[i]
		self.individuals = new_generation
		self.generation += 1

	def run_models(self):
		for i in range(self.n):
			self.individuals[i].bed = map(add, self.base, self.individuals[i].parameters)
			run = basic_model.isothermalISM(58, 1500, .0015, .0005, .00022, self.individuals[i].bed[:])
			for j in range(2000):
				run.timestep(1)
			self.individuals[i].surface = run.get_surface_elev()
			self.individuals[i].fitness = self.fitness_function.evaluate(self.individuals[i].bed, self.individuals[i].surface)
			print 'on individual', i, 'of', self.n
			print 'fitness', self.individuals[i].fitness


	def save_iteration(self, filename):
		with open('filename', 'wb') as csvfile:
			writer = csv.writer(csvfile)
			for i in range(self.n):
				writer.writerow([str(self.individuals[i].parameters).strip('[]'), self.individuals[i].fitness])

	def load_iteration(self, filename):
		return False # implement this when you need it, future isabel, i don't care


def main():
	fitness_function = evaluate.FitnessFunction()
	#population = Population(500, 58, -500, 500, fitness_function)
	population = Population(5, 58, -500, 500, fitness_function)
	population.run_models() #initial run at generation 0 before we start evolving
	
	# best fitness can't be computed until after models are all run. so makes sense to start while loop after initial run of models
	
	while(population.best_fitness() > 500):
		population.evolve()
		population.run_models()
		print population.best_fitness(True) #now this reflects generation that has just been done
		population.save_iteration('gen%d' % population.generation)




if __name__=='__main__':
    main()
