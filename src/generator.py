#!/usr/bin/env python
import math
import cairocffi as cairo
import logging

def generateExample():
	print("Hello world")

	WIDTH, HEIGHT, ITERATIONS = 1000, 1000, 15

	surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
	ctx = cairo.Context (surface)

	ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

	pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
	pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
	pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

	ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
	ctx.set_source (pat)
	ctx.fill ()

	Iterate(ctx,1,ITERATIONS,0.5, 1,0)

	ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
	ctx.set_line_width (0.0005)
	ctx.stroke ()
	
	fileLocation = "/app/example.png";

	surface.write_to_png (fileLocation) # Output to PNG

	return fileLocation

def Iterate(ctx,current,max,x,y,xMod):
	ctx.move_to (x, y)

	length = 0.06
	modD = 0.15
	newY = y-length
	newX = x + length*xMod

	logging.debug(x)
	logging.warning('(%s,%s) to (%s,%s) at %s',x,y,newX,newY,current)

	ctx.line_to (newX, newY) # Line to (x,y)

	if current <= max:
		Iterate(ctx,current +1,max,newX,newY,xMod+modD)
		Iterate(ctx,current +1,max,newX,newY,xMod-modD)