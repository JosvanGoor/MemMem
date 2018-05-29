import cv2
import numpy as np
from tqdm import tqdm

import preprocessing as pp

def getSliceHist(image, n_slices, exp_text_width, line_array, threshold, overshoot, PSL_width, height, width):
	is_line = False
	line_tuples = []
	start_line = 0
	end_line = 0

	for x in range(0, n_slices):
		left = PSL_width*x
		right = PSL_width*(x+1)
		for y in range(0,height):
			r = range(left, right)
			sum_pixels = PSL_width - (sum(image[y][r])/255.0)
			if sum_pixels > threshold:
				line_array[y] = line_array[y]+1
	left = n_slices*PSL_width
	right = n_slices*PSL_width+overshoot
	for y in range(0,height):
		r = range(left, right)
		sum_pixels = overshoot - (sum(image[y][r])/255.0)
		if sum_pixels > threshold:
			line_array[y]=line_array[y]+1

	for count, i in enumerate(line_array):
		if i>=1 and start_line==0:
			start_line = count
		elif i>1 and start_line!=0:
			is_line = True
		elif i<=1 and is_line:
			is_line = False
			end_line = count
			if end_line-start_line>exp_text_width:
				line_tuples.append([start_line,count])
			start_line = 0
		elif i<1:
			start_line = 0

	return line_tuples


def getSeg(image, top, bot):
	# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imh = image.shape[0]
	imw = image.shape[1]
	seg = np.zeros([imh,0])
	count = 0
	for i in tqdm(range(imw)):
		if sum(image[0:imh,i])/255.0<imh:
			if count > 5:
				seg = np.pad(seg,((0,0),(0,10)),mode='constant')
				segw = seg.shape[1]
				seg[0:imh,segw-10:segw] = np.ones([imh,10])*255.0
			seg = np.pad(seg,((0,0),(0,1)),mode='constant')
			segw = seg.shape[1]
			seg[0:imh,segw-1] = image[0:imh,i]
			count = 0
		else:
			count += 1
	return seg

def saveSegments(im, line_tuples, pad, height, width, showseg):
	im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
	for j, i in enumerate(line_tuples):
		top = i[0]-pad
		bot = i[1]+pad
		segment = im[top:bot,0:width-1]
		cv2.imwrite('seg_'+str(j)+'.png',im[top:bot,0:width-1])
		seg = getSeg(segment, top, bot)
		cv2.imwrite('seg'+str(j)+('.png'),seg)
		if showseg:
			cv2.imshow('seg',seg)
			cv2.waitKey(0)

def showSegments(im, line_tuples, pad, height, width):
	im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
	for j, i in enumerate(line_tuples):
		top = i[0]-pad
		bot = i[1]+pad
		if j%2 == 0:
			cv2.rectangle(im,(10,top),(width-10,bot),(0,0,255),2)
		else:
			cv2.rectangle(im,(10,top),(width-10,bot),(255,0,0),2)
	cv2.imshow('image', pp.resize(im, 0.5))
	cv2.waitKey(0)


def segmentLine(image, exp_text_width=10, pad=10, PSL_width=128, threshold=8, showseg=0):
	#image = cv2.imread(imname)
	#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
	height = image.shape[0]
	width = image.shape[1]

	overshoot = int(width%PSL_width)
	n_slices = int(width/PSL_width)
	threshold = PSL_width/8
	line_array = [0]*height

	# saveSegments(image, line_tuples, pad, height, width, showseg)
	line_tuples = getSliceHist(image, n_slices, exp_text_width, line_array, threshold, overshoot, PSL_width, height, width)
	#showSegments(image, line_tuples, pad, height, width)
	return line_tuples
	# if showseg:


#segmentLine("../ffilled.png")