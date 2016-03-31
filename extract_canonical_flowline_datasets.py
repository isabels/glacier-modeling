import math

def load_surface():
	easting = []
	northing = []
	elevation = []
	flowline = open('canonical_flowline_surface_elevation.csv', 'r')
	for line in flowline.readlines()[1:]:
		data = line.split(',')
		easting.append(float(data[0]))
		northing.append(float(data[1]))
		elevation.append(float(data[2]))
	return (easting, northing, elevation)

def load_velocity():
	velocity = []
	flowline = open('canonical_flowline_surface_velocity.csv', 'r')
	for line in flowline.readlines()[1:]:
		data = line.split(',')
		velocity.append(float(data[0]))
	return velocity

easting, northing, elevation = load_surface()
velocity = load_velocity()
print len(easting), len(northing), len(elevation), len(velocity)

#now: convert easting, northing to dist from terminus
dist_from_terminus = []
total_dist = 0
dist_from_terminus.append(0) #1st point is 0 km from terminus
for i in range(1, len(easting)):
	total_dist += math.sqrt((easting[i] - easting[i-1])**2 + (northing[i] - northing[i-1])**2)
	dist_from_terminus.append(total_dist)

print len(dist_from_terminus)
print dist_from_terminus

#UGH current flowline stops about 4km short of where it should be :(((


#create list
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