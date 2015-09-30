#transforms GPS elev data (plus straight-up guesswork for points below the GPS line) into height-at-each-node array

surf_dist = []
    surf_elev = []
    elev_data = open('surface_elevations.csv', 'r')
    for line in elev_data.readlines():
        data = line.split(',')
        surf_dist.append(float(data[0]))
        surf_elev.append(float(data[1]))