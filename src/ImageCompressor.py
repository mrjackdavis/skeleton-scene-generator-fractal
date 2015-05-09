import os
from PIL import Image as pil

def compress(pathToImage, quality):
	head, tail = os.path.split(pathToImage)
	fileName, ext = os.path.splitext(tail)

	outfile = "%s/%s-at-quality%s%%.jpg" % (head,fileName,str(quality)) 
	#open previously generated file
	compImg = pil.open(pathToImage)
	#compress file at 50% of previous quality
	compImg.save(outfile, "JPEG", quality=quality)

	return outfile