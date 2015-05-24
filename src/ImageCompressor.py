import os
from PIL import Image as pil

def compress(pathToImage, quality):
	head, tail = os.path.split(pathToImage)
	fileName, ext = os.path.splitext(tail)

	outfile = "%s/%s-at-quality%s%%.jpg" % (head,fileName,str(quality)) 
	#open previously generated file
	compImg = pil.open(pathToImage)
	compImg.save(outfile, "JPEG", quality=quality)

	return outfile

def compressAndScale(pathToImage, quality, newSize):
	head, tail = os.path.split(pathToImage)
	fileName, ext = os.path.splitext(tail)

	outfile = "%s/%s-%spx-at-quality%s%%.jpg" % (head,fileName,str(newSize),str(quality)) 
	size = newSize, newSize

	#open previously generated file
	compImg = pil.open(pathToImage)

	compImg.thumbnail(size, pil.ANTIALIAS)

	compImg.save(outfile, "JPEG", quality=quality)

	return outfile