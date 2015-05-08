#!/usr/bin/env python
import os
import math
import cairocffi as cairo
import logging

index = 0
MAX_LEVEL = 2

class Coordinates(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __str__(self):
		return "(%s,%s)" % (self.x, self.y)

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

		logging.info("Creating fractal for %s:%s",sklItem.id, sklProcess.id)

		surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context (surface)

		ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

		# pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
		# pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
		# pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

		ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
		ctx.set_source_rgb (0.5,0.5,0.5)
		ctx.fill ()

		PI = math.pi
		index = 0
		startPoint = Coordinates(0.5,0.5)
		angleVarience = PI/2
		numberOfStartingPoints = 4
		i = 0

		while i <= numberOfStartingPoints:
			Iterate(ctx,1,(i/numberOfStartingPoints*PI)*2-angleVarience,startPoint,angleVarience,sklItem)
			i = i + 1


		surface.write_to_png (fileLocation) # Output to PNG

		return fileLocation

def Iterate(ctx,currentLevel,currentAngle,currentCoordinates,angleVarience,sklItem):
	global index
	ctx.move_to (currentCoordinates.x, currentCoordinates.y)

	bytePoint = (index*7*3)%len(sklItem.resourceData)
	byte = sklItem.resourceData[bytePoint]

	length =  MAX_LEVEL/currentLevel * 0.05

	newAngle = currentAngle+angleVarience

	newX = length * math.cos(newAngle) + currentCoordinates.x
	newY = length * math.sin(newAngle) + currentCoordinates.y

	newCoordinates = Coordinates(newX,newY)

	logging.debug('Drawing line from %s to %s',currentCoordinates,newCoordinates)

	ctx.line_to (newCoordinates.x, newCoordinates.y) # Line to (x,y)

	ctx.set_source_rgb ((currentLevel/10)%1, ((index*0.0002)*currentLevel*0.3)%1, (index*0.003)%1) # Solid color
	ctx.set_line_width ((MAX_LEVEL/currentLevel)/1000)
	ctx.stroke ()

	index = index + 1
	
	if currentLevel <= MAX_LEVEL:
		numberOfNewBranches = 4
		# Start at 1 to ignore first line
		i = 1

		# First line
		Iterate(ctx,currentLevel +1,newAngle,newCoordinates,angleVarience,sklItem)

		# Lines inbetween
		while i < numberOfNewBranches - 1:
			variance = angleVarience + (angleVarience*-1 - angleVarience) * i/(numberOfNewBranches - 1)
			i = i+1
			Iterate(ctx,currentLevel +1,newAngle,newCoordinates,variance,sklItem)

		# Last line
		Iterate(ctx,currentLevel +1,newAngle,newCoordinates,angleVarience*-1,sklItem)

