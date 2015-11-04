import basic_model
import tools
import numpy as np

possibilities1 = [ .0008, .00082, .00085, .0009, .00095, .00097, .00099, .001, .0012, .0015]
possibilities2 = [ .0005, .0006, .0007,.00072, .00075, .00077, .0008, .00082, .00085, .0009]
possibilities3 = [.0001, .0002, .00022, .00024, .00026, .00028, .0003, .0004, .0005, .00055]
results = np.zeros([1000, 4])
count = 0
b0 = tools.load_nolan_bedrock()
obs_surface = tools.load_first_guess_surface()
for i in possibilities1:
	for j in possibilities2:
		for k in possibilities3:
			run = basic_model.isothermalISM(58, 1000, i,j,k, b0[:])
			for n in range(1000):
				run.timestep(1)
			difference = tools.calculate_surface_difference(run.get_surface_elev(), obs_surface)
			results[count][0] = i
			results[count][1] = j
			results[count][2] = k
			results[count][3] = difference
			count =+ 1
			print i, j, k, difference

f = file("experiment_results.txt","wb")
np.save(f,results)
f.close()
#best for 2: .00095, .0002

#best for 3: 0.0015 0.0005 0.00022 564.84883375


