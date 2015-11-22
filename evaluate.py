#all the code (?) to run the model inversion. yay, doing actual things!!
import tools
import basic_model

class FitnessFunction(object):
	penalty = 1000.

	def __init__(self):
		self.gps_surface = tools.load_first_guess_surface()
		self.nolan_bed = tools.load_nolan_bedrock()

	def constrain_to_nolan(self,bed_elev):
		nodes_to_check = (1,5, 12, 20, 32)
		expected_values = (-70,-200, -500, -600, -250)
		error = 100 #a rough average between the 30 for one reading and the 150 for the other. Welp.
		for node,val in zip(nodes_to_check, expected_values):
			if (bed_elev[node] > val + error) or (bed_elev[node] < val - error):
				return self.penalty
		return 0

	def constrain_to_reality(self,bed_elev):
		error = 500 #who knows. this is to prevent things from getting wildly out of hand w/o constraining too tightly to first guess.
		for i in range(len(bed_elev)-1):
			if(abs(bed_elev[i] - bed_elev[i+1]) > 150): #largest jump in basic bedtopo is about 80, so this might be reasonable?
				return self.penalty
			if((bed_elev[i] > self.nolan_bed[i] + error) or (bed_elev[i] < self.nolan_bed[i] - error)):
				return self.penalty
		return 0


	#function to evaluate fitness of the bed, returns number which is fitness, lower is better
	def evaluate(self,bed_elev, surf_elev):
		return self.constrain_to_reality(bed_elev) + self.constrain_to_nolan(bed_elev) + tools.calculate_surface_difference(surf_elev, self.gps_surface)
		#constrain to realistic data (no huge spikes)
		#constrain to reality via not more than 500 from bedtopo? (or is this more or less included in the other ones)

def main():
	bed = tools.load_nolan_bedrock()
	gps_surf = tools.load_first_guess_surface()
	run = basic_model.isothermalISM(58, 1000, .0015,.0005,.00022, bed[:])
	for n in range(1000):
		run.timestep(1)
	print evaluate_bed(bed, run.get_surface_elev())


if __name__=='__main__':
    main()
