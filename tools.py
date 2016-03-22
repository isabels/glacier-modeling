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

def load_mbal(filename, fulldata=False):
	#includes points past divide
	mbal=[]
	count = 0

	with open(filename, 'rU') as csvfile:
		reader = csv.reader(csvfile, dialect='excel')
		for row in reader:
			if(fulldata):
				mbal.append(float(row[1]))
			elif(count%10 == 0):
				mbal.append(float(row[1]))
			count += 1
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

def load_flowline():
	easting = []
	northing = []
	flowline = open('taku_flowline.csv', 'r')
	for line in flowline.readlines():
		data = line.split(',')
		easting.append(float(data[0]))
		northing.append(float(data[1]))
	return (easting, northing)

def calculate_surface_difference(calc_surf, obs_surf):
	diff = 0
	calc_surf = calc_surf[0:57] #ugh this is so dumb but whatever
	#obs_surf = obs_surf[0:55]
	for i in range(len(calc_surf)):
		diff += (calc_surf[i] - obs_surf[i])**2
	return math.sqrt(diff)

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
	surf_elev = load_first_guess_surface()
	mp.plot(range(0, 57000, 1000), surf_elev, 'red')
	mp.plot(range(0, 58000, 1000), load_nolan_bedrock(), 'black')
	diff = calculate_surface_difference(elev[len(time)-1], surf_elev)
	mp.title(diff)
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
	x_distances = range(0, 57000, 1000)
	elevations = np.zeros(57)
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

def load_nolan_bedrock(fulldata=False): #returns 550 nodes if fulldatda true, else 55 for testing
	#loads the bedrock data file that is just seismic data + linear interpolations
	bed = []
	count = 0
	with open('nolan_1995_bed_topo.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile, dialect='excel')
		for row in reader:
			if(fulldata):
				bed.append(row[1])
			elif(count%10 == 0):
				bed.append(float(row[1]))
			count += 1
	return bed

def load_first_guess_surface():
	f = open('first_guess_surface.csv', 'r')
	observed_surface=[]
	for line in f.readlines():
		data = line.split(',')
		observed_surface.append(float(data[1]))
	f.close()
	return observed_surface

easting, northing = load_flowline()
dist = 0
for i in range(length(easting) - 1):
	dist += sqrt((easting[i+1]-easting[i])^2 + (northing[i+1]-northing[i])^2)
dist = dist / length(easting) - 1
print(dist) #this is avg distance between sequential points on flowline, in m.
	


