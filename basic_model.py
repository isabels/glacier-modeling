
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
        self.mass_balance = tools.load_mbal(index=1)

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
    b0 = [0, -13.194332328814218, -38.903067546716585, -19.111669814095183, -11.523724411792534, -2.7157657368243817, 3.0654535680810455, 5.541899945147013, 8.074537134498327, 14.691381701086039, 55.338505328767766, 65.52415081425687, 88.88515245099936, 45.280135091360485, 37.163025349885345, 26.361002751980806, 17.616091160492946, 29.348995608129385, 38.9413333262409, 44.78731832741025, 11.605980665942283, 28.21103025317989, 51.81342499777949, 37.476068154499266, 18.99850594316948, 17.725242258076502, 20.609524442033948, 25.053646628849265, 26.714288344848615, 21.87001435049618, 12.57339344230794, 3.3076845928217584, -19.26594588387887, -1.0156469216603992, 1.7529976901298727, 26.92111025510949, 8.940834847755982, 13.744398671050769, 17.929802077333985, 19.914593812027384, 19.53749203059903, 19.69151935431371, -14.493433958963456, -15.519269707349096, -15.728166465811602, -14.334070514278444, -11.664608571214636, -6.802917490863337, -9.25796232097619, -10.688265799775003, -11.761064825878222, -10.563929341411434, -9.419119944183599, -10.293001180504737, -13.916979418452671, -15.241310272460622, -10.555407224120376, 0]
    base = tools.load_nolan_bedrock()
    b0 = map(operator.add, b0, base)

    run1 = isothermalISM(58, 1000, 1e-16, 1e-16, b0)#.001125, .000025, b0) #55 nodes, 1000-meter spacing,  basal slip was .0005
    run1.openOutput('pool10_gen14.nc')

    for i in range(5000): #5000 years
        run1.timestep(31536000)#1 yr in seconds??
        if(i%100==0): 
            print 'on timestep', i
            run1.write()
    #basal = run1.calculate_basal_velocity()  
    #deformation = run1.calculate_velocity() 
    run1.close()
    tools.plot_model_run('pool10_gen14.nc')


if __name__=='__main__':
    main()


