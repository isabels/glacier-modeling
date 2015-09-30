#transforms GPS elev data (plus straight-up guesswork for points below the GPS line) into height-at-each-node array

#currently makes surface as 55-node array. will eventually need to change/parameterize for full model

import numpy as np

#load existing GPS data (stored in dist to terminus, elev format)
surf_dist = []
surf_elev = []
elev_data = open('surface_elevations.csv', 'r')
for line in elev_data.readlines():
    data = line.split(',')
    surf_dist.append(float(data[0]))
    surf_elev.append(float(data[1]))


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
	print horz_dist, vert_dist
	frac = (current_dist - surf_dist[index]) / horz_dist
	elevations[i] = surf_elev[index] + (vert_dist * frac)

print elevations

#ok, so now have interpolated as much as possible from GPS data.
#time to brute-force guess the last 12 or so!!


