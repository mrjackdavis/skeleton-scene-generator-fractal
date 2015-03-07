#!/usr/bin/env python
import math
import cairocffi as cairo
import logging

def generateExample():
	print("Hello world")

	WIDTH, HEIGHT, ITERATIONS = 1000, 1000, 100

	surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
	ctx = cairo.Context (surface)

	ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

	pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
	pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
	pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

	ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
	ctx.set_source (pat)
	ctx.fill ()

	ctx.move_to (0.5, 1)

	i = 0
	while (i < ITERATIONS):
		Iterate(ctx)
		i = i + 1 
		pass

	ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
	ctx.set_line_width (0.005)
	ctx.stroke ()
	
	fileLocation = "/app/example.png";

	surface.write_to_png (fileLocation) # Output to PNG

	return fileLocation

def Iterate(ctx):
	x,y = ctx.get_current_point()

	newY = y-0.01
	newX = x

	logging.debug(x)
	logging.warning('(%s,%s) to (%s,%s)',x,y,newX,newY)

	ctx.line_to (newX, newY) # Line to (x,y)
	ctx.move_to (newX, newY)