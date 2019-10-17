# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 09:13:39 2019

@author: andre
"""

import matplotlib.pyplot as plt
import math as mth

def calcDistances(latitudeA=0,longitudeA=0,latitudeB=0,longitudeB=0,a0=0,a1=0,a2=0):
    global afta0, afta1, afta2, distance1, distance2, distance3, x, y
    afta0 = latitudeA + a0
    afta1 = longitudeA + a1
    afta2 = afta0 - a2
    distance1 = mth.sqrt((((longitudeA) - (longitudeB))**2) + (((afta0) - (latitudeB))**2))
    distance2 = mth.sqrt((((afta1) - (longitudeB))**2) + (((afta0) - (latitudeB))**2))
    distance3 = mth.sqrt((((afta1) - (longitudeB))**2) + (((afta2) - (latitudeB))**2))
    part1a = (afta1 - afta1)*((afta1**2-longitudeA**2)+(afta0**2-afta0**2)+(distance1**2-distance2**2)) 
    part2a = (longitudeA - afta1)*((afta1**2-afta1**2)+(afta2**2-afta0**2)+(distance2**2-distance3**2))
    part3a = 2*(((afta0-afta0)*(afta1-afta1))-((afta0-afta2)*(longitudeA-afta1)))
    y = -((part1a - part2a) / part3a)
    part1b = (afta0 - afta2)*((afta0**2-afta0**2)+(afta1**2-longitudeA**2)+(distance1**2-distance2**2))
    part2b = (afta0 - afta0)*((afta2**2-afta0**2)+(afta1**2-afta1**2)+(distance2**2-distance3**2))
    part3b = 2*(((longitudeA-afta1)*(afta0-afta2))-((afta1-afta1)*(afta0-afta0)))
    x = -((part1b - part2b) / part3b) 
    locationB = plt.Circle((x,y), 50, color='blue')
    ax.add_artist(locationB)

def processCoords(longitudeB=0,latitudeB=0):
    coordinatesOfX = longitudeB
    coordinatesOfY = latitudeB
    coordinateXList.append(coordinatesOfX)
    coordinateYList.append(coordinatesOfY)
 
epiScans = int(input('How many scans can be done? '))
timeInterval=float(input('Time Interval between Scans: '))
ax = plt.axes()
ax.set_aspect('equal')
fig = plt.figure()
ax.grid()
ax.set_xlim((-(1000),1000)) 
ax.set_ylim((-(1000),1000)) 
longitudeA=float(input('Your Longitude: '))
latitudeA=float(input('Your Latitude: '))
coordinateXList = []
coordinateYList = []

def getSpeed(coordinate1X, coordinate2X, coordinate3X, coordinate1Y, coordinate2Y, coordinate3Y):
    global speed1, speed2
    deltaD1 = mth.sqrt((((coordinate2X) - (coordinate1X))**2) + (((coordinate2Y) - (coordinate1Y))**2))
    deltaD2 = mth.sqrt((((coordinate3X) - (coordinate2X))**2) + (((coordinate3Y) - (coordinate2Y))**2))
    speed1 = int(deltaD1 / timeInterval)
    speed2 = int(deltaD2 / timeInterval)
    averageSpeed = ((speed2 + speed1) / 2) * timeInterval
    print('\nSpeed1: {}, Speed2: {}'.format(speed1,speed2))
    if (mth.fabs(speed2 - speed1) < 1.1):
        print('\nObject B is moving at a relatively constant speed of approximately {:.4f} units/second\n'.format(averageSpeed))

# Turns this into a function for epiScans
for i in range(0, epiScans, 1):
    longitudeB=float(input('For testing purposes, longitude of B: '))
    latitudeB=float(input('For testing purposes, latitude of B: '))
    
    # These values would be the varying coordiantes of "stationary" object A
    a0=float(input('Units Up: ')) 
    a1=float(input('Units Right: '))
    a2=float(input('Units Down: ')) 
    latitudeA = latitudeA + a0 - a2
    longitudeA = longitudeA + a1

    # This can be under a for loop to account for how unstationary objects will be
    calcDistances(latitudeA,longitudeA,latitudeB,longitudeB,a0,a1,a2)
    print('\nDistance 1 is: {} units\nDistance 2 is: {} units\nDistance 3 is: {} units\n'.format(distance1,distance2,distance3))
    print('Object B is at ({:.5f}, {:.5f})'.format(x,y))
    processCoords(x,y)
    objectA = plt.Circle((longitudeA,latitudeA), 25, color='green') 
    iteration1 = plt.Circle((longitudeA,afta0), distance1, color='purple',fill=False)
    iteration2 = plt.Circle((afta1,afta0), distance2, color='red',fill=False) 
    iteration3 = plt.Circle((afta1,(afta2)), distance3, color='orange',fill=False)
    ax.add_artist(objectA) 
    ax.add_artist(iteration1) 
    ax.add_artist(iteration2) 
    ax.add_artist(iteration3) 

coordinate1X = coordinateXList[0]
coordinate1Y = coordinateYList[0]
coordinate2X = coordinateXList[1]
coordinate2Y = coordinateYList[1]
coordinate3X = coordinateXList[2]
coordinate3Y = coordinateYList[2]
getSpeed(coordinate1X, coordinate2X, coordinate3X, coordinate1Y, coordinate2Y, coordinate3Y)

# Predicts constant motion
pIteration = 0
ptime = 0
timeMultiple = 0
deltaX1 = coordinate3X - coordinate2X
deltaY1 = coordinate3Y - coordinate2Y
newCoordX = float(coordinate3X)
newCoordY = float(coordinate3Y)
if (mth.fabs(speed2 - speed1) < 1.1):
    while pIteration < 10:
            newCoordX += deltaX1
            newCoordY += deltaY1
            plocationB = plt.Circle((newCoordX,newCoordY), 45, color='pink')
            ax.add_artist(plocationB)
            ptime = timeInterval * timeMultiple
            print('At t = {}, Object B will be at ({:.5f}, {:.5f})'.format(ptime,newCoordX,newCoordY))
            pIteration += 1
            timeMultiple += 1 
else:
    print('Cannot predict Object B\'s trajectory!')