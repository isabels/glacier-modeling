#roughness constraint of 0

import matplotlib.pyplot as mp
import tools
import csv
import scipy.io.netcdf as ncdf
import operator

# f = ncdf.netcdf_file('overfit.nc', 'r')
# elev = f.variables['surface_elev']
# bed = f.variables['bed_elev']
# time = f.variables['time']
# x = f.variables['x']
# timesteps = 15 #suddenly mad about length of ncdf variables, what the hell
# print len(elev[:])
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
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# mp.savefig('overfit.png', dpi=300)

# #roughness constraint of 25
# f = ncdf.netcdf_file('medium.nc', 'r')
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
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# mp.savefig('medium_no_title.png', dpi=300)

# #roughness constraint of 50
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
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# mp.savefig('smooth_no_title.png', dpi=300)

# all from both population sizes w roughness of 25 (this is popsize of 200)
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
# #### WITHOUT

# beds2 = read_in_beds('generation14-exp4.csv')
# b0 = beds2[0]
# base = tools.load_nolan_bedrock()
# b0 = map(operator.add, b0, base)

# ax.plot(x, b0, 'red', label='population size 200', lw=2)

# for i in range(1, 200):
# 	b0 = beds2[i]
# 	base = tools.load_nolan_bedrock()
# 	b0 = map(operator.add, b0, base)
# 	ax.plot(x, b0, 'red', lw=1)


# ax.scatter([1000,5000, 12000, 20000, 32000],[-70,-200, -500, -600, -250], label='seimsic data points')


# ax.axis([-2000, 60000, -1000, 2000])
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# # mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# fig.savefig('pop_200.png', dpi=300)

# ## this is the pop 2000 one
# bed_elev = tools.load_nolan_bedrock()
# fig = mp.figure()
# ax = fig.add_subplot(1,1,1)

# x = range(0, 58000, 1000)
# ax.plot(x, bed_elev, 'black', label='first guess surface', lw=2)

# #STRICT
# beds = read_in_beds('generation14-pop2000.csv')
# b0 = beds[0]
# base = tools.load_nolan_bedrock()
# b0 = map(operator.add, b0, base)

# ax.plot(x, b0, 'green', label='population size 2000', lw=2)



# for i in range(1, 200):
# 	b0 = beds[i]
# 	base = tools.load_nolan_bedrock()
# 	b0 = map(operator.add, b0, base)

# 	ax.plot(x, b0, 'green', lw=1)


# ax.scatter([1000,5000, 12000, 20000, 32000],[-70,-200, -500, -600, -250], label='seimsic data points')


# ax.axis([-2000, 60000, -1000, 2000])
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# # mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# fig.savefig('pop_2000.png', dpi=300)

# #pop 2000, showing all
# bed_elev = tools.load_nolan_bedrock()
# fig = mp.figure()
# ax = fig.add_subplot(1,1,1)

# x = range(0, 58000, 1000)
# ax.plot(x, bed_elev, 'black', label='first guess surface', lw=2)

# #STRICT
# beds = read_in_beds('generation14-pop2000.csv')
# b0 = beds[0]
# base = tools.load_nolan_bedrock()
# b0 = map(operator.add, b0, base)

# ax.plot(x, b0, 'green', label='population size 2000', lw=2)



# for i in range(1, 2000):
# 	b0 = beds[i]
# 	base = tools.load_nolan_bedrock()
# 	b0 = map(operator.add, b0, base)

# 	ax.plot(x, b0, 'green', lw=1)


# ax.scatter([1000,5000, 12000, 20000, 32000],[-70,-200, -500, -600, -250], label='seimsic data points')


# ax.axis([-2000, 60000, -1000, 2000])
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# # mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# fig.savefig('pop_2000_all.png', dpi=300)


## now comparison between pool sizes
# bed_elev = tools.load_nolan_bedrock()
# fig = mp.figure()
# ax = fig.add_subplot(1,1,1)

# x = range(0, 58000, 1000)
# ax.plot(x, bed_elev, 'black', label='first guess surface', lw=2)
# #### WITHOUT

# beds2 = read_in_beds('generation24-pool10.csv')
# b0 = beds2[0]
# base = tools.load_nolan_bedrock()
# b0 = map(operator.add, b0, base)

# ax.plot(x, b0, 'red', label='population size 200', lw=2)

# for i in range(1, 200):
# 	b0 = beds2[i]
# 	base = tools.load_nolan_bedrock()
# 	b0 = map(operator.add, b0, base)
# 	ax.plot(x, b0, 'red', lw=1)


# ax.scatter([1000,5000, 12000, 20000, 32000],[-70,-200, -500, -600, -250], label='seimsic data points')


# ax.axis([-2000, 60000, -1000, 2000])
# mp.ylabel('Elevation (m)')
# mp.xlabel('Distance from terminus (m)')
# # mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
# # mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
# fig.savefig('pop_200_pool10.png', dpi=300)


#best pool10_gen14
f = ncdf.netcdf_file('pool10_gen14.nc', 'r')
elev = f.variables['surface_elev']
bed = f.variables['bed_elev']
time = f.variables['time']
x = f.variables['x']
timesteps = 15 #suddenly mad about length of ncdf variables, what the hell
mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
for i in range(1, timesteps):
	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
mp.plot(x[0:58], elev[15][0:58], 'blue', label='final modeled surface', lw=2)
mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)
bed_elev = tools.load_nolan_bedrock()
surf_elev = tools.load_first_guess_surface()
mp.plot(x[0:57], surf_elev, 'red', label='observed surface', lw=2)
mp.plot(x[0:58], bed_elev, 'black', label='first guess surface')
mp.axis([-2000, 60000, -1000, 2000])
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
mp.savefig('pool10_gen14.png', dpi=300)
mp.clf()

#best pool10_gen24
f = ncdf.netcdf_file('pool10_gen24.nc', 'r')
elev = f.variables['surface_elev']
bed = f.variables['bed_elev']
time = f.variables['time']
x = f.variables['x']
timesteps = 15 #suddenly mad about length of ncdf variables, what the hell
mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
for i in range(1, timesteps):
	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
mp.plot(x[0:58], elev[15][0:58], 'blue', label='final modeled surface', lw=2)
mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)
bed_elev = tools.load_nolan_bedrock()
surf_elev = tools.load_first_guess_surface()
mp.plot(x[0:57], surf_elev, 'red', label='observed surface', lw=2)
mp.plot(x[0:58], bed_elev, 'black', label='first guess surface')
mp.axis([-2000, 60000, -1000, 2000])
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
mp.savefig('pool10_gen24.png', dpi=300)

mp.clf()
#best pool25_gen14
f = ncdf.netcdf_file('pool25_gen14.nc', 'r')
elev = f.variables['surface_elev']
bed = f.variables['bed_elev']
time = f.variables['time']
x = f.variables['x']
timesteps = 15 #suddenly mad about length of ncdf variables, what the hell
mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
for i in range(1, timesteps):
	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
mp.plot(x[0:58], elev[15][0:58], 'blue', label='final modeled surface', lw=2)
mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)
bed_elev = tools.load_nolan_bedrock()
surf_elev = tools.load_first_guess_surface()
mp.plot(x[0:57], surf_elev, 'red', label='observed surface', lw=2)
mp.plot(x[0:58], bed_elev, 'black', label='first guess surface')
mp.axis([-2000, 60000, -1000, 2000])
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
mp.savefig('pool25_gen14.png', dpi=300)
