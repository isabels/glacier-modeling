#creates csv with (distance from terminus, elevation) pairs, to load into other code and display
import math
import csv
  #surf_dist = []
        #surf_elev = []
        #elev_data = open('surface_elevations.csv', 'r')
        #for line in elev_data.readlines():
            #data = line.split(',')
            #surf_dist.append(float(data[0]))
            #surf_elev.append(float(data[1]))
        #mp.plot(surf_dist, surf_elev, 'red')


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

print elevation
print distance

with open('surface_elevations.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(elevation)):
    	writer.writerow([distance[i], elevation[i]])
    

