# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:07:36 2013

@author: nrjh
"""

import numpy as np
import random
import matplotlib.pyplot as mp


def generateRanTopo(length=1,levels=1,minz=0,maxz=1,smoother=0):
    
    levels=max(1,levels)
    length=max(1,length)
    length=length

    calcspace=np.zeros((levels,length))
    topo=np.zeros((length))
    zrange=maxz-minz
    
    for i in range(levels):
        for j in range(length):
            calcspace[i,j]=random.random()
        
    for i in range(levels):    
        print (levels-i)-1
        calcspace[i]=local_smoother1D(calcspace[i],i+smoother)
        scale=1./(2**(((levels-1)-i))) 
        print "i "+str(i)+" scale"+str(scale)
        maxval=np.amax(calcspace[i])
        minval=np.amin(calcspace[i])  
        scale=scale/(maxval-minval)
        calcspace[i]=(calcspace[i]-minval)*scale
        
        print
        print calcspace[i]
    
    
    for j in range(length):       
        topo[j]=np.sum(calcspace[0:levels,j])

    maxval=np.amax(topo)
    minval=np.amin(topo)

    if (maxval==minval):
        valrange=1.
    else:
        valrange=1./(maxval-minval)
    
    topo=(((topo-minval)*valrange)*zrange)+minz
    
    return topo
####################################################################   

def local_smoother1D(line,repeat):
    
    if (repeat<1):
        return line

    length=len(line)

    calcspace=np.zeros(length)
    
    calcspace[0]=(line[0]+line[1])/2.   
    calcspace[length-1]=(line[length-1]+line[length-2])/2. 
    
    for i in range(1,length-1):
        calcspace[i]=(line[i-1]+line[i]+line[i+1])/3.
    
    return local_smoother1D(calcspace,repeat-1)
       
    
#####################################################################
length=101
xstep=100

topox=np.arange(length)*xstep

for i in range(1):
    topoy=generateRanTopo(length,levels=4,minz=100,maxz=200,smoother=0)    

#mp.axis([0,10000,0,1000])
#mp.plot(topox,topoy)


#mp.show()

