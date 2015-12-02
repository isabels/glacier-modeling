#code based on example code on the parallel python website.

import pp
import math, sys, time

def isprime(n):
	"""Returns True if n is prime and False otherwise"""
	if not isinstance(n, int):
		raise TypeError("argument passed to is_prime is not of 'int' type")
	if n < 2:
		return False
	if n == 2:
		return True
	max = int(math.ceil(math.sqrt(n)))
	i = 2
	while i <= max:
		if n % i == 0:
			return False
		i += 1
	return True

def sum_primes(n):
	"""Calculates sum of all primes below given integer n"""
	return sum([x for x in xrange(2,n) if isprime(x)])



# tuple of all parallel python servers to connect with


# Creates jobserver with automatically detected number of workers (can also specify)
job_server = pp.Server()

print "Starting pp with", job_server.get_ncpus(), "workers\n"

# Submit a job of calulating sum_primes(100) for execution. 
# sum_primes - the function
# (100,) - tuple with arguments for sum_primes
# (isprime,) - tuple with functions on which function sum_primes depends
# ("math",) - tuple with module names which must be imported before sum_primes execution
# Execution starts as soon as one of the workers will become available
job1 = job_server.submit(sum_primes, (100,), (isprime,), ("math",))

# Retrieves the result calculated by job1
# The value of job1() is the same as sum_primes(100)
# If the job has not been finished yet, execution will wait here until result is available
#result = job1()

#print "Sum of primes below 100 is", result

#for calculates a whole bunch of sums of primes ten times, prints time elapsed in serial and parallel each time.
parallel_total = 0
serial_total = 0
for i in range(10):
	start_time = time.time()
	print "Calculating primes in parallel:"
	#note that the different sums are happening in parallel, but each individual call to sum of primes is not parallelized.
	# The following submits  jobs and then retrieves the results
	inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700, 100800, 100900, 101000, 101100, 101200, 101300, 101400, 101500, 101600)
	jobs = [(input, job_server.submit(sum_primes,(input,), (isprime,), ("math",))) for input in inputs]
	for input, job in jobs:
		print "Sum of primes below", input, "is", job()

	print "Time elapsed: ", time.time() - start_time, "s\n\n"
	parallel_total += time.time()-start_time
	#job_server.print_stats()

	print 'Calculating primes in serial:'
	start_time = time.time()
	inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700, 100800, 100900, 101000, 101100, 101200, 101300, 101400, 101500, 101600)
	for input in inputs:
		print "Sum of primes below", input, "is", sum_primes(input)
	print 'Time elapsed: ', time.time() - start_time, 's\n\n'
	serial_total += time.time() - start_time
# Parallel Python Software: http://www.parallelpython.com

print 'Average times to complete:'
print 'Parallel', parallel_total / 10
print 'Serial', serial_total / 10

