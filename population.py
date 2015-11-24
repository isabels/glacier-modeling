import numpy as np
import random
import genetic_tools as gt
import basic_model
import evaluate
import tools
import csv
import operator
import pp

class Individual(object):

	def __init__(self, parameters):
		self.parameters = parameters
		self.fitness = float("inf")


class Population(object):

	base = tools.load_nolan_bedrock()


	def __init__(self, size, length, zmin, zmax, fitness_function):
		self.generation = 0
		self.n = size #is NUMBER OF INDIVIDUALS
		self.individuals = np.empty(size, dtype=object)
		self.zmin = zmin
		self.zmax = zmax
		for i in range(self.n):
			self.individuals[i] = Individual(gt.create(length, zmin, zmax))#gt.create(length, param_range))
		self.mutation_rate = 2.0/length #trying w/ slightly more common mutation. we'll see what happens.
		self. pool_size = 25 #this is how many you pick the best for for evolution. NOT the population size.
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
			new_generation[i] = Individual(gt.mutate(child, self.mutation_rate, self.zmin, self.zmax))
			new_generation[i]
		self.individuals = new_generation
		self.generation += 1

	# def run_model(self, parameters, base, fitness_function): #runs one model. to make things parallelizable


	def run_models(self, parallelize = False, job_server = None): #defaults to running in serial, can make it parallel w/ params.
		if(parallelize):
			for i in range(self.n):
				#gotta do this in serial first, because it's an argument to isothermalISM, which needs to be created in serial (or so it seems. but it's working now so i'm not gonna mess with it)
				self.individuals[i].bed = map(operator.add, self.individuals[i].parameters, self.base)
			#creates list of tuples of i and job running i's model
			jobs = [(i, job_server.submit(run_model,(self.individuals[i].bed, basic_model.isothermalISM(58, 1000, .0015, .0005, .00022, self.individuals[i].bed[:]), self.fitness_function), (), ("operator", "basic_model", "tools"))) for i in range(self.n)]
			print 'jobs created'
			for i, job in jobs:
				self.individuals[i].fitness = job()
				print 'on individual', i, 'of', self.n
				print 'fitness', self.individuals[i].fitness
		else:
			for i in range(self.n):
				self.individuals[i].bed = map(operator.add, self.base, self.individuals[i].parameters)
				run = basic_model.isothermalISM(58, 1000, .0015, .0005, .00022, self.individuals[i].bed[:])
				for j in range(2000):
					run.timestep(1)				
				self.individuals[i].surface = run.get_surface_elev()
				self.individuals[i].fitness = self.fitness_function.evaluate(self.individuals[i].bed, self.individuals[i].surface)
				print 'on individual', i, 'of', self.n
				print 'fitness', self.individuals[i].fitness

	def save_iteration(self, filename):
		with open(filename, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			for i in range(self.n):
				writer.writerow([str(self.individuals[i].parameters).strip('"[]"'), self.individuals[i].fitness])

	def load_iteration(self, filename):
		return False # implement this when you need it, future isabel, i don't care

def run_model(bed, run, fitness_function): #runs one model. for parallelization.
	for j in range(2000):
		run.timestep(1)
	surf = run.get_surface_elev()
	fitness = fitness_function.evaluate(bed, surf[:58])

	return fitness
	# return surf

def main():
	job_server = pp.Server()
	print 'Currently using', job_server.get_ncpus(), 'cpus'
	fitness_function = evaluate.FitnessFunction()
	population = Population(10, 58, -500, 500, fitness_function)
	population.run_models(True,job_server) #initial run at generation 0 before we start evolving
	prev_best_fitness = float("inf")
	while(population.best_fitness() < prev_best_fitness):
		population.evolve()
		population.run_models(True,job_server)
		print population.best_fitness(True) #now this reflects generation that has just been done
		prev_best_fitness = population.best_fitness(False)
		population.save_iteration('generation%d.csv' % population.generation)
	print "best fitness better than 500, program has finished."




if __name__=='__main__':
    main()

#experiments to run/things to do:
#figure out why the hell average starting fitness is so high. it wasn't in my bed parameters tests.
#experiment with larger population (500?)
#something w/ overall smoothing applied after mutation?
