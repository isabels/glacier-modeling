
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
    
    def __init__(self,num_nodes,dx,bslip_start, bslip_stop, b): #initializes the model's fields
        self.dx = dx 
        self.generate_bslip_array(bslip_start, bslip_stop)
        self.num_nodes = num_nodes + self.nodes_past_divide

        self.time = 0 
        self.x= np.array(range(0,((self.num_nodes)*self.dx),self.dx)) 
        self.ice_thickness= np.zeros(self.num_nodes) 
        
        self.bed_elev = b
        for i in range(1210, 410, -40):
            self.bed_elev.append(i)
        self.surface_elev= self.bed_elev #start with no ice
        self.mass_balance = tools.load_mbal(index=4)

    def generate_bslip_array(self, bslip_start, bslip_stop):
        self.bslip = []
        step = (bslip_stop-bslip_start)/57 
        val = bslip_start
        for k in range(58):
            self.bslip.append(val)
            val += step
        for i in range(self.nodes_past_divide):
            self.bslip.append(self.bslip[57-i])
            #if val stays that high then it piles up on wrong side of divide    

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
            D[i] = (((-2*self.glenns_a*(self.p*self.g)**self.glenns_n)/(self.glenns_n+2))*(self.ice_thickness[i]**(self.glenns_n+2))*(abs((slopes[i])**(self.glenns_n-1))))-(self.bslip[i]*self.p*self.g*(self.ice_thickness[i]**2))
  
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
            velocity[i] = ((-(2*self.glenns_a*(self.p*-self.g)**self.glenns_n)/(self.glenns_n+1))*(self.ice_thickness[i]**(self.glenns_n+1))*(abs((slopes[i])**(self.glenns_n-1))))*(slopes[i])-(self.bslip[i]*self.p*-self.g*self.ice_thickness[i]*slopes[i])

            print 'velocity at node ', i, 'is: ', velocity[i]
        return velocity

    def calculate_basal_velocity(self): #this calculates the basal sliding portion of velocity to see if it's reasonable
        slopes = tools.calculate_slopes(self.surface_elev, self.dx)
        basal_velocity = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            basal_velocity[i] = -(self.bslip[i]*self.p*-self.g*self.ice_thickness[i]*slopes[i]) #g should be negative??)
            print 'basal velocity at node ', i, 'is: ', basal_velocity[i]
        return basal_velocity


    def get_ice_thickness(self):
        return self.ice_thickness

    def get_surface_elev(self):
        return self.surface_elev

def main():
    base = tools.load_nolan_bedrock()
    b0 = base#map(operator.add, base, b0)


    run1 = isothermalISM(58, 1000, .001125, .000025, b0) #55 nodes, 1000-meter spacing,  basal slip was .0005
    run1.openOutput('run1.nc')

    for i in range(1500): #5000 years
        run1.timestep(1)
        if(i%100==0): 
            print 'on timestep', i
            run1.write()
    #basal = run1.calculate_basal_velocity()  
    #deformation = run1.calculate_velocity() 
    run1.close()
    tools.plot_model_run('run1.nc')

if __name__=='__main__':
    main()


