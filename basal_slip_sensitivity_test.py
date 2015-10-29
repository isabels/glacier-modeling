import basic_model
import tools

possibilities = [.0005, .00055, .0006, .00065, .0007, .00075, .0008, .00085, .0009, .00095, .001]
b0 = tools.load_nolan_bedrock()
obs_surface = tools.load_first_guess_surface()
for i in possibilities:
	run = basic_model.isothermalISM(58, 1000, i, b0[:])
	for n in range(5000):
		run.timestep(1)
	difference = tools.calculate_surface_difference(run.get_surface_elev(), obs_surface)
	print 'run with basal slip of ', i, 'surface difference is', difference

#result: .0075 gives lowest error