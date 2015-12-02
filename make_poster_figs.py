import scipy.io.netcdf as ncdf
import tools
import operator
import csv

# import matplotlib
# # The important line!
# matplotlib.use('Agg')
import matplotlib.pyplot as mp

# f = ncdf.netcdf_file('smooth.nc', 'r')
# elev = f.variables['surface_elev']
# bed = f.variables['bed_elev']
# time = f.variables['time']
# x = f.variables['x']
# timesteps = 15 #suddenly mad about length of ncdf variables, what the hell
# mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
# for i in range(1, timesteps):
# 	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
# mp.plot(x[0:58], elev[15][0:58], 'blue', label='final modeled surface', lw=2)
# mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)
# bed_elev = tools.load_nolan_bedrock()
# surf_elev = tools.load_first_guess_surface()
# mp.plot(x[0:57], surf_elev, 'red', label='observed surface', lw=2)
# mp.plot(x[0:58], bed_elev, 'black', label='first guess surface')
# mp.axis([-2000, 60000, -1000, 2000])
# mp.title('Higher error value, but more realistic')
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# mp.savefig('better.png', dpi=300)

# #########and now the old model run. gonna copy and paste some code because i'm too lazy to refactor and want to be able to reproduce either figure
# mp.clf()
# f = ncdf.netcdf_file('old_model.nc', 'r')
# elev = f.variables['surface_elev']
# bed = f.variables['bed_elev']
# time = f.variables['time']
# x = f.variables['x']
# timesteps = 51 #suddenly mad about length of ncdf variables, what the hell
# mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
# for i in range(1, timesteps):
# 	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
# mp.plot(x[0:58], elev[50][0:58], 'blue', label='final modeled surface', lw=2)
# mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)

# surf_elev = tools.load_first_guess_surface()
# mp.plot(range(0, 57000, 1000), surf_elev, 'red', label='observed surface', lw=2)
# mp.axis([-2000, 60000, -1000, 2000])
# mp.title('Example model run')
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# mp.savefig('old_model.png', dpi=300)

############ current model but with jameso's random bed topo
# mp.clf()
# f = ncdf.netcdf_file('random_bed.nc', 'r')
# elev = f.variables['surface_elev']
# bed = f.variables['bed_elev']
# time = f.variables['time']
# x = f.variables['x']
# timesteps = 51 #suddenly mad about length of ncdf variables, what the hell
# mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
# for i in range(1, timesteps):
# 	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
# mp.plot(x[0:58], elev[50][0:58], 'blue', label='final modeled surface', lw=2)
# mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)

# surf_dist, surf_elev = tools.load_gps_surface()
# mp.plot(surf_dist, surf_elev, 'red', label='observed surface', lw=2)
# mp.axis([-2000, 60000, -1000, 2000])
# mp.title('Model run with randomly generated rough bed topography')
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.05))
# mp.legend(loc='lower right', fontsize='small', borderaxespad=1.5)
# mp.savefig('random_bed.png', dpi=300)

#################### showing some of the beds


def read_in_beds(filename):
	beds = []
	with open(filename, 'rU') as csvfile:
			reader = csv.reader(csvfile, dialect='excel')
			index = 0
			for row in reader:
				beds.append([float(i) for i in row[0].split(',')])
	return beds

# bed_elev = tools.load_nolan_bedrock()
# fig = mp.figure()
# ax = fig.add_subplot(1,1,1)

# x = range(0, 58000, 1000)
# ax.plot(x, bed_elev, 'black', label='first guess surface', lw=2)


# beds = read_in_beds('generation39.csv')
# b0 = beds[0]
# base = tools.load_nolan_bedrock()
# b0 = map(operator.add, b0, base)

# ax.plot(x, b0, 'green', label='beds with roughness constraint', lw=2)

# for i in range(1, 50):
# 	b0 = beds[i]
# 	base = tools.load_nolan_bedrock()
# 	b0 = map(operator.add, b0, base)

# 	ax.plot(x, b0, 'green', lw=1)

# beds2 = read_in_beds('generation1.csv')
# b0 = beds2[0]
# base = tools.load_nolan_bedrock()
# b0 = map(operator.add, b0, base)

# ax.plot(x, b0, 'red', label='beds without roughness constraint', lw=2)

# for i in range(1, 500):
# 	b0 = beds2[i]
# 	base = tools.load_nolan_bedrock()
# 	b0 = map(operator.add, b0, base)

# 	ax.plot(x, b0, 'red', lw=1)

# ax.scatter([1000,5000, 12000, 20000, 32000],[-70,-200, -500, -600, -250], label='seimsic data points')


# ax.axis([-2000, 60000, -1000, 2000])
# mp.title('Beds with lowest error')
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# fig.savefig('beds.png', dpi=300)

##### GENERATION COMPARISON
bed_elev = tools.load_nolan_bedrock()

for i in range(1,10):
	fig = mp.figure()
	ax = fig.add_subplot(1,1,1)


	fig = mp.figure()
	ax = fig.add_subplot(1,1,1)

	x = range(0, 58000, 1000)
	ax.plot(x, bed_elev, 'black', label='first guess surface', lw=2)


	beds = read_in_beds('generation%d.csv' % i)
	b0 = beds[0]
	base = tools.load_nolan_bedrock()
	b0 = map(operator.add, b0, base)


	ax.plot(x, b0, 'red', label='beds without roughness constraint', lw=2)

	for j in range(1, 500):
		b0 = beds[j]
		base = tools.load_nolan_bedrock()
		b0 = map(operator.add, b0, base)

		ax.plot(x, b0, 'red', lw=1)

	ax.scatter([1000,5000, 12000, 20000, 32000],[-70,-200, -500, -600, -250], label='seimsic data points')


	ax.axis([-2000, 60000, -1000, 2000])
	mp.title('Beds from generation %d' % i)
	mp.ylabel('Elevation (m)')
	mp.xlabel('Distance from terminus (m)')
	# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
	mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
	fig.savefig('graph_generation%d.png' % i, dpi=300)

