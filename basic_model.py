
import math
import numpy as np
import scipy.sparse as sparse          
import scipy.sparse.linalg as linalg
import tools
import scipy.io.netcdf as ncdf
import matplotlib.pyplot as mp
import operator

class isothermalISM(object):
    p = 918 #density of ice
    g = 9.81 #gravitational constant
    glenns_a = 2.4e-24 #glenn's flow law constant, should be 2.4e-24 for temperate (0degC) ice 
    glenns_n = 3 #power of glenn's flow law
    nodes_past_divide = 20 #used to add things to mass balance
    
    def __init__(self,num_nodes,dx,bslip_1, bslip_2, bslip_3, b): #initializes the model's fields
        self.dx = dx 
        self.bslip_1 = bslip_1
        self.bslip_2 = bslip_2
        self.bslip_3 = bslip_3
        self.num_nodes = num_nodes + 20

        self.time = 0 
        self.x= np.array(range(0,((self.num_nodes)*self.dx),self.dx)) 
        self.ice_thickness= np.zeros(self.num_nodes) 
        
        self.bed_elev = b
        for i in range(1210, 410, -40):
            self.bed_elev.append(i)
        self.surface_elev= self.bed_elev #start with no ice
        self.mass_balance = tools.load_mbal('reduced_smoothed_mbal.csv')

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
        
    def timestep(self,dt): #performs one timestep, i.e. calculates a new surface elev, thickness from prev one
        D = np.zeros(self.num_nodes)
        slopes = tools.calculate_slopes(self.surface_elev, self.dx) 
        for i in range(0,self.num_nodes):
            if(i<20):
                D[i] = (((-2*self.glenns_a*(self.p*self.g)**self.glenns_n)/(self.glenns_n+2))*(self.ice_thickness[i]**(self.glenns_n+2))*(abs((slopes[i])**(self.glenns_n-1))))-(self.bslip_1*self.p*self.g*(self.ice_thickness[i]**2))
            elif(i<40):
                D[i] = (((-2*self.glenns_a*(self.p*self.g)**self.glenns_n)/(self.glenns_n+2))*(self.ice_thickness[i]**(self.glenns_n+2))*(abs((slopes[i])**(self.glenns_n-1))))-(self.bslip_2*self.p*self.g*(self.ice_thickness[i]**2))
            else:
                D[i] = (((-2*self.glenns_a*(self.p*self.g)**self.glenns_n)/(self.glenns_n+2))*(self.ice_thickness[i]**(self.glenns_n+2))*(abs((slopes[i])**(self.glenns_n-1))))-(self.bslip_3*self.p*self.g*(self.ice_thickness[i]**2))
        
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
            B[i] = (-alpha*self.surface_elev[i+1]) + ((1 + alpha + beta)*self.surface_elev[i]) - (beta*self.surface_elev[i-1]) + (self.mass_balance[i]*dt)
        
        self.surface_elev, info=linalg.bicgstab(A, B) 
        
        for i in range(self.num_nodes):
            if(self.surface_elev[i] < self.bed_elev[i]):
                self.surface_elev[i] = self.bed_elev[i]
        self.ice_thickness = self.surface_elev - self.bed_elev
        self.time += dt
        
    def calculate_velocity(self): #calculates and prints out the current SURFACE velocity at each node
        slopes = tools.calculate_slopes(self.surface_elev, self.dx) 
        velocity = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            if(i<20):
                velocity[i] = ((-(2*self.glenns_a*(self.p*-self.g)**self.glenns_n)/(self.glenns_n+1))*(self.ice_thickness[i]**(self.glenns_n+1))*(abs((slopes[i])**(self.glenns_n-1))))*(slopes[i])-(self.bslip_1*self.p*-self.g*self.ice_thickness[i]*slopes[i])

            elif(i<40):
                velocity[i] = ((-(2*self.glenns_a*(self.p*-self.g)**self.glenns_n)/(self.glenns_n+1))*(self.ice_thickness[i]**(self.glenns_n+1))*(abs((slopes[i])**(self.glenns_n-1))))*(slopes[i])-(self.bslip_2*self.p*-self.g*self.ice_thickness[i]*slopes[i])

            else:
                velocity[i] = ((-(2*self.glenns_a*(self.p*-self.g)**self.glenns_n)/(self.glenns_n+1))*(self.ice_thickness[i]**(self.glenns_n+1))*(abs((slopes[i])**(self.glenns_n-1))))*(slopes[i])-(self.bslip_3*self.p*-self.g*self.ice_thickness[i]*slopes[i])
            print 'velocity at node ', i, 'is: ', velocity[i]

    def calculate_basal_velocity(self): #this calculates the basal sliding portion of velocity to see if it's reasonable
        slopes = tools.calculate_slopes(self.surface_elev, self.dx)
        basal_velocity = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            if(i<20):
                basal_velocity[i] = -(self.bslip_1*self.p*-self.g*self.ice_thickness[i]*slopes[i]) #g should be negative??)

            elif(i<40):
                basal_velocity[i] = -(self.bslip_2*self.p*-self.g*self.ice_thickness[i]*slopes[i]) #g should be negative??)

            else:
                basal_velocity[i] = -(self.bslip_3*self.p*-self.g*self.ice_thickness[i]*slopes[i]) #g should be negative??)
            print 'basal velocity at node ', i, 'is: ', basal_velocity[i]

    def get_ice_thickness(self):
        return self.ice_thickness

    def get_surface_elev(self):
        return self.surface_elev

def main():
    b0 = [-53.86014283247338, -96.55148545680116, -209.56378728526175, -329.5285447843742, -276.1078577736731, -99.4682311472077, -74.60838257235906, 103.76931702628877, 199.59759885797695, 325.49387992076936, 294.9387516971606, 190.74077827555544, 95.99117577626988, 252.4851292030383, 410.3736616110993, 500, 500, 444.71357635367707, 326.35184433516275, 223.25791552817049, 98.55471776145947, 134.18167926051117, 30.336550811088184, -88.39136174706994, -121.36948314990242, -18.45822543176338, -66.01158355801323, 52.93628093781889, -92.66509252409524, 15.70587677548626, -22.132177754463765, 6.391541935525751, -68.42339808954196, 39.59640808291448, 53.464027842215515, 136.78502122848863, 254.14520471035019, 192.5665648106059, 65.30439277418417, 14.10079843084735, -114.02424000705798, -289.4634592194706, -303.0305745281302, -266.62019841090347, -198.4732468197231, -210.421471160374, -143.2408448139692, -66.7972463258127, -18.769521382966776, 46.9742033841991, 105.26603075720368, 164.98279637713722, -43.50064538327361, -79.11047511726842, -3.8891318593645394, 12.390579201231496, -59.56957705146683, 0]
    base = tools.load_nolan_bedrock()
    b0 = base#map(operator.add, base, b0)

    run1 = isothermalISM(58, 1000, 0.0015, .0005, 0.00022, b0) #55 nodes, 1000-meter spacing,  basal slip was .0005
    run1.openOutput('run1.nc')

    for i in range(1500): #5000 years
        run1.timestep(1)
        if(i%100==0): 
            print 'on timestep', i
            run1.write()
    run1.calculate_basal_velocity()  
    run1.calculate_velocity() 
    run1.close()
    tools.plot_model_run('run1.nc')

if __name__=='__main__':
    main()


