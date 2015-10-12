import math
import csv
import numpy as np
import matplotlib.pyplot as mp
import scipy.io.netcdf as ncdf


def calculate_slopes(elev, dx):
	slopes = np.zeros(len(elev))
	slopes[0] = (elev[1] - elev[0]) / dx
	for i in range(1, len(elev)-1):
		slopes[i] = (elev[i+1]-elev[i-1])/(dx*2.0)
	slopes[len(elev)-1] = (elev[len(elev)-1] - elev[len(elev)-2]) / dx
	return slopes

def load_mbal():
	#includes points past divide
	f = open('TAKU_MBAL_DATA.csv', 'r')
	mbal=[]
	count = 0
	for line in f.readlines():
		count += 1
		if(count%10==0):
			data = line.split(',')
			mbal.append(float(data[1]))
	for i in range(20): #stupid hack to deal with continuation past divide
		mbal.append(7)
	return mbal

def load_bedtopo():
	f = open ('beddata.txt', 'r')
	bed = [float(line) for line in f.readlines()] #topmost point is at 1250 m 
	f.close()
	return bed

def load_gps_surface():
	surf_dist = []
	surf_elev = []
	elev_data = open('surface_elevations.csv', 'r')
	for line in elev_data.readlines():
		data = line.split(',')
		surf_dist.append(float(data[0]))
		surf_elev.append(float(data[1]))
	return (surf_dist, surf_elev)

def plot_model_run(fname): #reads and plots data from the output file
	f = ncdf.netcdf_file(fname, 'r')
	elev = f.variables['surface_elev'][:]
	bed = f.variables['bed_elev'][:]
	time = f.variables['time'][:]
	x = f.variables['x'][:]
	for i in range (len(time) - 1):
		mp.plot(x, bed[i], 'green')
		mp.plot(x, elev[i], 'blue')
	mp.plot(x, elev[len(time)-1], 'cyan')
	surf_dist, surf_elev = load_gps_surface() #will this work? apparently so!
	mp.plot(surf_dist, surf_elev, 'red')
	mp.show()

def create_gps_elevation_points():
	#transforms GPS data to dist from terminus, elev pairs
	distance = []
	elevation = []
	total_distance = 12900 #first point on profile is 12.9 km from terminus
	prev_x = 0
	prev_y = 0
	with open('GPS_elevation_data.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile, dialect='excel')
		for row in reader:
			print row
			if(prev_x != 0): #terrible hack to avoid first time through
				total_distance += math.sqrt( (float(row[1]) - prev_x)**2 + (float(row[2]) - prev_y)**2 )
			elevation.append(float(row[3]))
			distance.append(total_distance)
			prev_x = float(row[1])
			prev_y = float(row[2])
	with open('surface_elevations.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile)
		for i in range(len(elevation)):
			writer.writerow([distance[i], elevation[i]])

def create_first_guess_surface():
	#finds elevation at each node, from GPS data and rest from figure in Nolan et al 1995.
	#should eventually be replaced with DEM results
	surf_dist, surf_elev = load_gps_surface()
	#the goal is to fill in the nodes with elev values. 
	#algorithm is to find two gps points on either side of each node, then linearly interpolate
	x_distances = range(0, 55000, 1000)
	elevations = np.zeros(55)
	index = 0 #keeps track of where we are in gps data array
	for i in range(len(elevations)):
		current_dist = x_distances[i]
		if(current_dist < surf_dist[0]):
			continue #skip through the nodes before GPS survey coverage
		while(surf_dist[index] < current_dist and surf_dist[index + 1] < current_dist):
			index += 1 #get to GPS data points on either side of current node
		horz_dist = surf_dist[index + 1] - surf_dist[index]
		vert_dist = surf_elev[index + 1] - surf_elev[index]
		frac = (current_dist - surf_dist[index]) / horz_dist
		elevations[i] = surf_elev[index] + (vert_dist * frac)
	#brute force the rest of the points, woop woop
	elevations[1] = 165
	elevations[2] = 210
	elevations[3] = 230
	elevations[4] = 250
	elevations[5] = 300
	elevations[6] = 350
	elevations[7] = 400
	elevations[8] = 450
	elevations[9] = 500
	elevations[10] = 525
	elevations[11] = 550
	elevations[12] = 600
	#save to ANOTHER CSV! 
	with open('first_guess_surface.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile)
		for i in range(len(elevations)):
			writer.writerow([x_distances[i], elevations[i]])


