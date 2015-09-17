# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 12:21:04 2015

@author: kiya
"""
import math
import numpy as np
import scipy.sparse as sparse          # For sparse matrix types
import scipy.sparse.linalg as linalg
import tools
import scipy.io.netcdf as ncdf
import matplotlib.pyplot as mp
from TopoHandler import generateRanTopo #fancy equation tool


class isothermalISM(object):
    
    def __init__(self,nn,dx,ga,slidepar): #ga is 'glen's a' and slidepar = slide parameter
        self.nn = nn #number of nodes
        self.dx = dx #distance between each node (100 meter increments)
        self.ga = ga # should be 1e-16
        self.slidepar = slidepar # or the sliding parameter
        self.p = 918 #density of ice, kg/m^3
        self.g = 9.81 #gravitational constant, m/s^2
        self.n = 3 #Glen's flow law power
        self.x= np.array(range(0,(self.nn*self.dx),self.dx)) #build x-dimension of 55km w/100 meter step that you can do math on
        self.bed = np.zeros(self.nn)  
        #self.bed=generateRanTopo(self.nn,levels=4,minz=0,maxz=500,smoother=0) #generates the bed topography
        #self.bed = self.bed + range(0, self.nn * 50, 50)
        self.H= np.zeros(self.nn) #ice thickness at each node
        self.time = 0 #counts time to write into netcdf
        
        
        infile = open ('beddata.txt', 'r')
        numbers = [float(line) for line in infile.readlines()]
        infile.close()
        self.bed = numbers
        #print (numbers) 
        self.elev= self.bed #surface elevation at each node
        
    def timestep(self,dt,mbal):
        self.dt = dt
        self.mbal = mbal
        
        D = np.zeros(self.nn)
        slopes = tools.calculate_slopes(self.elev, self.dx) #importing our derivative function for the slopes
        for i in range(0,self.nn):
            D[i] = (((-2*self.ga*(self.p*self.g)**self.n)/(self.n+2))*(self.H[i]**(self.n+2))*(abs((slopes[i])**(self.n-1))))-(self.slidepar*self.p*self.g*(self.H[i]**2)) #whew! gives diffusivity, D, at a given point 'i'   
        A = sparse.lil_matrix((self.nn,self.nn)) #matrix A
        A[0, 0] = 1 #first value is 1
        A[self.nn-1, self.nn-1] = 1 #last value is one

        B = np.zeros(self.nn)
        B[0] = self.bed[0] #these are the first and last terms in B 'array' 
        B[self.nn-1] = self.bed[self.nn-1]
        
        for i in range(1, self.nn-1): #calculates other values and assigns them to their places in the matrix
            alpha = (self.dt/(4*self.dx**2))*(D[i] + D[i+1]) #these calculate alpha and beta for each specific point
            beta = (self.dt/(4*self.dx**2))*(D[i-1] + D[i])
            A[i, i-1] = beta
            A[i, i] = 1 - alpha - beta
            A[i, i+1] = alpha
            B[i] = (-alpha*self.elev[i+1]) + ((1 + alpha + beta)*self.elev[i]) - (beta*self.elev[i-1]) + (self.mbal[i]*self.dt) #calculates present gamma term
        
        self.elev, info=linalg.bicgstab(A, B) #mystery room where matrices get solved.
        self.elev[self.nn-1] +=350 #what the hell does this do??
        for i in range(self.nn):
            if(self.elev[i] < self.bed[i]):
                self.elev[i] = self.bed[i]
        self.H = self.elev - self.bed
        self.time += self.dt
        
    def calculate_velocity(self):
        slopes = tools.calculate_slopes(self.elev, self.dx) #importing our derivative function for the slopes
        velocity = np.zeros(self.nn)
        for i in range(self.nn):
            velocity[i] = ((-(2*self.ga*(self.p*-9.81)**self.n)/(self.n+1))*(self.H[i]**(self.n+1))*(abs((slopes[i])**(self.n-1))))*(slopes[i])-(self.slidepar*self.p*-9.81*self.H[i]*slopes[i])
            print('velocity at node ', i, 'is: ', velocity[i])
        
    def openOutput(self,fname): #open the magic storage box
        self.writeCounter = 0 #starting a count of each time the model runs
        f = ncdf.netcdf_file(fname, 'w') #open the file to write in it, not read it
        f.createDimension('x', self.nn)
        f.createDimension('t', None)
        f.createVariable('elev', 'float', ('t', 'x'))
        f.createVariable('bed', 'float', ('t', 'x'))
        f.createVariable('time', 'float', ('t'))
        f.createVariable('x', 'float', ('x'))
        f.variables['x'][:] = self.x
        self.f = f
        
    def write(self): #putting numbers into the magic storage box
        self.f.variables['elev'][self.writeCounter, :] = self.elev
        self.f.variables['bed'][self.writeCounter, :] = self.bed
        self.f.variables['time'][self.writeCounter] = self.time
        self.writeCounter += 1 #keeps count so it doesn't overwrite
        
        
    def close(self): #close the magic box now
        self.f.close()
        
    def readPlotNetcdf(self, fname): #reading things out of the magic box
        f = ncdf.netcdf_file(fname, 'r')
        elev = f.variables['elev'][:]
        bed = f.variables['bed'][:]
        time = f.variables['time'][:]
        x = f.variables['x'][:]
        for i in range (len(time)):
            mp.plot(x, bed[i], 'green')
            mp.plot(x, elev[i], 'blue')
        mp.plot(x, elev[len(time)-1], 'cyan')

        #mp.show()
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
            


run1 = isothermalISM(55, 1000, 1e-16, .0001) #55 nodes, 1000-meter spacing, glen's A (fixed), basal slip of zero
run1.openOutput('run1.nc')
run1.write()

f = open('TAKU_MBAL_DATA.csv', 'r')
mbal=[]
count = 0
for line in f.readlines():
    count += 1
    if(count%10==0):
        data = line.split(',')
        mbal.append(float(data[1]))
        
for i in range(5000):
    run1.timestep(1,mbal)
    if(i%100==0): #modulus! when you divide i/100 and the remainder is zero, do this:
        print ('on timestep', i)
        run1.write()
f.close()
run1.calculate_velocity()   
print('made it here!')
run1.close()

run1.readPlotNetcdf('run1.nc')





