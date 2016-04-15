#all the code (?) to run the model inversion. yay, doing actual things!!
import tools
import basic_model
import operator

class FitnessFunction(object):
	penalty = 1000.

	def __init__(self, roughness_penalty):
		self.gps_surface = tools.load_first_guess_surface()
		self.nolan_bed = tools.load_nolan_bedrock()
		self.roughness_penalty = roughness_penalty

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
			if(abs(bed_elev[i] - bed_elev[i+1]) > 90): #largest jump in basic bedtopo is about 80, so this might be reasonable?
				return self.penalty
			if((bed_elev[i] > self.nolan_bed[i] + error) or (bed_elev[i] < self.nolan_bed[i] - error)):
				return self.penalty
		return 0

	def smoothness_constraint(self, bed_elev): #penalizes for each wiggle that is not in the direction of the greater slope
		total = 0
		for i in range(1, len(bed_elev)):
			if (i<=20): #sloping down still
				if (bed_elev[i] > bed_elev[i-1]):
					total += self.roughness_penalty
			else: #sloping up now
				if(bed_elev[i] < bed_elev[i-1]):
					total += self.roughness_penalty
		return total


	#function to evaluate fitness of the bed, returns number which is fitness, lower is better
	def evaluate(self,bed_elev, surf_elev):
		return self.constrain_to_reality(bed_elev) + self.constrain_to_nolan(bed_elev) + self.smoothness_constraint(bed_elev) + tools.calculate_surface_difference(surf_elev, self.gps_surface)
		#constrain to realistic data (no huge spikes)
		#constrain to reality via not more than 500 from bedtopo? (or is this more or less included in the other ones)

def main():
	b0 = [-53.86014283247338, -96.55148545680116, -209.56378728526175, -329.5285447843742, -276.1078577736731, -99.4682311472077, -74.60838257235906, 103.76931702628877, 199.59759885797695, 325.49387992076936, 294.9387516971606, 190.74077827555544, 95.99117577626988, 252.4851292030383, 410.3736616110993, 500, 500, 444.71357635367707, 326.35184433516275, 223.25791552817049, 98.55471776145947, 134.18167926051117, 30.336550811088184, -88.39136174706994, -121.36948314990242, -18.45822543176338, -66.01158355801323, 52.93628093781889, -92.66509252409524, 15.70587677548626, -22.132177754463765, 6.391541935525751, -68.42339808954196, 39.59640808291448, 53.464027842215515, 136.78502122848863, 254.14520471035019, 192.5665648106059, 65.30439277418417, 14.10079843084735, -114.02424000705798, -289.4634592194706, -303.0305745281302, -266.62019841090347, -198.4732468197231, -210.421471160374, -143.2408448139692, -66.7972463258127, -18.769521382966776, 46.9742033841991, 105.26603075720368, 164.98279637713722, -43.50064538327361, -79.11047511726842, -3.8891318593645394, 12.390579201231496, -59.56957705146683, 0]
	base = tools.load_nolan_bedrock()
	bed = map(operator.add, base, b0)
	gps_surf = tools.load_first_guess_surface()
	run = basic_model.isothermalISM(58, 1000, .0015,.0005,.00022, bed[:])
	ff = FitnessFunction()
	for n in range(1000):
		run.timestep(1)
	print ff.evaluate(bed, run.get_surface_elev())


if __name__=='__main__':
    main()
