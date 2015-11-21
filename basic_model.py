
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
    b0 = [-121.61447444687286, -40.116840792711336, -147.6009968472764, -263.4662279677807, -113.7719998018802, -39.958074259622435, -39.62407571356214, -129.69877656161808, -168.8844440258147, -16.810225067389855, -14.74191094883721, -8.273309765866488, -34.07586424942264, -56.48096282604505, -122.58437769191582, -215.40000924720783, -197.2098080746655, -180.33039250683706, -112.18956101939638, -49.46653610709698, -47.0198226657985, -186.37226356553225, -200.55107180255217, -255.286466061683, -265.48902907230155, -280.00758191581383, -240.0992278289701, -220.66108545551242, -232.3019799793356, -156.0486162859212, -118.66938378726394, -78.66634840286723, -49.3122730596783, -31.721521841656113, -30.99932796637459, -116.51513383699165, -58.555522120170146, -7.724721379670737, -33.00559873701778, -67.29114810011949, -106.08507603157706, -144.24184310542378, -177.711885834821, -277.0472117560437, -222.29692631082423, -230.08362013890573, -234.244856972965, -202.06218358179945, -161.1489352163696, -103.84472597065773, -37.25824483576569, 27.30732876093263, 77.43251042716605, 104.20228476370323, 106.27018561655132, 91.05956471210625, 71.80784669934434, 110.55468283312794]
    base = tools.load_nolan_bedrock()
    b0 = map(operator.add, base, b0)

    run1 = isothermalISM(58, 1000, 0.0015, .0005, 0.00022, b0) #55 nodes, 1000-meter spacing,  basal slip was .0005
    run1.openOutput('run1.nc')

    for i in range(5000): #5000 years
        run1.timestep(1)
        if(i%100==0): 
            print 'on timestep', i
            run1.write()
    #run1.calculate_velocity()   
    run1.close()
    tools.plot_model_run('run1.nc')

if __name__=='__main__':
    main()


