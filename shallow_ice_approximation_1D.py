# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 16:28:57 2015

@author: ethan
"""

import numpy as np #imports numpy for further use
import scipy.sparse as sparse #types needed to hold sparse matrix
import scipy.sparse.linalg as linalg #solver routines needed to calculate the answer
import tools as derivx #imports prewritten derivative script
import matplotlib.pyplot as mp
import scipy.io.netcdf as ncdf
from TopoHandler import generateRanTopo
#from newbed import generate_bed_with_forcing


class isothermalISM(object):
    def __init__ (self,nn,dx,ga,slidepar,n): 
        self.nn=nn #nn= number of nodes
        self.dx=dx #dx= total size of glacier
        self.ga=ga #ga= Glen's A
        self.slidepar=slidepar #slidepar= slide parameters
        self.n=n #n= exponent for Glen's Flow Law
        self.x=np.array(range(0,self.nn*self.dx,self.dx)) #defines the x dimension
        self.bed=generateRanTopo(self.nn,levels=4,minz=-800,maxz=800,smoother=0) #generates random bed topography
        #self.bed=generate_bed_with_forcing(self.nn,levels=4,minz=-800,maxz=800,smoother=0,maxa=100,maxb=200)
        self.elev=self.bed #surface elevation at each node
        self.H=np.zeros(self.nn) #thickness of ice at each node
        
        
    def timestep(self,dt,mbal): #defines a timestep
        self.dt=dt #variable that changes time
        self.mbal=mbal #mbal= mass balance (meters water equivalent)
        D=np.zeros(self.nn) #array for diffusivity
        slopes=derivx.calculate_slopes(self.elev,self.dx) #calls out derivative function
        for i in range(0,self.nn): #this counts diffusivity
            D[i]=((-(2*self.ga*(rho*g)**self.n)/(self.n+2))*(self.H[i]**(self.n+2))*((abs(slopes[i]))**(self.n-1)))-(self.slidepar*rho*g*(self.H[i]**2)) #calculates diffusivity of ice (used in alpha and beta statements below)
        
        A=sparse.lil_matrix((self.nn,self.nn)) #this creates our square matrix
        B=np.zeros(self.nn) #sets an array for our second set of known variables
        for i in range(1,self.nn-1): #the rest of this block of code sets the diagonal of our matrix
            self.alpha=(self.dt/(4*(self.dx)**2))*(D[i]+D[i+1]) #alpha equation
            self.beta=(self.dt/(4*(self.dx)**2))*(D[i-1]+D[i]) #beta equation
            A[i,i]=1-self.alpha-self.beta
            A[i,i-1]=self.beta
            A[i,i+1]=self.alpha
            gamma=(-self.alpha*self.elev[i+1])+((1+self.alpha+self.beta)*self.elev[i])-(self.beta*self.elev[i-1])+(self.mbal[i]*self.dt) #gamma equation
            B[i]=gamma
            
        A[0,0]=1 #sets first number of out matrix
        A[self.nn-1,self.nn-1]=1 #sets the last number of our matrix
        B[0]=self.bed[0] #sets first variable for our B array as bed elevation
        B[self.nn-1]=self.bed[self.nn-1] #sets our last variable for the B array as the previous bed elevation
            
        self.elev,info=linalg.bicgstab(A,B) #this multiplies MatrixA by ArrayB
        self.H=self.elev-self.bed
            
    def OpenOutput(self,fname):
        self.writecounter=0 #sets a writecount so that the file does not overwrite itself every time we run a new timestep
        f=ncdf.netcdf_file(fname,'w') #
        f.createDimension('x',self.nn) #creates X dimension in the netcdf file that is the length of the glacier
        f.createDimension('t',None) #creates a time dimension in the netcdf file
        f.createVariable('elev','float',('t','x')) #creates a surface elevation variable in the netcdf file
        f.createVariable('bed','float',('t','x')) #creates a bed elevation variable in the netcdf file
        f.createVariable('time','float',('t')) #creates a time variable in the netcdf file
        f.createVariable('x','float',('x')) #creates an x variable in the netcdf file
        f.variables['x'][:]=self.x #sets the netcdf file x variable to the size of the pre-defined x in the object code
        self.f=f
    
    def write(self):
        self.f.variables['elev'][self.writecounter,:]=self.elev #inputs surface elevation data from the code into the save space in the netcdf file
        self.f.variables['bed'][self.writecounter,:]=self.bed #inputs bed elevatoin data from the code into the save space in the netcdf file
        self.f.variables['time'][self.writecounter]=self.dt #inputs time data from the code into the save space in the netcdf file
        self.writecounter+=1 #implements the writecounter 
    
    def close(self): #closes the netcdf 
        self.f.close()
        
    def Read_plot_ncdf(self): #This block of code reads the newly written netcdf file from above
        f=ncdf.netcdf_file('test1.nc','r')
        elev=f.variables['elev'][:] 
        bed=f.variables['bed'][:]
        time=f.variables['time'][:]
        x=f.variables['x'][:]
        for i in range(len(time)):
                mp.plot(x,elev[i,:],'green')
                mp.plot(x,bed[i,:],'blue')
        mp.show()
        

rho=(918) #ice density (kg/m^3)
g=(9.81) #gravity constant (m/s^2)


run1=isothermalISM(31,50000,1e-16,1,3) #this block of code runs the model with the given parameters
run1.OpenOutput('test1.nc')
#run1.write()
for i in range(10000): #sets a loop of time for the timestep to run in
   run1.timestep(1,.3)
   if (i%1000)==0:
       run1.write()
run1.close()
print('made it here!')
run1.Read_plot_ncdf()

