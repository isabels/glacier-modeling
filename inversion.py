#all the code (?) to run the model inversion. yay, doing actual things!!
import tools
import basic_model

def constrain_to_nolan(bed_elev):
	nodes_to_check = (1,5, 12, 20, 32)
	expected_values = (-70,-200, -500, -600, -250)
	error = 50 #a rough average between the 30 for one reading and the 150 for the other. Welp.
	for node,val in zip(nodes_to_check, expected_values):
		if (bed_elev[node] > val + error) or (bed_elev[node] < val - error):
			return float("inf")
	return 0

def constrain_to_reality(bed_elev, nolan_elev):
	error = 500 #who knows. this is to prevent things from getting wildly out of hand w/o constraining too tightly to first guess.
	for i in range(len(bed_elev)-1):
		if(abs(bed_elev[i] - bed_elev[i+1]) > 150): #largest jump in basic bedtopo is about 80, so this might be reasonable?
			return float("inf")
		if((bed_elev[i] > nolan_elev[i] + error) or (bed_elev[i] < nolan_elev[i] - error)):
			return float("inf")
	return 0


#function to evaluate fitness of the bed, returns number which is fitness, lower is better
def evaluate_bed(bed_elev, surf_elev, nolan_elev, gps_elev):
	return constrain_to_reality(bed_elev, nolan_elev) + constrain_to_nolan(bed_elev) + tools.calculate_surface_difference(surf_elev, gps_elev)
	#constrain to realistic data (no huge spikes)
	#constrain to reality via not more than 500 from bedtopo? (or is this more or less included in the other ones)

# CONSTRUCT BED: given tuple of variables, constructs a bed
# RUN MODEL: runs model on constructed bed. this plus construct bed give what ya need for the evaluating

#

def main():
	bed = tools.load_nolan_bedrock()
	gps_surf = tools.load_first_guess_surface()
	run = basic_model.isothermalISM(58, 1000, .0015,.0005,.00022, bed[:])
	for n in range(1000):
		run.timestep(1)
	print evaluate_bed(bed, run.get_surface_elev(), bed, gps_surf)


if __name__=='__main__':
    main()
