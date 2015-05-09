#!/usr/bin/env python
import os
import math
import cairocffi as cairo
import logging
import numpy as np

index = 0
MAX_LEVEL = 10

class Coordinates(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __str__(self):
		return "(%s,%s)" % (self.x, self.y)

class FractalContextStats(object):
	def __init__(self,median,mean,stddev,dataSize,minimum,maximum):
		self.median = median
		self.mean = mean
		self.stddev = stddev
		self.dataSize = dataSize
		self.minimum = minimum
		self.maximum = maximum
	def __str__(self):
		return 'length/median/mean/stddev/min/max     %s/%s/%s/%s/%s/%s' % (self.dataSize,self.median,self.mean,self.stddev,self.minimum,self.maximum)

class FractalIteration(object):
	def __init__(self,angle,angleVar,colR,colG,colB):
		self.angle = angle
		self.angleVar = angleVar
		self.colR = colR
		self.colG = colG
		self.colB = colB

class FractalContext(object):
	def __init__(self,stats,ittr):
		self.stats = stats
		self.thisItr = ittr
		self.lastItr = ittr
	def nextIteration(self,ittr):
		self.lastItr = self.thisItr
		self.thisItr = ittr
	def getIteration(self):
		return self.thisItr
	def deltaIteration(self):
		angle = self.lastItr.angle - self.thisItr.angle
		angleVar = self.lastItr.angleVar - self.thisItr.angleVar
		colR = self.lastItr.colR - self.thisItr.colR
		colG = self.lastItr.colG - self.thisItr.colG
		colB = self.lastItr.colB - self.thisItr.colB
		return FractalIteration(angle,angleVar,colR,colG,colB)


def new(sklProcess):
	sklItem = sklProcess.sklItem
	global index

	WIDTH, HEIGHT = 5000, 5000

	fileLocation = "/app/%s-%s.png" % (sklItem.id,sklProcess.id)

	if os.path.isfile(fileLocation):
		logging.warning("Cannot generate item[%s]. %s already exists",sklItem.id,fileLocation)
	else:
		logging.info("Getting URL data for scene %s from %s",sklItem.id, sklItem.resourceURL)
		sklItem.resourceData = sklItem.GetData()

		logging.debug(type(sklItem.resourceData))

		logging.info("Creating fractal for %s:%s",sklItem.id, sklProcess.id)

		surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context (surface)

		ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

		# pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
		# pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
		# pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

		ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
		ctx.set_source_rgb (1,1,1)
		ctx.fill ()

		stats = FractalContextStats(np.median(sklItem.resourceData),np.mean(sklItem.resourceData),np.mean(sklItem.resourceData),len(sklItem.resourceData),min(sklItem.resourceData),max(sklItem.resourceData))


		logging.debug(stats)

		PI = math.pi
		index = 0

		startPoint = Coordinates(0.5,0.5) # Middle
		angleVarience = stats.dataSize % PI/1.5
		numberOfStartingPoints = stats.mean*100 % 9
		i = 0

		while i <= numberOfStartingPoints:
			frtCtx = FractalContext(stats,FractalIteration((i/numberOfStartingPoints*PI)*2-angleVarience,angleVarience,0,0,0))
			Iterate(frtCtx,ctx,1,(i/numberOfStartingPoints*PI)*2-angleVarience,startPoint,angleVarience,sklItem)
			i = i + 1


		surface.write_to_png (fileLocation) # Output to PNG

		return fileLocation

def Iterate(frtCtx,ctx,currentLevel,currentAngle,currentCoordinates,angleVarience,sklItem):
	global index
	ctx.move_to (currentCoordinates.x, currentCoordinates.y)

	bytePoint1 = ((index+1)*7)%len(sklItem.resourceData)
	bytePoint2 = ((index+1)*3)%len(sklItem.resourceData)
	bytePoint3 = ((index+1)*13)%len(sklItem.resourceData)
	byte1 = sklItem.resourceData[bytePoint1]
	byte2 = sklItem.resourceData[bytePoint2]
	byte3 = sklItem.resourceData[bytePoint3]

	length =  ((MAX_LEVEL/currentLevel * 0.02) + (100/byte1)/100) % 0.1

	newAngle = currentAngle+angleVarience

	newX = length * math.cos(newAngle) + currentCoordinates.x
	newY = length * math.sin(newAngle) + currentCoordinates.y

	newCoordinates = Coordinates(newX,newY)

	# logging.debug('Drawing line from %s to %s',currentCoordinates,newCoordinates)

	ctx.line_to (newCoordinates.x, newCoordinates.y) # Line to (x,y)

	r = frtCtx.getIteration().colR + 0.1
	g = frtCtx.getIteration().colG + 0.1
	b = frtCtx.getIteration().colB + 0.1

	ctx.set_source_rgb (r,g,b) # Solid color
	ctx.set_line_width ((MAX_LEVEL/currentLevel)/1000)
	ctx.stroke ()

	index = index + 1
	
	if currentLevel <= MAX_LEVEL:
		newContext = FractalContext(frtCtx.stats,frtCtx.getIteration())
		newContext.nextIteration(FractalIteration(newAngle,angleVarience,r,g,b))

		numberOfNewBranches = (byte1 + byte2 + byte3)/100%4
		# Start at 1 to ignore first line
		i = 1

		# First line
		Iterate(newContext,ctx,currentLevel +1,newAngle,newCoordinates,angleVarience,sklItem)

		# Lines inbetween
		while i < numberOfNewBranches - 1:
			variance = angleVarience + (angleVarience*-1 - angleVarience) * i/(numberOfNewBranches - 1)
			i = i+1
			extraVariance = variance + 100 -(byte1 + byte2 + byte3)/1000%100
			Iterate(newContext,ctx,currentLevel +1,newAngle,newCoordinates,variance,sklItem)

		# Last line
		Iterate(newContext,ctx,currentLevel +1,newAngle,newCoordinates,angleVarience*-1,sklItem)

