import numpy as np
import random
import genetic_tools as gt
import basic_model
import evaluate

class Population(object):

	class Individual(object):

		def __init__(self, parameters):
			self.parameters = parameters

	def __init__(self, size, length, param_range, fitness_function):
		self.n = size
		self.individuals = np.empty(size, dtype=object)
		self.param_range = param_range
		for i in range(size):
			self.individuals[i] = self.Individual((1,2,3,4,5))#gt.create(length, param_range))
		self.mutation_rate = 1.0/length
		self. pool_size = 10
		self.fitness_function = fitness_function

	def best_fitness(self):
		best = float("inf")
		for i in range(self.n):
			current = self.fitness_function.evaluate_bed(self.individuals[i].bed, self.individuals[i].surface)
			if(current < best):
				best = current
		return best

	def choose(self): #returns the index in self.individuals of the fittest of the 10
		best = float("inf")
		best_index = -1
		for i in range(self.pool_size):
			index = random.randint(0, self.n-1)
			current = self.fitness_function.evaluate_bed(self.individuals[index].bed, self.individuals[index].surface)
			if(current > best):
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

	def run_models(self):
		for i in range(self.n):
			self.individuals[i].bed = gt.generate_bed(self.individuals[i].parameters)
			run = basic_model.isothermalISM(58, 1000, .0015, .0005, .00022, self.individuals[i].bed[:])
			for j in range(2000):
				run.timestep(1)
			self.individuals[i].surface = run.get_surface_elev()


def main():
	fitness_function = evaluate.FitnessFunction()
	population = Population(2, 5, 10, fitness_function)
	population.run_models()
	population.evolve()
	population.run_models()
	print population.best_fitness()



if __name__=='__main__':
    main()
