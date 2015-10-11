#transforms GPS elev data (plus straight-up guesswork for points below the GPS line) into height-at-each-node array

#currently makes surface as 55-node array. will eventually need to change/parameterize for full model

import numpy as np
import matplotlib.pyplot as mp
import csv

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
	frac = (current_dist - surf_dist[index]) / horz_dist
	elevations[i] = surf_elev[index] + (vert_dist * frac)


#ok, so now have interpolated as much as possible from GPS data.
#time to brute-force guess the last 12 or so!!

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

#plot things to make sure they still look reasonable
# mp.plot(surf_dist, surf_elev, 'red')
# mp.plot(x_distances, elevations, 'blue')
# mp.show()

#save to ANOTHER CSV! 
with open('first_guess_surface.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(elevations)):
    	writer.writerow([x_distances[i], elevations[i]])

