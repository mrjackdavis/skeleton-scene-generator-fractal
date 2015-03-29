#!/usr/bin/env python
import os
import math
import cairocffi as cairo
import logging

index = 0

def new(sklItem):
	global index

	WIDTH, HEIGHT, ITERATIONS = 5000, 5000, 11

	fileLocation = "/app/%s.png" % (sklItem.id)

	if os.path.isfile(fileLocation):
		logging.warning("Cannot generate item[%s]. %s already exists",sklItem.id,fileLocation)
	else:
		sklItem.resourceData = sklItem.GetData()

		surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context (surface)

		ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

		# pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
		# pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
		# pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

		ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
		ctx.set_source_rgb (0.5,0.5,0.5)
		ctx.fill ()

		index = 0
		Iterate(ctx,1,ITERATIONS,0.5, 0.5,0,sklItem)

		surface.write_to_png (fileLocation) # Output to PNG

		return fileLocation

def Iterate(ctx,currentLevel,maxLevel,x,y,xMod,sklItem):
	global index
	ctx.move_to (x, y)

	bytePoint = (index*7*3)%len(sklItem.resourceData)
	byte = sklItem.resourceData[bytePoint]

	length = ((byte/500)*((currentLevel%maxLevel)/40)*(index%byte/11)-(byte/1234))
	modD = (byte/100)
	newY = y-length
	newX = x + length*xMod

	# logging.debug('at level %s, index %s : bytePoint = %s; byte = %s; length = %s; modD = %s;',currentLevel,index,bytePoint,byte,length,modD)

	ctx.line_to (newX, newY) # Line to (x,y)

	ctx.set_source_rgb ((currentLevel/10)%1, ((index*0.0002)*currentLevel*0.3)%1, (index*0.003)%1) # Solid color
	ctx.set_line_width (((index*0.0002)*(byte*0.03)*0.3)%0.05)
	ctx.stroke ()

	index = index + 1

	if currentLevel <= maxLevel:
		Iterate(ctx,currentLevel +1,maxLevel,newX,newY,xMod+modD,sklItem)
		Iterate(ctx,currentLevel +1,maxLevel,newX,newY,xMod-modD,sklItem)