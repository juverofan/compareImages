from PIL import ImageChops
import math, operator
import os
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import functools


def rmsdiff(im1, im2):
	#print("Calculate the root-mean-square difference between two images")
	try:
		im1 = im1.convert ('RGBA')
		im2 = im2.convert ('RGBA')
		width, height = im1.size
		#print(str(width)+"x"+str(height))
		if width < height and width > 0:
			im1=im1.transpose(Image.ROTATE_90)
			#im1 = im1.resize((600,int(height*600/width)), Image.ANTIALIAS)
		
		width, height = im1.size
		if width >= height and height > 0:
			im1 = im1.resize((int(width*600/height),600), Image.ANTIALIAS)
		
		
		width, height = im2.size
		#print(str(width)+"x"+str(height))
		
		if width < height and width > 0:
			im2 = im2.transpose(Image.ROTATE_90)
		width, height = im2.size
		if width >= height and height > 0:
			im2 = im2.resize((int(width*600/height),600), Image.ANTIALIAS)
		h = ImageChops.difference(im1, im2).histogram()
		# calculate rms
		return math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))
	except IOError:
		return 1000

def rmsdiff1(im1, im2):
	#print("Calculate the root-mean-square difference between two images")
	try:
		im1 = im1.convert ('RGBA')
		im2 = im2.convert ('RGBA')
		width, height = im1.size
		#print(str(width)+"x"+str(height))
		if width < height and width > 0:
			im1=im1.transpose(Image.ROTATE_270)
			#im1 = im1.resize((600,int(height*600/width)), Image.ANTIALIAS)
		
		width, height = im1.size
		if width >= height and height > 0:
			im1 = im1.resize((int(width*600/height),600), Image.ANTIALIAS)
		
		
		width, height = im2.size
		#print(str(width)+"x"+str(height))
		
		if width < height and width > 0:
			im2 = im2.transpose(Image.ROTATE_270)
		width, height = im2.size
		if width >= height and height > 0:
			im2 = im2.resize((int(width*600/height),600), Image.ANTIALIAS)
		h = ImageChops.difference(im1, im2).histogram()
		# calculate rms
		return math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))
	except IOError:
		return 1000

import argparse

text = "=======Image Diff======="

parser = argparse.ArgumentParser(description = text)  

parser.add_argument("-f", "--filex", help="The first image file")
parser.add_argument("-c", "--compare", help="The second image file")

args = parser.parse_args()

filex = args.filex
compare = args.compare

filename = filex
if "/" in filename:
	filename = filename.split("/")[len(filename.split("/"))-1]
else:
	filename = filename


secondfname = compare
if "/" in compare:
	secondfname = secondfname.split("/")[len(secondfname.split("/"))-1]
else:
	secondfname = secondfname

if(os.path.isfile(filex) and (filename.upper().endswith(".JPG") or filename.upper().endswith(".PNG") or filename.upper().endswith(".JPEG") or filename.upper().endswith(".BMP") or filename.upper().endswith(".GIF")) ):
	if(os.path.isfile(compare) and os.stat(filex).st_size > 0 and os.stat(compare).st_size > 0):
		try:
			im1=Image.open(filex)
			im2=Image.open(compare)
			rdt = rmsdiff(im1,im2)
			rdt1 = rmsdiff1(im1,im2)
			if rdt < rdt1:
				print("image similarity rate between "+filename+" vs "+secondfname+":\n"+str(100.0-rdt)+" %")
			else:
				print("image similarity rate between "+filename+" vs "+secondfname+":\n"+str(100.0-rdt1)+" %") 
		except IOError:
			print("can not calculate image similarity rate between "+filename+" vs "+secondfname+"")
