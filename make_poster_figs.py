import scipy.io.netcdf as ncdf
import matplotlib.pyplot as mp
import tools

f = ncdf.netcdf_file('run1.nc', 'r')
elev = f.variables['surface_elev']
bed = f.variables['bed_elev']
time = f.variables['time']
x = f.variables['x']
timesteps = 51 #suddenly mad about length of ncdf variables, what the hell
mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
for i in range(1, timesteps):
	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
mp.plot(x[0:58], elev[50][0:58], 'blue', label='final modeled surface', lw=2)
mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)

surf_dist, surf_elev = tools.load_gps_surface()
mp.plot(surf_dist, surf_elev, 'red', label='observed surface', lw=2)
mp.axis([-2000, 60000, -1000, 2000])
mp.title('Model run with smooth bed topography')
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.1))
mp.legend(loc='lower right', fontsize='small', borderaxespad=1.5)
mp.savefig('current_model.png', dpi=300)

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
mp.clf()
f = ncdf.netcdf_file('random_bed.nc', 'r')
elev = f.variables['surface_elev']
bed = f.variables['bed_elev']
time = f.variables['time']
x = f.variables['x']
timesteps = 51 #suddenly mad about length of ncdf variables, what the hell
mp.plot(x[0:58], elev[0][0:58], 'lightblue', label='intermediate modeled surfaces', lw=2) #hack for labeling
for i in range(1, timesteps):
	mp.plot(x[0:58], elev[i][0:58], 'lightblue', lw=2)
mp.plot(x[0:58], elev[50][0:58], 'blue', label='final modeled surface', lw=2)
mp.plot(x[0:58], bed[0][0:58], 'green', label='glacier bed', lw=2)

surf_dist, surf_elev = tools.load_gps_surface()
mp.plot(surf_dist, surf_elev, 'red', label='observed surface', lw=2)
mp.axis([-2000, 60000, -1000, 2000])
mp.title('Model run with randomly generated rough bed topography')
mp.ylabel('Elevation (m)')
mp.xlabel('Distance from terminus (m)')
mp.annotate('Matthes-\nLlewellyn\n divide', xy=(57000, 1200), xytext=(52000, 500), arrowprops=dict(facecolor='black', shrink=0.05))
mp.legend(loc='lower right', fontsize='small', borderaxespad=1.5)
mp.savefig('random_bed.png', dpi=300)