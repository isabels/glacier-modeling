import numpy as np
import random
import genetic_tools as gt
import basic_model
import evaluate
import generate_bed as bed
import pickle

class Population(object):

	class Individual(object):

		def __init__(self, parameters):
			self.parameters = parameters

		def to_string(self):
			print self.parameters, self.fitness

	def __init__(self, size, length, param_range, fitness_function):
		self.generation = 0
		self.n = size
		self.individuals = np.empty(size, dtype=object)
		self.param_range = param_range
		for i in range(size):
			self.individuals[i] = self.Individual(gt.create(size, param_range))#gt.create(length, param_range))
		self.mutation_rate = 1.0/length
		self. pool_size = 10
		self.fitness_function = fitness_function

	def best_fitness(self):
		best = float("inf")
		for i in range(self.n):
			if(self.individuals[i].fitness < best):
				best = current
		return best

	def choose(self): #returns the index in self.individuals of the fittest of the 10
		best = float("inf")
		best_index = -1
		for i in range(self.pool_size):
			index = random.randint(0, self.n-1)
			if(self.individuals[index].fitness < best):
				best = current
				best_index = index
		return(self.individuals[best_index])

	def evolve(self):
		new_generation = np.empty(self.n, dtype=object)
		for i in range(self.n): #this completely replaces each generation. ???
			a = self.choose()
			b = self.choose()
			child = gt.cross(a.parameters, b.parameters, .7)
			new_generation[i] = self.Individual(gt.mutate(child, self.mutation_rate, 10))
		self.individuals = new_generation
		self.generation += 1

	def run_models(self):
		for i in range(self.n):
			self.individuals[i].bed = bed.generate_bed(self.individuals[i].parameters)
			run = basic_model.isothermalISM(58, 1000, .0015, .0005, .00022, self.individuals[i].bed[:])
			for j in range(2000):
				run.timestep(1)
			self.individuals[i].surface = run.get_surface_elev()
			self.individuals[i].fitness = self.fitness_function.evaluate_bed(self.individuals[i].bed, self.individuals[i].surface)
			if(i%10==0):
				print 'on individual', i, 'of', self.n

	def save_iteration(self, filename):
		with open(filename, 'w') as f:
			pickle.dump((self.generation, self.individuals), f)

	def load_iteration(self, filename):
		with open(filename) as f:
			self.generation, self.individuals = pickle.load(f)


def main():
	fitness_function = evaluate.FitnessFunction()
	population = Population(400, 2, 20, fitness_function)
	print 'population created'
	population.run_models()
	population.evolve()
	population.run_models()
	print [item.to_string() for item in population.individuals]



if __name__=='__main__':
    main()
