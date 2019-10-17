# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:38:08 2019

@author: dandrew

TRIANGULATION ON MOVING/NON-MOVING OBJECT B
- Assumes Object B Stationary
- Assumes Object B Linear in Movement
"""

import matplotlib.pyplot as plt
import math as mth

def acquireDistances(latitudeA=0,longitudeA=0,latitudeB=0,longitudeB=0,a0=0,a1=0,a2=0):
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

def deriveSpeed(coordinate1X, coordinate1Y, coordinate2X, coordinate2Y, coordinate3X, coordinate3Y, timeInterval):
    global deltaX, deltaY, accelerating, acceleration, averageSpeed, deltaX1, deltaY1, accelerationX, accelerationY, speedX0, speedY0
    deltaX0 = coordinate2X - coordinate1X
    deltaY0 = coordinate2Y - coordinate1Y
    deltaX1 = coordinate3X - coordinate2X
    deltaY1 = coordinate3Y - coordinate2Y
    deltaD1 = mth.sqrt((((coordinate2X) - (coordinate1X))**2) + (((coordinate2Y) - (coordinate1Y))**2))
    deltaD2 = mth.sqrt((((coordinate3X) - (coordinate2X))**2) + (((coordinate3Y) - (coordinate2Y))**2))
    speed1 = int(deltaD1 / timeInterval)
    speed2 = int(deltaD2 / timeInterval)
    averageSpeed = (speed2 + speed1) / 2
    print('Speed1: {}, Speed2: {}'.format(speed1,speed2))
    if (mth.fabs(speed2 - speed1) < 1.1):
        print('Object B is moving at a relatively constant speed of {:.4f} units/second\n'.format(averageSpeed))
    else:
        accelerating = True
        speedX0 = deltaX0 / timeInterval
        speedX1 = deltaX1 / timeInterval
        speedY0 = deltaY0 / timeInterval
        speedY1 = deltaY1 / timeInterval
        accelerationX = (speedX1 - speedX0) / timeInterval
        accelerationY = (speedY1 - speedY0) / timeInterval
        acceleration = mth.sqrt((accelerationX**2) + (accelerationY**2))
        print('Object B is accelerating {} units/second^2\n'.format(acceleration))
 
accelerating = False
ax = plt.axes()
ax.set_aspect('equal')
fig = plt.figure()
ax.grid()
ax.set_xlim((-(1000),1000)) 
ax.set_ylim((-(1000),1000)) 
longitudeA=float(input('Your Longitude: '))
latitudeA=float(input('Your Latitude: '))
timeInterval=float(input('Time Interval between your Scans: '))
coordinateXList = []
coordinateYList = []
print('LongA: {}, LatA: {}'.format(longitudeA,latitudeA))
for i in range(0, 3, 1):
    longitudeB=float(input('For testing purposes, longitude of B: '))
    latitudeB=float(input('For testing purposes, latitude of B: '))
    a0=float(input('Units Up: ')) 
    a1=float(input('Units Right: '))
    a2=float(input('Units Down: ')) 
    latitudeA = latitudeA + a0 - a2
    longitudeA = longitudeA + a1

    # This can be under a for loop to account for how unstationary objects will be
    acquireDistances(latitudeA,longitudeA,latitudeB,longitudeB,a0,a1,a2)
    print('\nDistance 1 is: {} units\nDistance 2 is: {} units\nDistance 3 is: {} units\n'.format(distance1,distance2,distance3))
    print('Object B is at ({:.5f}, {:.5f})'.format(x,y))
    processCoords(x,y)
    objectA = plt.Circle((longitudeA,latitudeA), 10, color='green') 
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
deriveSpeed(coordinate1X, coordinate1Y, coordinate2X, coordinate2Y, coordinate3X, coordinate3Y, timeInterval)
newCoordX = float(coordinate3X)
newCoordY = float(coordinate3Y)
pIteration = 0
timeMultiple = 3
ptime = 0
time = 0
slopeEpi = (y - latitudeA) / (x - longitudeA)
radianEpi =(mth.atan(slopeEpi))

if accelerating:
    # Works now, but only when it starts acceleratin at t=0
    print('Predictions assume object started accelerating when you started to scan.\nNote that object will keep accelerating, never reaching terminal velocity')
    while pIteration < 100:
        newcalculatedPositionX = (((time**2)*(accelerationX))/2) + coordinate1X
        newcalculatedPositionY = (((time**2)*(accelerationY))/2) + coordinate1Y 
        plocationB = plt.Circle((newcalculatedPositionX,newcalculatedPositionY), 45, color='pink')
        ax.add_artist(plocationB)
        print('At t = {}, Object B will be at ({:.5f}, {:.5f})'.format(time,newcalculatedPositionX,newcalculatedPositionY))
        pIteration += 1
        time += 1 
        
else:
    while pIteration < 10:
        newCoordX += deltaX1
        newCoordY += deltaY1
        plocationB = plt.Circle((newCoordX,newCoordY), 45, color='pink')
        ax.add_artist(plocationB)
        ptime = timeInterval * timeMultiple
        print('At t = {}, Object B will be at ({:.5f}, {:.5f})'.format(ptime,newCoordX,newCoordY))
        pIteration += 1
        timeMultiple += 1 