import scipy.io.netcdf as ncdf
import tools
import operator
import csv

# import matplotlib
# # The important line!
# matplotlib.use('Agg')
import matplotlib.pyplot as mp

f = ncdf.netcdf_file('v2_no_penalty.nc', 'r')
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
mp.plot(x[0:58], bed_elev, 'black', label='original bed')
mp.axis([-2000, 60000, -1000, 2050])
mp.title('No roughness penalty')
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
mp.savefig('v2_no_penalty.png', dpi=300)

mp.clf()
f = ncdf.netcdf_file('v2_penalty_50.nc', 'r')
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
mp.plot(x[0:58], bed_elev, 'black', label='original bed')
mp.axis([-2000, 60000, -1000, 2050])
mp.title('High roughness penalty')
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
mp.savefig('v2_penalty_50.png', dpi=300)

mp.clf()
f = ncdf.netcdf_file('v2_penalty_25.nc', 'r')
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
mp.plot(x[0:58], bed_elev, 'black', label='original bed')
mp.axis([-2000, 60000, -1000, 2050])
mp.title('Medium roughness penalty')
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
mp.savefig('v2_penalty_25.png', dpi=300)

mp.clf()
f = ncdf.netcdf_file('v2_penalty_15.nc', 'r')
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
mp.plot(x[0:58], bed_elev, 'black', label='original bed')
mp.axis([-2000, 60000, -1000, 2050])
mp.title('Small roughness penalty')
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
# mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='upper left', fontsize='small', borderaxespad=1.5)
mp.savefig('v2_penalty_15.png', dpi=300)