
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
    b0 = [0, -15.391036329011465, -56.18804193716341, -56.75452402248031, -40.91559098555361, -21.030862534504006, -8.698062913195654, 21.98135584957196, 51.72708104691265, 72.5540674129723, 109.23152958362691, 104.70179203562078, 59.315070535032525, 63.11751413064514, 43.69350174215236, 38.24523980950079, 32.27630804343695, 25.694000259472944, 20.599632345828216, 30.170667651499137, 26.706100875667563, 75.57670270695047, 85.58419521764642, 106.6784810495721, 109.7513775579893, 87.85890070787003, 87.82759490095208, 81.37206117065648, 68.55315870658433, 50.44197117069722, 29.22204709543831, 7.448308648202399, -12.799815813383757, -22.963463384186298, -42.59341274921514, -48.3279275100681, -24.12160206760299, -32.44778070262141, -12.584521510422134, 9.850065880800276, 12.958598573624407, 24.81448121266737, 7.933361833020385, -25.589253492939154, -27.37754236418303, -16.698620108798412, -15.328542475558862, -16.774803190576495, -7.7284819946333485, -36.34211410302805, -47.1944532025009, -50.58893494406152, -43.78486070544924, -29.319966582800276, -13.42955227163459, -2.268578361437467, 1.515245491935436, 0]
    base = tools.load_nolan_bedrock()
    b0 = map(operator.add, b0, base)

    run1 = isothermalISM(58, 1000, 0.0015, .0005, 0.00022, b0) #55 nodes, 1000-meter spacing,  basal slip of zero
    run1.openOutput('medium.nc')

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


