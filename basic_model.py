
import math
import numpy as np
import scipy.sparse as sparse          
import scipy.sparse.linalg as linalg
import tools
import scipy.io.netcdf as ncdf
import matplotlib.pyplot as mp
from TopoHandler import generateRanTopo 

class isothermalISM(object):
    p = 918 #density of ice
    g = 9.81 #gravitational constant
    glenns_a = 1e-18 #glenn's flow law constant, should be 1e-16
    glenns_n = 3 #power of glenn's flow law
    
    def __init__(self,num_nodes,dx,slide_parameter, fname): #initializes the model's fields
        self.dx = dx 
        self.slide_parameter = slide_parameter 
        self.num_nodes = num_nodes + 20

        self.time = 0 
        self.x= np.array(range(0,(self.num_nodes*self.dx),self.dx)) 
        self.ice_thickness= np.zeros(self.num_nodes) 
        
        infile = open ('beddata.txt', 'r')
        numbers = [float(line) for line in infile.readlines()] #topmost point is at 1250 m
        infile.close()
        self.bed_elev = numbers #+ range(1240, 1040, 10) #sloping back down on far side of divide
        for i in range(1210, 410, -40):
            self.bed_elev.append(i)
        self.surface_elev= self.bed_elev #start with no ice
        self.openOutput(fname)
        
    def openOutput(self,fname): #sets up a file to copy each timestep's data into
        self.writeCounter = 0 
        f = ncdf.netcdf_file(fname, 'w') 
        f.createDimension('x', self.num_nodes)
        f.createDimension('t', None)
        f.createVariable('surface_elev', 'float', ('t', 'x'))
        f.createVariable('bed_elev', 'float', ('t', 'x'))
        f.createVariable('time', 'float', ('t'))
        f.createVariable('x', 'float', ('x'))
        f.variables['x'][:] = self.x
        self.f = f
        self.write() #writes initial condition to file
        
    def write(self): #writes one timestep's worth of data into the file
        self.f.variables['surface_elev'][self.writeCounter, :] = self.surface_elev
        self.f.variables['bed_elev'][self.writeCounter, :] = self.bed_elev
        self.f.variables['time'][self.writeCounter] = self.time
        self.writeCounter += 1 
        
    def close(self): #closes the output file
        self.f.close()
        
    def timestep(self,dt,mass_balance): #performs one timestep, i.e. calculates a new surface elev, thickness from prev one
        D = np.zeros(self.num_nodes)
        slopes = tools.calculate_slopes(self.surface_elev, self.dx) 
        for i in range(0,self.num_nodes):
            D[i] = (((-2*self.glenns_a*(self.p*self.g)**self.glenns_n)/(self.glenns_n+2))*(self.ice_thickness[i]**(self.glenns_n+2))*(abs((slopes[i])**(self.glenns_n-1))))-(self.slide_parameter*self.p*self.g*(self.ice_thickness[i]**2))
        
        A = sparse.lil_matrix((self.num_nodes,self.num_nodes)) 
        A[0, 0] = 1 
        A[self.num_nodes-1, self.num_nodes-1] = 1 
        B = np.zeros(self.num_nodes)
        B[0] = self.bed_elev[0] 
        B[self.num_nodes-1] = self.bed_elev[self.num_nodes-1] 
        
        for i in range(1, self.num_nodes-1): 
            alpha = (dt/(4.0*self.dx**2))*(D[i] + D[i+1]) 
            beta = (dt/(4.0*self.dx**2))*(D[i-1] + D[i]) 
            A[i, i-1] = beta
            A[i, i] = 1 - alpha - beta
            A[i, i+1] = alpha
            B[i] = (-alpha*self.surface_elev[i+1]) + ((1 + alpha + beta)*self.surface_elev[i]) - (beta*self.surface_elev[i-1]) + (mass_balance*dt)
        
        self.surface_elev, info=linalg.bicgstab(A, B) 
        
        for i in range(self.num_nodes):
            if(self.surface_elev[i] < self.bed_elev[i]):
                self.surface_elev[i] = self.bed_elev[i]
        self.ice_thickness = self.surface_elev - self.bed_elev
        self.time += dt
        
    def calculate_velocity(self): #calculates and prints out the current velocity at each node
        slopes = tools.calculate_slopes(self.surface_elev, self.dx) 
        velocity = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            velocity[i] = ((-(2*self.glenns_a*(self.p*-9.81)**self.glenns_n)/(self.glenns_n+1))*(self.ice_thickness[i]**(self.glenns_n+1))*(abs((slopes[i])**(self.glenns_n-1))))*(slopes[i])-(self.slide_parameter*self.p*-9.81*self.ice_thickness[i]*slopes[i])
            print('velocity at node ', i, 'is: ', velocity[i])

            

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
    f.close()
    surf_dist = []
    surf_elev = []
    elev_data = open('surface_elevations.csv', 'r')
    for line in elev_data.readlines():
        data = line.split(',')
        surf_dist.append(float(data[0]))
        surf_elev.append(float(data[1]))
    mp.plot(surf_dist, surf_elev, 'red')
    mp.show()

run1 = isothermalISM(55, 1000, 0.00001, 'run1.nc') #55 nodes, 1000-meter spacing,  basal slip of zero
for i in range(5000): #5000 years
    run1.timestep(1,.6)
    if(i%100==0): 
        print ('on timestep', i)
        run1.write()
#run1.calculate_velocity()   
run1.close()

plot_model_run('run1.nc')


