#all the code (?) to run the model inversion. yay, doing actual things!!
import tools
import basic_model

class FitnessFunction(object):

	#function to evaluate fitness of the bed, returns number which is fitness, lower is better
	def evaluate(self, parameters):
		#(a, b, c, d, e, f, g, h) all integers in range 0-99 (8 parameters)
		# minimize
		return sum(list(parameters))



