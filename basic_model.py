
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
        
    def calculate_velocity(self): #calculates and prints out the current velocity at each node
        slopes = tools.calculate_slopes(self.surface_elev, self.dx) 
        velocity = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            velocity[i] = ((-(2*self.glenns_a*(self.p*-9.81)**self.glenns_n)/(self.glenns_n+1))*(self.ice_thickness[i]**(self.glenns_n+1))*(abs((slopes[i])**(self.glenns_n-1))))*(slopes[i])-(self.slide_parameter*self.p*-9.81*self.ice_thickness[i]*slopes[i])
            print('velocity at node ', i, 'is: ', velocity[i])

    def get_ice_thickness(self):
        return self.ice_thickness

    def get_surface_elev(self):
        return self.surface_elev

def main():
    b0 = [0, -16.230128697218376, -54.503766387093904, -25.26953803052109, -13.872887770589509, -6.20962595867039, 82.97323312739655, 120.35371078111311, 103.4672155973308, 135.83634455092192, 102.3367639265352, 115.50652549130476, 92.01988447091989, 92.21206210218159, 68.1039819294848, 56.934184865644056, 37.913935055705025, 45.847312411301175, 49.34589345212055, 53.69120461555752, 57.6566373791093, 63.979112085511694, 98.18758152147319, 109.71914629815429, 82.21094185823465, 96.77444126703224, 68.04043249359363, 43.303581693168816, 28.859014949744537, 15.299902849463571, 2.732625377840773, 12.834282673071646, 9.992556708674913, 1.8564026174763335, 19.66466701201127, -2.255686383986809, -25.783827683950946, 9.738691855379326, 9.956969474386048, 4.174462265821802, 2.1463600655826425, -36.172165800981176, -28.848731406102118, -21.738300382738842, -18.68149551645931, -20.790203345289367, -25.1159895675725, -27.115813361126712, -23.317392747055447, -14.107838585400009, -2.9263806248091804, 5.963580682888779, 10.704901762355233, 12.052645760412597, 5.380063252247421, 9.880991881803043, -13.422675942084904, 0]
    base = tools.load_nolan_bedrock()
    b0 = map(operator.add, b0, base)

    run1 = isothermalISM(58, 1000, 0.0015, .0005, 0.00022, b0) #55 nodes, 1000-meter spacing,  basal slip of zero
    run1.openOutput('smooth.nc')

    for i in range(1500): #5000 years
        run1.timestep(1)
        if(i%100==0): 
            print 'on timestep', i
            run1.write()
    #run1.calculate_velocity()   
    run1.close()
    tools.plot_model_run('smooth.nc')

if __name__=='__main__':
    main()


