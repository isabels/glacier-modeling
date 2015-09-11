import numpy as np

def calculate_slopes(elev, dx):
	slopes = np.zeros(len(elev))
	slopes[0] = (elev[1] - elev[0]) / dx
	for i in range(1, len(elev)-1):
		slopes[i] = (elev[i+1]-elev[i-1])/(dx*2.0)
	slopes[len(elev)-1] = (elev[len(elev)-1] - elev[len(elev)-2]) / dx
	return slopes
