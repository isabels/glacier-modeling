import numpy as np
import random
import genetic_tools as gt
import basic_model
import evaluate
import generate_bed as bed
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
			new_generation[i] = Individual(gt.mutate(child, self.mutation_rate, self.zmin, self.zmax))
			new_generation[i]
		self.individuals = new_generation
		self.generation += 1

	# def run_model(self, parameters, base, fitness_function): #runs one model. to make things parallelizable


	def run_models(self, job_server):
		for i in range(self.n):
			self.individuals[i].bed = map(operator.add, self.individuals[i].parameters, self.base)

		# sum_primes - the function
# (100,) - tuple with arguments for sum_primes
# (isprime,) - tuple with functions on which function sum_primes depends
# ("math",) - tuple with module names which must be imported before sum_primes execution
# Execution starts as soon as one of the workers will become available
		print 'in run models'
		# jobs = [(i, job_server.submit(self.run_model,(self.individuals[i].parameters,self.base, self.fitness_function), (), ())) for i in range(self.n)]
		jobs = [(i, job_server.submit(run_model,(self.individuals[i].bed, basic_model.isothermalISM(58, 1500, .0015, .0005, .00022, self.individuals[i].bed[:]), self.fitness_function), (), ("operator", "basic_model", "tools"))) for i in range(self.n)]

		print 'jobs created!'
		print jobs
		for i, job in jobs:
			print 'in for loop, about to call job'
			self.individuals[i].fitness = job()
			print 'on individual', i, 'of', self.n
			print 'fitness', self.individuals[i].fitness
		# for i in range(self.n):
			# self.individuals[i].bed = map(add, self.base, self.individuals[i].parameters)
			# run = basic_model.isothermalISM(58, 1500, .0015, .0005, .00022, self.individuals[i].bed[:])
			# for j in range(2000):
			# 	run.timestep(1)

			#job1 = job_server.submit(sum_primes, (100,), (isprime,), ("math",))
			
			#self.individuals[i].surface = self.run_model(self.individuals[i].bed[:])
			# self.individuals[i].fitness = self.run_model(self.individuals[i].parameters, self.base, self.fitness_function)
			# print 'on individual', i, 'of', self.n
			# print 'fitness', self.individuals[i].fitness

	def save_iteration(self, filename):
		with open(filename, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			for i in range(self.n):
				writer.writerow([str(self.individuals[i].parameters).strip('"[]"'), self.individuals[i].fitness])

	def load_iteration(self, filename):
		return False # implement this when you need it, future isabel, i don't care

def run_model(bed, run, fitness_function): #runs one model. to make things parallelizable
	for j in range(2000):
		run.timestep(1)
	surf = run.get_surface_elev()
	fitness = fitness_function.evaluate(bed, surf)

	return fitness
	# return surf

def main():
	job_server = pp.Server()
	print 'Currently using', job_server.get_ncpus(), 'cpus'
	fitness_function = evaluate.FitnessFunction()
	population = Population(5, 58, -500, 500, fitness_function)
	population.run_models(job_server) #initial run at generation 0 before we start evolving
	
	# best fitness can't be computed until after models are all run. so makes sense to start while loop after initial run of models
	
	# while(population.best_fitness() > 500):
	# 	population.evolve()
	# 	population.run_models(job_server)
	# 	print population.best_fitness(True) #now this reflects generation that has just been done
	# 	population.save_iteration('generation%d.csv' % population.generation)




if __name__=='__main__':
    main()
