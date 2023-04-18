
print("Loading Packages")
#Put all 10x images that you want counted into a single folder 
#All images in the folder need to have the same number and order of stained Vischannels
import cv2 as cv
import sys

import numpy as np
import matplotlib

import matplotlib.path as mpltPath

matplotlib.use("TkAgg")
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
import math
import os, errno
from pathlib import Path
import shutil

# to enable VSI file support
#import javabridge
#import bioformats
from PIL import Image 
import PIL 
import imageio
import pandas as pd
import random
from scipy.stats import gaussian_kde
from scipy import stats
from keras.models import load_model
import csv
import tkinter as tk
import ctypes

#matplotlib.use('Agg')
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
screensize = [width, height]	

from settings import Settings
import tifffile as tiff
from io import BytesIO

settings = Settings()

#import os, psutil
#process = psutil.Process(os.getpid())


def openVSI(fullpath):
    images = bioformats.load_image(fullpath, rescale=False)
    images = cv.split(images)

    return images

def imageThreshold(img,threshmethod):

    """IMAGE THRESHOLDING."""
    # based on - https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html

    #img = cv.medianBlur(img,5)
    img_blur = cv.GaussianBlur(img,(5,5),0)

    ret,th1 = cv.threshold(img_blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    th2 = cv.adaptiveThreshold(img_blur,255,cv.ADAPTIVE_THRESH_MEAN_C,
        cv.THRESH_BINARY,11,2)
    th3 = cv.adaptiveThreshold(img_blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY,11,2)
    titles = ['Original Image (Blur)', 'Global Otsu Thresholding',
        'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img_blur, th1, th2, th3]

    if debug or debugThreshold:
        showImages(images, titles)

    return cv.bitwise_not(images[threshmethod])

def proccessVisualImage(img):
    """Function to proccess a flourescence image with nuclear localized signal (e.g. DAPI)."""
    # normalize (stretch histogram and convert to 8-bit)

    img = cv.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    img = np.uint8(img)
    # invert image 
    # FUTURE: consider other normalization strategies
    
    #img = cv.bitwise_not(img)
    return img

def showImages(images, titles='', save = 0, path = ' ', text_coords = []):
	"""For debugging, show images and titles so that they ahare the same axis (zoom together)"""
	# mng = plt.get_current_fig_manager()
	# mng.full_screen_toggle()

	# doesn't show both only most recent...
	#plt.suptitle(suptitle)
	# 
	cols = int(len(images) // 2 + len(images) % 2)
	rows = int(len(images) // cols + len(images) % cols)
	#plt.figure(figsize = (rows,cols))
	# print("cells/rows",cols,rows)
	fig, axes = plt.subplots(rows,cols, sharex=True, sharey=True, figsize=(10,10))
	# for i in range(len(images)):
	for i, ax in enumerate(axes.flat):
		if i < len(images):
			img = images[i]
			# img = self.gammaCorrect(img)
			#img = cv.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
			ax.imshow(img,'gray')
			if titles != '':
				ax.set_title(titles[i])
			# plt.xticks([]),plt.yticks([])
			else:
				fig.delaxes(ax)
		if not len(text_coords) == 0:
			for i in range(len(text_coords)):
				if i > 0:
					x = text_coords[i][0]
					y = text_coords[i][1]
					s = str(i)
					plt.text(x, y, s, fontsize=12)
	plt.tight_layout()
	plt.suptitle("press 'Q' to move to next step", verticalalignment="bottom")


	if save == 0:
		plt.show()
	else:
		plt.savefig(path, bbox_inches='tight')
	plt.close("all")

def cellshowImages(images, titles='', save = 0, path = ' ', text_coords = []):
	"""For debugging, show images and titles so that they ahare the same axis (zoom together)"""
	# mng = plt.get_current_fig_manager()
	# mng.full_screen_toggle()

	# doesn't show both only most recent...
	#plt.suptitle(suptitle)
	# 
	cols = int(len(images) // 2 + len(images) % 2)
	rows = int(len(images) // cols + len(images) % cols)
	#plt.figure(figsize = (rows,cols))
	# print("cells/rows",cols,rows)
	fig, axes = plt.subplots(rows,cols, sharex=True, sharey=True, figsize=(10,10))
	# for i in range(len(images)):
	for i, ax in enumerate(axes.flat):
		if i < len(images):
			img = images[i]
			# img = self.gammaCorrect(img)
			#img = cv.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
			ax.imshow(img,'gray', vmin=0, vmax=255)
			if titles != '':
				ax.set_title(titles[i])
			# plt.xticks([]),plt.yticks([])
			else:
				fig.delaxes(ax)
		if not len(text_coords) == 0:
			for i in range(len(text_coords)):
				if i > 0:
					x = text_coords[i][0]
					y = text_coords[i][1]
					s = str(i)
					plt.text(x, y, s, fontsize=12)
	plt.tight_layout()
	plt.suptitle("press 'Q' to move to next step", verticalalignment="bottom")


	if save == 0:
		plt.show()
	else:
		plt.savefig(path, bbox_inches='tight')
	plt.close("all")


def thresholdSegmentation( 
    thresh, 
    img, 
    opening_kernel = np.ones((1,1),np.uint8),
    opening_iterations = 2, 
    background_kernel = np.ones((3,3),np.uint8),
    background_iterations = 1,
    ):
    """SEGMENTATION and WATERSHED"""
    # based on - https://docs.opencv.org/3.4/d3/db4/tutorial_py_watershed.html
    # 1. noise removal
    # kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, opening_kernel, iterations= opening_iterations)

    # 2. sure background area
    sure_bg = cv.dilate(opening, background_kernel, iterations= background_iterations)

    # 3. Finding sure foreground area
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5) # calculates distance from boundary
    
    dt = dist_transform[dist_transform != 0] #remove zeros
    
    if debug:
        print(f"Max distance: {dist_transform.max()}")
        print(f"Median distance: {np.median(dt)}")

    ret, sure_fg = cv.threshold(dist_transform, np.median(dt), 255, 0) # use median distance (assume most cells are singlets)

    # 4. Finding unknown region
    sure_fg = np.uint8(sure_fg) 
    unknown = cv.subtract(sure_bg,sure_fg)

    # 5. Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    markers = cv.watershed(img,markers)

    img[markers == -1] = [255,0,0]

    titles = ['threshold', 'opening', 'dist_transform', 'sure_fg', 'unknown', 'watershed']
    images = [thresh, opening, dist_transform, sure_fg, unknown, img]
    NucleiBoarder = img
    
    if debugThreshold or debug:
        showImages(images, titles)

    count = markers.max()-1
    output = cv.connectedComponentsWithStats(sure_fg)

    return([count, output, sure_fg, img, markers])
# other functions of potential interest - findContours
# NEXT FILTER ON SIZE, CIRCULARITY - GET X-Y centroid
# https://www.learnopencv.com/blob-detection-using-opencv-python-c/ - for circularity

def showCentroids(images, df, titles='', save = 0, path = ' ', text_coords = []):
	"""Show centroids side-by-side with image."""

	celltypes = cell_types_to_analyze
	
	cols = int(len(images) // 2 + len(images) % 2)
	rows = int(len(images) // cols + len(images) % cols)
	#plt.figure(figsize = (rows,cols))
	# print("cells/rows",cols,rows)
	fig, axes = plt.subplots(rows,cols, sharex=True, sharey=True, figsize=(10,10))
	# for i in range(len(images)):
	for i, ax in enumerate(axes.flat):
		if i < len(images):
			img = images[i]
			# img = self.gammaCorrect(img)
			#img = cv.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
			ax.imshow(img,'gray')
			colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
			
			dotsize = 5
			for j in range(len(celltypes)):
				celltype = celltypes[j]
				color = colors[j]
				celltypedf = df.loc[df[celltype] == 1]
				centroids_x = celltypedf['X']
				centroids_y = celltypedf['Y']
				ax.scatter(centroids_x,centroids_y, s=dotsize,c=color)
				ax.legend(celltypes, loc="lower left")
				dotsize = dotsize*0.75
			if titles != '':
				ax.set_title(titles[i])
			# plt.xticks([]),plt.yticks([])
			else:
				fig.delaxes(ax)
		if not len(text_coords) == 0:
			for i in range(len(text_coords)):
				if i > 0:
					x = text_coords[i][0]
					y = text_coords[i][1]
					s = str(i)
					plt.text(x, y, s, fontsize=12)
	plt.tight_layout()
	plt.suptitle("press 'Q' to move to next step", verticalalignment="bottom")
	if debugCellLocations:
		plt.show()
	plt.close('all')




def getCells(oriImg, visoriImg, centroids, markers):
	"""Returns the image of each cell, and builds cells as a dictionary"""
	for i in range(len(centroids)):
	#print(type(channels))
	#for i in range(100):
		cellimg = []
		X = centroids[i][0]
		Y = centroids[i][1]
		#print(X,Y)
		shape = oriImg[Nuclei_Identification_Channel].shape
		width = shape[1]
		height = shape[0]

		x_min = math.ceil((X - cropsize/2).astype(int))
		x_max = math.ceil((X + cropsize/2).astype(int))
		y_min = math.ceil((Y - cropsize/2).astype(int))
		y_max = math.ceil((Y + cropsize/2).astype(int))

		if x_min < 0 or x_max > width or y_min < 0 or y_max > height:
			cellimg.append(np.zeros((len(namChannels),cropsize,cropsize), np.uint8))
			cellimg.append(np.zeros((len(namChannels),cropsize,cropsize), np.uint8))
			skipped = "Yes"
		else:
			#shallow copy of cells
			cellimg.append(oriImg[:,y_min:y_max,x_min:x_max])
			cellimg.append(visoriImg[:,y_min:y_max,x_min:x_max])
			cellMarkers = markers[y_min:y_max,x_min:x_max]
			skipped = "No"


		
		filename = 'Cell ID ' + str(i) + '.tif'
		savepa = os.path.join(SampleCellsFolder,filename)
		
		#Uncomment this to save ALL cell images
		#imageio.mimwrite(savepa,cellimg)


		cell =  {
				'oriImgName' : oriImgName,
				'CellID' :  str(i),
				'centroids' : centroids[i], 
				'cellimg' : cellimg,
				'cellMarkers': cellMarkers, 
				'skipped' : skipped
				}

		#print("include")
		cells.append(cell)

	return cells

def adjust_visual(array, set_points):
	"""
	average_val = np.average(array)
	bitSP = 255 * set_point
	dif = bitSP - average_val
	if dif > 0:
		array_adj = array + dif
	elif dif < 0:
		array_adj = array - dif
	elif dif == 0:
		array_adj = array
	"""
	array_adj = np.copy(array)
	rmax = np.quantile(array_adj, set_points[1]) + (np.quantile(array_adj, set_points[1])*0.1)
	rmin = np.quantile(array_adj, set_points[0]) - (np.quantile(array_adj, set_points[0])*0.1)
	#rmax = math.floor(np.max(array) - (np.max(array)*set_points[1]))
	#rmin = math.floor(np.min(array) + (np.min(array)*set_points[0]))
	array_adj = np.where(array > rmax, rmax, array)
	array_adj = np.where(array < rmin, rmin, array)
	tmax = 255
	tmin = 0

	array_adj = ((array_adj - rmin) / (rmax - rmin)) * (tmax-tmin) + tmin

	return array_adj


def gammaCorrect(image, gamma: float=-1):
	"""Gamma correct."""
	if gamma == -1:
		return image
	max_pixel = np.max(image)
	corrected_image = image
	corrected_image = (corrected_image / max_pixel) 
	corrected_image = np.power(corrected_image, gamma)
	corrected_image = corrected_image * max_pixel
	return corrected_image

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv.LUT(image, table)

def RandomSampler(cells, NumberWant, path):
	#Save a specified number of random cells to servay code
	randomlist = random.sample(range(len(cells)), NumberWant)
	if len(cells) < NumberWant:
		NumberWant = 0.1*cells.size
	for randcellID in randomlist:
		filename = cells[randcellID]['CellID'] + '.tif'
		savepa = os.path.join(path,filename)
		cellimg = cells[randcellID]['cellimg']
		tiff.imsave(savepa, cellimg)

def AddStats(oriImg, cells, labels, centroids, AreaStats, IntensityStats, modeStats):
	#isolate the pixels of the nuclei and bakground regions using masking, the report area and intensity data for each channel
	
	AreaStatsPix = AreaStats[:,4]
	AreaStatsmm2 = []
	#print(AreaStatsPix)
	np.array(AreaStats)
	for area in AreaStatsPix:
		AreaStatsmm2.append((area/(scale**2))/1000000)
	#print(AreaStatsmm2)

	for cell in cells:
		skipped = cell['skipped']
		#16 bit cellimg
		img = cell['cellimg'][0]

		if skipped == "No":
			stats = {}
			for i in range(len(img)):
				channel = img[i]
				marker = np.uint8(cell['cellMarkers'])
				centVal = marker[round(cropsize/2),round(cropsize/2)]
				centroid_x = cell['centroids'][0]
				centroid_y = cell['centroids'][1]

				marker[marker == 1] = 0
				marker[marker == 255] = 0
				
				#centMarker[centMarker == 1] = 0
				#centMarker[centMarker == -1] = 0
				centMarker = np.copy(marker)
				centMarker[centMarker != centVal] = 0
				centMarker[centMarker > 0] = 1
				kernel = np.ones((3,3), np.uint8)
				centMarker = cv.dilate(centMarker, kernel, iterations=1)
				centArea = np.sum(centMarker)
				#print(centArea)

				markerAll = np.copy(marker)
				markerAll[markerAll > 0] = 1
				markerAll = cv.dilate(markerAll, kernel, iterations=1)
				allArea = np.sum(markerAll)
				#print(allArea)

				otherMarker = np.copy(marker)
				otherMarker[otherMarker == centVal] = 0
				otherMarker[otherMarker > 0] = 1
				otherMarker = cv.dilate(otherMarker, kernel, iterations=1)
				otherArea = np.sum(otherMarker)
				#print(otherArea)

				invertMask = 1 - markerAll
				backgroundArea = np.sum(invertMask)
				#print(backgroundArea)

				nucleiCent = cv.bitwise_and(channel, channel, mask=centMarker)
				centIntensity = np.sum(nucleiCent)

				nucleiAll = cv.bitwise_and(channel, channel, mask=markerAll)
				allIntensity = np.sum(nucleiAll)

				background = cv.bitwise_and(channel, channel, mask=invertMask)
				backgroundIntensity = np.sum(background)

				nucleiOther = cv.bitwise_and(channel, channel, mask=otherMarker)
				otherIntensity = np.sum(nucleiOther)

				
				"""ADD IN STATS ABOUT THE CELL, LIKE AREA IN PIXELS AND INTENSITY, CHECK INTENSITY AND MAKE SURE IT IS ORIGINAL, AND THEN AMMEND cells WITH APPROPRIATE DATA"""
				stats[namChannels[i]] = [[centIntensity,centArea], [allIntensity,allArea], [ otherIntensity,otherArea], [ backgroundIntensity,backgroundArea]]
				
				if debugMasking or debug:
					images = [channel, nucleiCent, nucleiAll, nucleiOther ,background]
					Titles = ["Original","Center nuclei", "All nuclei", "Other nuclei", "Background"]
					showImages(images,Titles)

				#add in cell location and overall lesion information
				label = labels[int(centroid_y), int(centroid_x)]
				location = {
							'location_int' : label, 
							'Areas_info' : AreaStatsmm2,
							'Areas_infoPix' : AreaStatsPix,
							'ROIintensities': IntensityStats,
							'ROImodes': modeStats,
							}

		cell['stats'] = stats
		cell['location'] = location

	return cells

def MacLearnImgPrepper(cells):
	#Takes the cell image and makes an RGB with blue being dapi and green and red being one of the channels
	for cell in cells:
		skipped = cell['skipped']
		if skipped == "No":
			#raw
			#[
			img = np.copy(cell['cellimg'][1])

			#img = (img/256).astype('uint8')
			
			DAPI_ch = img[Nuclei_Identification_Channel]
			RGBs = {}
		
			for i in range(len(namChannels)):
				ch = namChannels[i]
				
				if i > 0 :
					if str(ch) == 'CC1' or str(ch) == 'PLP':
						blue = DAPI_ch
						#green = np.uint8(gammaCorrect(img[i],gamma = gammas[i]))
						green = img[i]
						#to correct for gradients in staining intensity, make the max pixel in every cell image 127 (half max intensity of 8 bit image)
						#green = cv.normalize(src=green, dst=None, alpha=0, beta=127, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
						red = img[-1]
						#red = cv.normalize(src=red, dst=None, alpha=0, beta=127, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)

					else:
						blue = DAPI_ch
						green = img[i]
						red = img[i]
						
					chrgb = cv.merge([blue, green, red])
					
					if debugImgPrepper or debug:
						cellshowImages([blue, green, red],['1','2','3'])

					RGBs[namChannels[i]] = [chrgb]

		cell['RGBs'] = RGBs

	return cells

def Reorder(UserROIs,output,IntensityStats):
	(numLabels, labelsUserROI, stats, centroids) = output
	reorderstats = [stats[0]] * numLabels
	reordercentroids = [centroids[0]] * numLabels
	reorderIntensityStats = [IntensityStats[0]] * numLabels
	for i in range(numLabels+1):
		if i > 0:
			ix = int(math.floor(centroids[i][0]))
			iy = int(math.floor(centroids[i][1]))
			for j in range(numLabels+1):
				if j > 0:
					jx = int(math.floor(centroids[j][0]))
					jy = int(math.floor(centroids[j][1]))
					if UserROIs[iy,ix] == labelsUserROI[jy,jx]:
						val = int(UserROIs[iy,ix])
						reorderstats[val] = stats[i]
						reordercentroids[val] = centroids[i]
						reorderIntensityStats[val] = IntensityStats[i]
	reordercentroids = np.array(reordercentroids)
	reorderstats = np.array(reorderstats)
	reorderIntensityStats = np.array(reorderIntensityStats)

	output2 = numLabels, labelsUserROI, reorderstats, reordercentroids, reorderIntensityStats

	return output2

def LesionFigSave(DAPIImg, UserROIs, screensize):
	img = cv.bitwise_not(np.copy(DAPIImg, subok = True)) 
	imgheight, imgwidth = img.shape[0:2]

	smallwidth = int(screensize[0] * 0.8)
	smallheight = int(smallwidth*(imgheight/imgwidth))
	
	#print(smallheight)
	if smallheight > screensize[1]:
		smallheight = int(screensize[1] * 0.8)
		smallwidth = int(smallheight*(imgwidth/imgheight))
		
	boarders = img

	labelsT = np.zeros((imgheight,imgwidth), dtype= np.uint8)

	numLabelsT = 0
	statsT = []
	centroidsT = []
	IntensityStatsT = []
	modeStatsT = []

	for i in range(len(UserROIs)):
		bincanvas = np.zeros((imgheight,imgwidth), dtype= np.uint8)
		polygon = UserROIs[i]
		polygon = np.array([polygon])
		fill = i+1
		cv.fillPoly(bincanvas, polygon, fill)
		
		labelsT = np.where(labelsT == 0, bincanvas, labelsT)
		bincanvas = cv.resize(bincanvas, (imgwidth, imgheight))
		
		ret, thresh1 = cv.threshold(bincanvas, 0, 255, cv.THRESH_BINARY)
		"""
		print(np.max(thresh1))
		img = np.copy(thresh1)
		scale_percent = 20 # percent of original size
		width = int(img.shape[1] * scale_percent / 100)
		height = int(img.shape[0] * scale_percent / 100)
		dim = (width, height)
		  
		# resize image
		resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
		cv.imshow('winname', resized)
		cv.waitKey(0)
		cv.destroyWindow('winname')
		thresh1 = np.uint8(thresh1)
		"""
		#print('DAPIImg',DAPIImg.shape)
		#print('boarders',boarders.shape)
		#print('polygon',polygon)

		cv.polylines(boarders, np.array([polygon]), True, (255, 255, 255), 5)
		#print(Lbinarr.shape)

		#cv.imshow('boarders', boarders)
		#cv.waitKey(0)
		
	
		output = cv.connectedComponentsWithStats(thresh1)
		centroids = []
		(numLabels, labels, stats, centroids) = output
		#print('centroids '+ str(centroids))

		IntensityStats, modeStats = GeneralROIIntensity(oriImg, labels, centroids)

		
		if i == 0:
			statsT.append(stats[0])
			centroidsT.append(centroids[0])
			IntensityStatsT.append(IntensityStats[0])
			modeStatsT.append(modeStats[0])

		numLabelsT = numLabelsT + 1
		statsT = np.append(statsT,[stats[1]],axis= 0)
		centroidsT = np.append(centroidsT,[centroids[1]],axis= 0)
		IntensityStatsT.append(IntensityStats[1])
		modeStatsT.append(modeStats[1])

	labelsT = cv.resize(labelsT, (imgwidth, imgheight))
	boarders = cv.resize(boarders, (imgwidth, imgheight))

	ret, threshAll = cv.threshold(labelsT, 0, 255, cv.THRESH_BINARY)
	threshAll = np.uint8(threshAll)
	outputBKG = cv.connectedComponentsWithStats(threshAll)
	(numLabelsBKG, labelsBKG, statsBKG, centroidsBKG) = outputBKG
	IntensityStatsBKG , modeStatsBKG = GeneralROIIntensity(oriImg, labelsBKG, centroidsBKG)
	IntensityStatsT[0] = IntensityStatsBKG[0]
	modeStatsT[0] = modeStatsBKG[0]
	
	
	outputT = (numLabelsT, labelsT, statsT, centroidsT, IntensityStatsT, modeStatsT)
	
	FigureSavePath = os.path.join(SpecificImgFolder, "Lesion_Boarder_Visualization.pdf")
	images = [boarders]
	#print(threshAll.size,boarders.size)
	titles = ["Boarder" ]
	#showImages(images, titles, save = 1, path = FigureSavePath, text_coords = centroidsT)

	#print("Intensity stats: ")
	#print(IntensityStatsT)

	return outputT

def showDensities(img,densities, save = 0, path = ' '):
	"""Show centroids side-by-side with image."""
	"""plt.subplot(1,2,1),plt.imshow(img,'gray')
	plt.subplot(1,2,2),plt.scatter(centroids_x,-centroids_y)
	plt.show()"""
	centers_x = []
	centers_y = []
	dens = []
	for density in densities:
		centers_x.append(density[1][0])
		centers_y.append(density[1][1])
		dens.append(density[2])
	maxx = np.max(dens)
	minn = np.min(dens)
	mean = np.mean(dens)
	median = np.median(dens)
	std = np.std(dens)
	#print(mean)
	#print(median)
	#print(std)

	smin = 1
	smax = 20

	#PlotHistogram(dens)

	for i in range(len(dens)):
		#min-max feature scaling normalization, https://en.wikipedia.org/wiki/Normalization_(statistics)
		dens[i] = smin + (((dens[i] - minn)*(smax-smin))/(maxx-minn))


	implot = plt.imshow(img,'gray')
	plt.scatter(centers_x, centers_y, s=dens,c="red")
	if save == 0:
		plt.show()
	else:
		plt.savefig(path, bbox_inches='tight')
	plt.close('all')

def PlotHistogram(data):
	# Creating histogram
	fig, ax = plt.subplots(figsize =(10, 7))
	ax.hist(data, bins = 20)
	 
	# Show plot
	plt.show()
	plt.close('all')

def loadKerasModel(filename):
    """Load h5 model file."""
    return load_model(filename)

def getPredictions(cells, model):
	"""Find predictions for all cells in image."""
	p=0
	c=0
	for cell in cells:

		if cell['skipped'] == "No":
			#MacLearnPredict = []
			
			if p == 50:
				value = (c/len(cells))*100
				formatted_string = "{:.2f}".format(value)
				float_value = float(formatted_string)
				if useKeras:
					print("          Keras ",float_value, " % complete")
				p=0
				c= c+1
			else:
				p=p+1
				c=c+1
			for i in range(len(namChannels)):
				if i > 0:
					if namChannels[i] == 'CC1' or namChannels[i] == 'PLP':
						img = cell['RGBs'][namChannels[i]][0]
						img = img.astype('float64')
						img = np.expand_dims(img, axis=0)

						if useKeras:
							predict = model.predict(img)
							predict = predict[0][0]
						else:
							predict = 0
					else:
						predict = 0
					cell['RGBs'][namChannels[i]].append(predict)
			
	return cells

def Cells_to_df(cells):

	######Add
	#Build Titles, accounting for variable number of Vischannels and lesions per image
	columnTitles = ["Original Filename","Cell ID", "X","Y", "skipped", 'location']
	TitlesIA = []
	for i in range(len(namChannels)):
		ch_nam = namChannels[i]
		centintensTitle = ch_nam + " Main Nuclei Pixel Intensity"
		centareaTitle = ch_nam + " Main Nuclei Area (pixels^2)"

		allintensTitle = ch_nam + " All Nuclei Pixel Intensity"
		allareaTitle = ch_nam + " All Nuclei Area (pixels^2)"

		otherintensTitle = ch_nam + " Non-main Nuclei Pixel Intensity"
		otherareaTitle = ch_nam + " Non-main Nuclei Area (pixels^2)"

		bkgintensTitle = ch_nam + " Background Pixel Intensity"
		bkgareaTitle = ch_nam + " Background Area (pixels^2)"
		if i > 0:
			MacLearnPredTitle = ch_nam + " Machine Learning Prediction"
			TitlesIA.extend([MacLearnPredTitle, centintensTitle,centareaTitle,allintensTitle,allareaTitle,otherintensTitle,otherareaTitle,bkgintensTitle,bkgareaTitle])

		else:
			TitlesIA.extend([centintensTitle,centareaTitle,allintensTitle,allareaTitle,otherintensTitle,otherareaTitle,bkgintensTitle,bkgareaTitle])
	columnTitles.extend(TitlesIA)

	LesTitles = []
	for i in range(numLabels+1):
		if i == 0:
			LesAreaNam = "Background Area (mm^2)"
			LesTitles.append(LesAreaNam)
			LesAreapixNam = "Background Area (pixels^2)"
			LesTitles.append(LesAreapixNam)
			for chnam in namChannels:
				chInten = "Background Raw Intensity " + chnam
				chmode = "Background Mode Intensity Value " + chnam
				LesTitles.append(chInten)
				LesTitles.append(chmode)

		else :
			LesAreaNam = "ROI " + str(i) + " Area (mm^2)"
			LesTitles.append(LesAreaNam)
			LesAreapixNam = "ROI " + str(i) + " Area (pixels^2)"
			LesTitles.append(LesAreapixNam)
			for chnam in namChannels:
				chInten = "ROI " + str(i) + " Raw Intensity " + chnam
				LesTitles.append(chInten)
				chmode = "ROI " + str(i) + " Mode Intensity Value " + chnam
				LesTitles.append(chmode)

	columnTitles.extend(LesTitles)


	#Build a new cells (cellsAnno) that is more ammenabel to dataframe construction
	cellsAnno = []

	for cell in cells:
		cellAnno = []
		cellAnno.extend([cell['oriImgName'], cell['CellID'], cell['centroids'][0], cell['centroids'][1], cell['skipped'], cell['location']['location_int']])
		if cell['skipped'] == 'No' :
			intensAreaVal = []
			for i in range(len(namChannels)):
				ch_nam = namChannels[i]
				centIntensVal = cell['stats'][ch_nam][0][0]
				centareaVal = cell['stats'][ch_nam][0][1]

				allintensVal = cell['stats'][ch_nam][1][0]
				allareaVal = cell['stats'][ch_nam][1][1]

				otherintensVal = cell['stats'][ch_nam][2][0]
				otherareaVal = cell['stats'][ch_nam][2][1]

				bkgintensVal = cell['stats'][ch_nam][3][0]
				bkgareaVal = cell['stats'][ch_nam][3][1]
				if i > 0:
					MacLearnPred = cell['RGBs'][ch_nam][1]
					cellAnno.extend([MacLearnPred,centIntensVal,centareaVal,allintensVal,allareaVal,otherintensVal,otherareaVal,bkgintensVal,bkgareaVal])
				else:
					cellAnno.extend([centIntensVal,centareaVal,allintensVal,allareaVal,otherintensVal,otherareaVal,bkgintensVal,bkgareaVal])
			for i in range(numLabels+1):

				areamm2 = cell['location']['Areas_info'][i]
				cellAnno.append(areamm2)

				areapix = cell['location']['Areas_infoPix'][i]
				cellAnno.append(areapix)

				for chnam in namChannels:
					roiIntensity = int(cell['location']['ROIintensities'][i][chnam])
					#print('roiIntensity ', i, roiIntensity)
					roiChmode = cell['location']['ROImodes'][i][chnam]
					cellAnno.append(roiIntensity)
					cellAnno.append(roiChmode)

			cellsAnno.append(cellAnno)


	#might need to fill empty spaces with 0's here
	#print('cells', cells[0]['location']['ROIintensities'][0][namChannels[2]])
	#print('cellsAnno',cellsAnno[0][columnTitles.index('Background Raw Intensity Sox2')])
	df = pd.DataFrame(data=cellsAnno, columns=columnTitles)
	#print('df', df.at[0,'Background Raw Intensity Sox2'])
	return df

def ProcessRawResults(df, Summary, cell_type_conditions, cell_types_to_analyze):
	if not os.path.exists(HandAuditdfsave):
		#Dataframe-wide computation
		for i in range(len(namChannels)):
			ToHisto = []
			ch = namChannels[i]
			#Calculate Main cell Mean florecence for each channel 
			MeanNewcolumnTitle = ch + " Main Cell Mean Fluorescence (Intensity/pix^2)"
			IntensColumnTitle1 = ch + " Main Nuclei Pixel Intensity"
			AreaColumnTitle2 = ch + " Main Nuclei Area (pixels^2)"
			df[MeanNewcolumnTitle] = df[IntensColumnTitle1] / df[AreaColumnTitle2]
			ToHisto.extend([AreaColumnTitle2, MeanNewcolumnTitle])

			#Calculate bkg Mean florecence for each channel 
			NewcolumnTitle = ch + " Bkg Mean Fluorescence (Intensity/pix^2)"
			ColumnTitle1 = ch + " Background Pixel Intensity"
			ColumnTitle2 = ch + " Background Area (pixels^2)"
			df[NewcolumnTitle] = df[ColumnTitle1] / df[ColumnTitle2]

			#Calculate Relative florecence for the main cell for each channel 
			RelNewcolumnTitle = ch + " Relative Fluorescence (Main/Bkg)"
			ColumnTitle1 = ch + " Main Cell Mean Fluorescence (Intensity/pix^2)"
			ColumnTitle2 = ch + " Bkg Mean Fluorescence (Intensity/pix^2)"
			df[RelNewcolumnTitle] = df[ColumnTitle1] / df[ColumnTitle2]
			ToHisto.extend([RelNewcolumnTitle])

		#Calculate image-specific thresholds
		#https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
		
		"""	SpecificImgResultsPath = os.path.join(ResultsFolderPath,"Image_Specific_Results")
		SpecificImgFolder = os.path.join(SpecificImgResultsPath, Image[:-4] + " Results")"""
		
		for i in range(len(namChannels)):
			ToHisto = []
			ch = namChannels[i]
			AreaColumnTitle = ch + " Main Nuclei Area (pixels^2)"
			IntensColumnTitle = ch + " Main Nuclei Pixel Intensity"
			MeanNewcolumnTitle = ch + " Main Cell Mean Fluorescence (Intensity/pix^2)"
			RelNewcolumnTitle = ch + " Relative Fluorescence (Main/Bkg)"
			MacLearnPredTitle = ch + " Machine Learning Prediction"
			bkgIntensTitle = ch + " Background Pixel Intensity"
			bkgMeanTitle = ch + " Bkg Mean Fluorescence (Intensity/pix^2)"

			#Define Threshold values for all of the parameters (size, mean intensity, relative intensity, maclearn(well its 1))
			#sizethresh is set at 10 to 250 pix^2, or ~4um^2 to ~105um^2
			sizeThresh_um2 = [4.3,300]
			sizeThresh = [sizeThresh_um2[0]*(scale**2),sizeThresh_um2[1]*(scale**2)]
			df["SizeThreshed"] = np.where((df[AreaColumnTitle] > sizeThresh[0]) & (df[AreaColumnTitle] < sizeThresh[1]), 1, 0)

			IntensMean = np.mean(df[IntensColumnTitle])
			IntensStd = np.std(df[IntensColumnTitle])		
			IntensThresh = IntensMean + (0.25*IntensStd)
			IntensThreshedTitle = ch + " IntensThreshed"
			df[IntensThreshedTitle] = np.where((df[IntensColumnTitle] >= IntensThresh), 1, 0)

			#based on the average bkg mean intensity of the whole image
			bkgmean = np.mean(df[bkgMeanTitle])
			MeanThresh = bkgmean + (np.std(df[bkgMeanTitle]))
			MeanThreshedTitle = ch + " MeanThreshed"
			df[MeanThreshedTitle] = np.where((df[MeanNewcolumnTitle] >= MeanThresh), 1, 0)

			#based on relationship between the the immediate bkg around each nuclei
			#RelMean = np.mean(df[RelNewcolumnTitle])
			#RelStd = np.std(df[RelNewcolumnTitle])		
			RelIntensThreshlow = Relthreshs[i][0]
			RelIntensThreshhigh = Relthreshs[i][1]
			RelThreshedTitle = ch + " RelThreshed"
			#high confidence rel thresh
			df[RelThreshedTitle] = np.where((df[RelNewcolumnTitle] >= RelIntensThreshhigh), 1, 0)
			#low confidence rel thresh
			df[RelThreshedTitle] = np.where((df[RelNewcolumnTitle] >= RelIntensThreshlow) & (df[IntensColumnTitle] >= bkgmean), 1, df[RelThreshedTitle])
			if i != 0:
				MacLearnThreshedTitle = ch + " MacLearnThreshed"
				df[MacLearnThreshedTitle] = np.where((df[MacLearnPredTitle] >= 0.5), 1, 0)


			#Identify different types of positivity FUNCTIONALITY NOT CURRENTLY BEING USED
			# 1 means just maclearn predicted
			# 2 means predicted positive in the traditional sense
			# 3 both maclearn and traditional positive

			Postivity_RankTitle = ch + " Postivity_Rank"
			df[Postivity_RankTitle] = 0
			if ch == 'DAPI_ch':
				df[Postivity_RankTitle] = np.where((df[IntensColumnTitle] > 0), 1, 0)
			elif ch == 'CC1' or ch == 'PLP':
				df[Postivity_RankTitle] = np.where((df[MacLearnThreshedTitle] == 1), 1, df[Postivity_RankTitle])
			else:
					#df[Postivity_RankTitle] = np.where((df["SizeThreshed"] == 1) & (df[MeanThreshedTitle] == 1), 1, df[Postivity_RankTitle])
					df[Postivity_RankTitle] = np.where( (df["SizeThreshed"] == 1) & (df[RelThreshedTitle] == 1), 1, df[Postivity_RankTitle])
			
			if debugProcessRawResults or debug:
				ToHisto = [AreaColumnTitle,IntensColumnTitle,MeanNewcolumnTitle,RelNewcolumnTitle]
				#debug Histograms to show distribution of values for each channel, have the threshold appear on that histogram
				dfnonan= df.fillna(0)
				fig, axes = plt.subplots(len(ToHisto),figsize = (10,10))
				fig.tight_layout(h_pad=2)
				for i in range(len(ToHisto)):
					axes[i].hist(dfnonan[ToHisto[i]], alpha = 0.5, bins = 80, label="Main")
					Mean = np.mean(dfnonan[ToHisto[i]])
					Std = np.std(dfnonan[ToHisto[i]])
					axes[i].title.set_text(ToHisto[i])
					if i == 0:
						axes[i].axvline(x=10, color='orange', linestyle='dashed', linewidth=1)
						axes[i].axvline(x=250, color='orange', linestyle='dashed', linewidth=1)
						axes[i].text(10,0,'Threshold',color='orange')
					elif i == 2:
						axes[i].hist(dfnonan[bkgMeanTitle],alpha = 0.5, color='pink', bins = 20, label="bkg mean")
						axes[i].axvline(x=MeanThresh, color='orange', linestyle='dashed', linewidth=1)
						axes[i].text(MeanThresh,0,'Threshold',color='orange')
						axes[i].legend(loc='upper right')
					else:
						axes[i].axvline(x=Mean, color='blue', linestyle='dashed', linewidth=1)
						axes[i].text(Mean,0,'mean',color='blue')
						axes[i].axvline(x=Mean+Std, color='red', linestyle='dashed', linewidth=1)
						axes[i].text(Mean+Std,0,'mean + 1std',color='red')
						axes[i].axvline(x=Mean+(Std*0.25), color='orange', linestyle='dashed', linewidth=1)
						axes[i].text(Mean+(Std*0.25),0,'Threshold',color='orange')
					figname = ch + " Thresholding_Histograms"
					FigureSavePath = os.path.join(SpecificImgFolder,figname)
				#plt.savefig(FigureSavePath)
				
				plt.show()
				plt.close('all')


		#Adjust for Sox2 bleed through
		if 'Sox2' in namChannels:
			Sox2pos = "Sox2 Postivity_Rank"
			Olig2pos = "Olig2 Postivity_Rank"

			Sox2lowthresch = 2
			
			Sox2Rel = "Sox2 Relative Fluorescence (Main/Bkg)"
			df[Sox2pos] = np.where( (df[Olig2pos] == 0) & (df[Sox2Rel] >= Sox2lowthresch) & (df["SizeThreshed"] == 1), 1, df[Sox2pos])
	



	#Visual Validation? Need to load cells

	#Define positive cell types

	for i in range(len(cell_types_to_analyze)):
		conditions = []
		celltypename = cell_types_to_analyze[i]
		Definitions = cell_type_conditions[celltypename]
		#make a boolean array for each condition then compare the booleans at each positon
		for j in range(len(Definitions)):

			ch_nam = Definitions[j][0]
			val = Definitions[j][1]
			Postivity_RankTitle = ch_nam + " Postivity_Rank"
			conditions.append(df[Postivity_RankTitle] == val)

		#reshape the resulting boolean arrays to stay consistent
		conditions = np.array(conditions)
		conditions = np.rot90(conditions,k=-1)
		conditions = np.fliplr(conditions)

		
		#callapse the boolean arrays to a single boolean array
		callapsedConditions =[]
		for row in conditions:
			callapsedConditions.append(all(row))

		callapsedConditions = np.array(callapsedConditions)

		df[celltypename] = np.where(callapsedConditions,1, 0)

	df.to_csv(UpdateResultSave, index = False)

	#Build Summary

	Summary.append({'Original Filename': df['Original Filename'][0]})
	cell_types = cell_types_to_analyze.copy()
	

	for i in range(len(namChannels)):
		ch = namChannels[i]
		Postivity_RankTitle = ch + " Postivity_Rank"
		df['Quantification'] = np.where((df[Postivity_RankTitle] == 1) & (df["location"] == 0), 1, 0)
		cellNumber = np.sum(df['Quantification'])
		area = df['Background Area (mm^2)'][0]
		density = cellNumber/area

		areapix = df['Background Area (pixels^2)'][0]
		RawIntenstitle = 'Background Raw Intensity ' + ch
		ModeIntenstitle = 'Background Mode Intensity Value ' + ch
		ModeIntens = df[ModeIntenstitle][0]
		RawIntens = df[RawIntenstitle][0]
		meanIntenstitle = 'Background Mean Intensity ' + ch + ' (Sum Intensity/pixels^2)'

		meanIntens = RawIntens/areapix
		cellnumtitle = 'Background ' + ch + ' Positive Cell Number'
		celldenstitle = 'Background ' + ch + ' Positive Cells Density (cells/mm^2)'
		#Summary[-1][cellnumtitle] = cellNumber
		#Summary[-1][celldenstitle] = density
		#Summary[-1][RawIntenstitle] = RawIntens
		#print("rawintens", RawIntens)
		#Summary[-1][meanIntenstitle] = meanIntens
		#Summary[-1][ModeIntenstitle] = ModeIntens

	for cell_type in cell_types:
		df['Quantification'] = np.where((df[cell_type] == 1) & (df["location"] == 0), 1, 0)
		cellNumber = np.sum(df['Quantification'])
		area = df['Background Area (mm^2)'][0]
		density = cellNumber/area
		cellnumtitle = 'Background ' + cell_type + ' Number'
		celldenstitle = 'Background ' + cell_type + ' Density (cells/mm^2)'
		#Summary[-1][cellnumtitle] = cellNumber
		#Summary[-1][celldenstitle] = density

	

	if ROINumber == 0:
		ROIcycle = 1
	else:
		ROIcycle = ROINumber
	seperator = "||"
	for i in range(ROIcycle):
		ROI = i+1
		lesTitle = 'ROI '+ str(ROI) +' Area (mm^2)'
		lesTitlepix = 'ROI '+ str(ROI) +' Area (pixels^2)'
		area = df[lesTitle][0]
		areapix = df[lesTitlepix][0]
		Summary[-1][lesTitle] = area
		Summary[-1][lesTitlepix] = areapix
		for y in range(len(namChannels)):
			ch = namChannels[y]
			Postivity_RankTitle = ch + " Postivity_Rank"
			df['Quantification'] = np.where((df[Postivity_RankTitle] == 1) & (df["location"] == ROI), 1, 0)
			cellNumber = np.sum(df['Quantification'])
			density = cellNumber/area
			cellnumtitle = 'ROI '+ str(ROI) + ' ' + ch + ' Positive Cell Number'
			celldenstitle = 'ROI '+ str(ROI) + ' ' + ch + ' Positive Cells Density (cells/mm^2)'
			ModeIntenstitle = "ROI " + str(ROI) + " Mode Intensity Value " + ch
			ModeIntens = df[ModeIntenstitle][0]
			RawIntenstitle = 'ROI '+ str(ROI) + ' Raw Intensity ' + ch
			RawIntens = df[RawIntenstitle][0]
			meanIntenstitle = 'ROI '+ str(ROI) + ' Mean Intensity ' + ch + ' (Sum Intensity/pixels^2)'
			meanIntens = RawIntens/areapix

			Summary[-1][cellnumtitle] = cellNumber
			#Summary[-1][celldenstitle] = density
			Summary[-1][RawIntenstitle] = RawIntens
			#Summary[-1][meanIntenstitle] = meanIntens
			#Summary[-1][ModeIntenstitle] = ModeIntens


		for cell_type in cell_types:
			df['Quantification'] = np.where((df[cell_type] == 1) & (df["location"] == ROI), 1, 0)
			cellNumber = np.sum(df['Quantification'])
			density = cellNumber/area
			cellnumtitle = 'ROI '+ str(ROI) +' ' + cell_type + ' Number'
			celldenstitle = 'ROI '+ str(ROI) +' ' + cell_type + ' Density (cells/mm^2)'
			Summary[-1][cellnumtitle] = cellNumber
			#Summary[-1][celldenstitle] = density

		'''
		#Add percentage calculations
		if bool(PercentCalcs):
			for percentcalc in PercentCalcs:
				PercentTitle = 'ROI '+ str(ROI) + " " +str(percentcalc[0]) + '/' + str(percentcalc[1])
				cellnumtitle1 = 'ROI '+ str(ROI) +' ' + percentcalc[0] + ' Number'
				cellnumtitle2 = 'ROI '+ str(ROI) +' ' + percentcalc[1] + ' Number'
				cellnum1 = Summary[-1][cellnumtitle1]
				cellnum2 = Summary[-1][cellnumtitle2]
				Percent = (cellnum1 / cellnum2) *100

				#print(PercentTitle, Percent)

				Summary[-1][PercentTitle] = Percent

		'''
		seperator = seperator +' '
		Summary[-1][seperator] = '||'

	if perilesionanalysis:
		pericore = ["LesionEdge","Core"]
		for k in range(len(pericore)):
			ROI = pericore[k]
			pericoreKey = k + 1
			lesTitle = str(ROI) +' Area (mm^2)'
			lesTitlepix = str(ROI) +' Area (pixels^2)'
			areapix = pericoreAreapx[k]
			area = (areapix/(scale**2))/1000000

			Summary[-1][lesTitle] = area
			Summary[-1][lesTitlepix] = areapix
			for y in range(len(namChannels)):
				ch = namChannels[y]
				Postivity_RankTitle = ch + " Postivity_Rank"
				df['Quantification'] = np.where((df[Postivity_RankTitle] == 1) & (df["Edge1Core2"] == pericoreKey), 1, 0)
				cellNumber = np.sum(df['Quantification'])
				density = cellNumber/area
				cellnumtitle = str(ROI) + ' ' + ch + ' Positive Cell Number'
				celldenstitle = str(ROI) + ' ' + ch + ' Positive Cells Density (cells/mm^2)'

				Summary[-1][cellnumtitle] = cellNumber
				Summary[-1][celldenstitle] = density


			for cell_type in cell_types:
				df['Quantification'] = np.where((df[cell_type] == 1) & (df["Edge1Core2"] == pericoreKey), 1, 0)
				cellNumber = np.sum(df['Quantification'])
				density = cellNumber/area
				cellnumtitle = str(ROI) +' ' + cell_type + ' Number'
				celldenstitle = str(ROI) +' ' + cell_type + ' Density (cells/mm^2)'
				Summary[-1][cellnumtitle] = cellNumber
				Summary[-1][celldenstitle] = density

			#Add percentage calculations
			if bool(PercentCalcs):
				for percentcalc in PercentCalcs:
					PercentTitle = str(ROI) + " " +str(percentcalc[0]) + '/' + str(percentcalc[1])
					cellnumtitle1 = str(ROI) +' ' + percentcalc[0] + ' Number'
					cellnumtitle2 = str(ROI) +' ' + percentcalc[1] + ' Number'
					cellnum1 = Summary[-1][cellnumtitle1]
					cellnum2 = Summary[-1][cellnumtitle2]
					Percent = (cellnum1 / cellnum2) *100

					#print(PercentTitle, Percent)

					Summary[-1][PercentTitle] = Percent

	if MFIPercAreaAnalysis:
		for i in range(len(ROINames)):
			AreaTitle = ROINames[i] + " Area (mm^2)"
			Summary[-1][AreaTitle] = ROIAreaList[i]
			for j in range(len(namChannels)):
				MFITitle =  ROINames[i] + namChannels[j] + " MFI"
				PercAreaThreshTitle = ROINames[i] +  namChannels[j] + " Percent Thresh Area"

				Summary[-1][MFITitle] = ROIMFIList[i][j]
				Summary[-1][PercAreaThreshTitle] = ROIPercAreaList[i][j]


	return Summary
				
class PolygonDrawer(object):
	def __init__(self, window_name, img, ROINumber, screensize):
		self.window_name = window_name # Name for our window
		self.img = img
		self.imgheight, self.imgwidth = self.img.shape[0:2]

		self.smallwidth = int(screensize[0] * 0.8)
		self.smallheight = int(self.smallwidth*(self.imgheight/self.imgwidth))
		
		
		if self.smallheight > screensize[1]:
			self.smallheight = int(screensize[1] * 0.8)
			self.smallwidth = int(self.smallheight*(self.imgwidth/self.imgheight))
			

		self.smallImg = cv.resize(self.img, (self.smallwidth,self.smallheight))

		self.done = False # Flag signalling we're done with one polygon
		self.doneAll = False # Flag signalling we're done with all polygons

		self.current = (0, 0) # Current position, so we can draw the line-in-progress
		self.points = [] # List of points defining our polygon
		self.polygons = [] # List of all polygons
		self.FINAL_LINE_COLOR = (255, 255, 255)
		self.WORKING_LINE_COLOR = (127, 127, 127)
		self.scaleheight = self.imgheight/self.smallheight
		self.scalewidth = self.imgwidth/self.smallwidth
		print(self.scalewidth)


	def on_mouse(self, event, x, y, buttons, user_param):
		# Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)

		if self.done: # Nothing more to do
			return

		if event == cv.EVENT_MOUSEMOVE:
			# We want to be able to draw the line-in-progress, so update current mouse position
			self.current = (x, y)

		elif event == cv.EVENT_LBUTTONDOWN:
			# Left click means adding a point at current position to the list of points
			print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
			self.points.append([x, y])

		elif event == cv.EVENT_RBUTTONDOWN:
			# Right click means we're done
			print("Completing polygon with %d points." % len(self.points))
			self.done = True


	def run(self):
		# Let's create our working window and set a mouse callback to handle events

		cv.namedWindow(self.window_name, flags=cv.WINDOW_AUTOSIZE)
		cv.imshow(self.window_name, np.zeros((self.imgheight, self.imgwidth), np.uint8))
		cv.waitKey(1)
		cv.setMouseCallback(self.window_name, self.on_mouse)
		i = 0
		for i in range(ROINumber):
			self.done = False
			if i == 0:
				Polycanvas = np.copy(self.smallImg, subok= True)
				cv.imshow(self.window_name, Polycanvas)

			while(not self.done):
				# This is our drawing loop, we just continuously draw new images
				# and show them in the named window
				canvas = np.copy(Polycanvas, subok= True)
				if (len(self.points) > 0):
					# Draw all the current polygon segments
					cv.polylines(canvas, np.array([self.points]), False, self.FINAL_LINE_COLOR, 1)
					# And  also show what the current segment would look like
					cv.line(canvas, tuple(self.points[-1]), self.current, self.WORKING_LINE_COLOR)
				# Update the window
				cv.imshow(self.window_name, canvas)
				# And wait 50ms before next iteration (this will pump window messages meanwhile)
				if cv.waitKey(50) == 27: # ESC hit
					self.done = True

			# User finised entering the polygon points, so let's make the final drawing

			# of a filled polygon
			if (len(self.points) > 0):
				print("points",self.points)

				cv.fillPoly(Polycanvas, np.array([self.points]), self.FINAL_LINE_COLOR)
			# And show it
			cv.imshow(self.window_name, Polycanvas)

			#scale points to original image
			self.ScalePoints = []
			for point in self.points:
				point[0] = math.floor(point[0] * self.scalewidth)
				point[1] = math.floor(point[1] * self.scaleheight)

				self.ScalePoints.append(point)

			self.polygons.append(self.ScalePoints)

			self.points = []
			self.ScalePoints = []

			# Waiting for the user to press any key
			i = i + 1

		cv.destroyWindow(self.window_name)

		return self.polygons

def GeneralROIIntensity(oriImg, labels, centroids):
	intensitStats =[]
	modeStats = []

	
	for i in range(len(centroids)):
		#print('i = '+ str(i))
		#print(np.max(labels))
		mask = np.copy(labels)
		mask[mask > i] = 0
		mask[mask < i] = 0
		mask[mask == i] = 1
		mask = np.uint8(mask)
		chIntensity = {}
		chmode = {}
		for j in range(len(namChannels)):
			chnam = namChannels[j]
			channel = oriImg[j]
			channelmasked = cv.bitwise_and(channel, channel, mask=mask)
			intensity = np.sum(channelmasked)
			#print(str(chnam) + ' max of channel ' + str(np.max(channel)))
			#print('intensity ' + str(intensity))
			counts, bins = np.histogram(channelmasked[channelmasked>0], bins=np.arange(65536))

			mode = np.argmax(counts)
			chIntensity[chnam] = intensity
			chmode[chnam] = mode
		
		intensitStats.append(chIntensity)
		modeStats.append(chmode)
	return [intensitStats, modeStats]

def ProcessHandaudit(path, celldf, clickTolerance):
	handAudit = pd.read_csv(path)
	for i in range(len(namChannels)):
		chnPos = namChannels[i] + " Postivity_Rank";
		IntensColumnTitle = namChannels[i] + " Main Nuclei Pixel Intensity"
		if namChannels[i] == 'DAPI_ch':
			celldf[chnPos] = np.where((celldf[IntensColumnTitle] > 0), 1, 0)
		if i > 0:
			xnam = namChannels[i] + " X"
			ynam = namChannels[i] + " Y"
			coords = handAudit[[xnam, ynam]]
			celldf[chnPos] = 0
			counter = 0
			tocker = 0

			for j in range(len(coords)):
				
				xco = coords[xnam][j]
				yco = coords[ynam][j]
				
				xycell = celldf[['X','Y']].values.tolist()
				
				#distances = map(FindDistance, xycell)

				distances = map(lambda x: FindDistance(xco,yco,x), xycell)
				distances = list(distances)
				
				min_value = min(distances)
				min_index = distances.index(min_value)
				if min_value < clickTolerance:
					celldf[chnPos][min_index] = 1

				else:
					celldf[chnPos][min_index] = 0

				counter = counter + 1
				tocker = tocker + 1
				Cordspercent = str((counter/len(coords))*100)
				if tocker > 50:
					print(namChannels[i],Cordspercent[0:6])
					tocker = 0
	return celldf

def FindDistance(x1,y1,compcoords):
	x2 = compcoords[0]
	y2 = compcoords[1]
	distance = math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))
	return distance


def saveBorder(images, UserROIs, titles='', path = ' ', text_coords = []):
	"""Show centroids side-by-side with image."""

	sizeh = images.shape[0]
	sizew = images.shape[1]

	dpiscale = 1000
	scaleh = sizeh/dpiscale
	scalew = sizew/dpiscale

	colors = ['#1f77b4']
	
	Linewidth = 0.5
	fig = plt.figure(frameon=False, figsize=(scalew, scaleh), dpi=100)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

	img = np.zeros((sizeh, sizew), np.uint8)
	ax.imshow(img, aspect='auto')

	for j in range(len(UserROIs)):
		polygon = UserROIs[j]
		polygon.append(polygon[0]) #repeat the first point to create a 'closed loop'

		xs, ys = zip(*polygon) #create lists of x and y values
		
		color = colors[0]
		
		plt.plot(xs,ys) 
		
		#fig.savefig(fname, dpiscale)
		# Save the image in memory in PNG format

	png1 = BytesIO()
	fig.savefig(png1, format="png", dpi = dpiscale)

	# Load this image into PIL
	png2 = Image.open(png1)

	# Save as TIFF
	FigureSavePath = os.path.join(path, "Borders.tiff")
	png2.save(FigureSavePath)
	png1.close()

				
def perilesionAnalyser(df,images,ROIs):
	bordersize = 75
	images = images[0]
	pxbordersize = scale * bordersize
	pxbordersize = int(round_up_to_odd(pxbordersize))

	points = df[['X','Y']].values.tolist()
	sizeh = images.shape[0]
	sizew = images.shape[1]
	canvas = np.zeros((sizeh,sizew), dtype= np.uint8)

	

	polygon = UserROIs[0]

	perilesioncoords = []

	
	polygon = np.array([polygon])
	oripoly = np.zeros((sizeh,sizew), dtype= np.uint8)
	fill = 255

	cv.fillPoly(oripoly, polygon, fill)

	Largepoly = np.copy(oripoly)
	
	#ret, thresh1 = cv.threshold(bincanvas, 0, 255, cv.THRESH_BINARY)
	output = cv.connectedComponentsWithStats(oripoly)

	polyWidth = output[2][1][2]
	polyarea = output[2][1][4]
	iterWidth = output[2][1][2]

	#kernel = np.ones((5,5),np.uint8)
	kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(pxbordersize,pxbordersize))

	oripoly = np.where(oripoly == 255, 127, oripoly)

	#Circular erode a 50um circ. kernel
	Largepoly = cv.erode(Largepoly, kernel, iterations= 1)
	iteroutput = cv.connectedComponentsWithStats(Largepoly)
	iterWidth = iteroutput[2][1][2]
	iterarea = iteroutput[2][1][4]


	#change the values arround the lesion that are in the perilesion
	oripoly = np.where( Largepoly == 255, 255 , oripoly)

	if debugperilesion:
		plt.imshow(oripoly,cmap="gray")
		plt.show()

	#go through all of the cell coordinates, and if its location = 127 then give it a perilesion flag

	perilesioncoords = map(lambda x: inperi(x, oripoly), points)
	perilesioncoords = list(perilesioncoords)

	df['Edge1Core2'] = perilesioncoords

	perilesion = np.copy(oripoly)
	core = np.copy(oripoly)

	perilesion = np.where( perilesion == 127, 1 , 0)
	core = np.where( core == 255, 1 , 0)

	perilesAreapx = np.sum(perilesion)
	coreAreapx = np.sum(core)

	pericore = [perilesAreapx,coreAreapx]

	return df, pericore


def centroid(vertexes):
     _x_list = [vertex [0] for vertex in vertexes]
     _y_list = [vertex [1] for vertex in vertexes]
     _len = len(vertexes)
     _x = sum(_x_list) / _len
     _y = sum(_y_list) / _len
     return(_x, _y)

def inperi(x,oripoly):
	loc = oripoly[int(x[1]), int(x[0])]
	val = 0
	if loc == 127:
		val = 1
	if loc == 255:
		val = 2

	return val

def round_up_to_odd(f):
    return np.ceil(f) // 2 * 2 + 1



def MFI_PerctArea(df,images,UserROIs):
	sizeh = images.shape[1]
	sizew = images.shape[2]
	canvas = np.zeros((sizeh,sizew), dtype= np.uint8)
	ROImaskList = []
	mainROIint = 0
	ROINames = ROITitles
	PLWM = False
	PLWMROIint = 1

	roiInt = 0

	#Create a list of masks where the ROI area is labelled with 1s

	for roi in UserROIs:
		roiInt = 1
		polygon = np.array([roi])
		roicanvas = np.copy(canvas)

		fill = roiInt

		cv.fillPoly(roicanvas, polygon, fill)

		ROImaskList.append(roicanvas)

	if PLWM:
		mainROI = np.copy(ROImaskList[mainROIint])
		PLWMROI = np.copy(ROImaskList[PLWMROIint])
		PLWMROI = np.where(mainROI == 1, 0,PLWMROI)
		ROImaskList[PLWMROIint] = PLWMROI

	if perilesionanalysis:
		bordersize = 75
		pxbordersize = scale * bordersize
		pxbordersize = int(round_up_to_odd(pxbordersize))
		kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(pxbordersize,pxbordersize))
		mainROI = np.copy(ROImaskList[mainROIint])
		mainROI = np.where( mainROI == 1, 255 , mainROI)
		core = np.copy(mainROI)
		core = cv.erode(mainROI, kernel, iterations= 1)
		perilesion = np.copy(mainROI)
		perilesion = np.where(core == 255, 0, perilesion)

		core = np.where(core == 255, 1, core)
		perilesion = np.where(perilesion == 255, 1, perilesion)

		ROImaskList.extend([core, perilesion])

	#if debugMFI:
		#showImages(ROImaskList, titles=ROINames)

	#Calculate Areas for each ROI
	ROIAreaList = []
	ROIAreapixList = []
	for roi in ROImaskList:
		areapix = np.sum(roi)
		area = (areapix/(scale**2))/1000000
		ROIAreaList.append(area)
		ROIAreapixList.append(areapix)

	#calculate MFI for each channel for each ROI
	ROIMFIList = []
	for i in range(len(ROImaskList)):
		roi = ROImaskList[i]
		roiArea = ROIAreapixList[i]
		mfiList = []
		for j in range(len(namChannels)):
			chanimg = images[j]
			IntesityMask = np.copy(roi)
			IntesityMask = np.where(roi == 1, chanimg, 0)
			TotalIntensity = np.sum(IntesityMask)
			MFIchan = TotalIntensity/roiArea
			mfiList.append(MFIchan)

		ROIMFIList.append(mfiList)


	#calculate % area above threshold
	ROIPercAreaList = []
	for i in range(len(ROImaskList)):
		#print(i)
		roi = ROImaskList[i]
		roiArea = ROIAreaList[i]
		roiAreapix = ROIAreapixList[i]
		PercAreaList = []
		print('roiAreapix ', roiAreapix)
		for j in range(len(namChannels)):
			#Threshold each channel, compare thresh methods?
			chanimg = np.copy(images[j])
			#chanimg = chanimg.astype('uint8')\
			chanimg = gammaCorrect(chanimg, gamma = gammas[j])
			chanimg = cv.bitwise_not(proccessVisualImage(chanimg))
			thresh = imageThreshold(chanimg,threshmethod)
			ThreshMask = np.copy(roi)
			ThreshMask = np.where(thresh == 0,0,ThreshMask)
			TotalMaskArea = np.sum(ThreshMask)
			PercAreachan = (TotalMaskArea/roiAreapix)*100
			PercAreaList.append(PercAreachan)

			if debugMFI and namChannels[j] == 'NF' :
				ShowIMG = [images[j],chanimg,thresh,ThreshMask]
				Titles = ['images[j]','chanimg','thresh','ThreshMask']
				debugMFIsave = os.path.join(SpecificImgFolder,"MFI Debug"+ROINames[i])
				showImages(ShowIMG, titles=Titles, save = 1, path = debugMFIsave)

				ShowIMG = [roi, ThreshMask]
				Titles = ['roi '+ str(roiAreapix) ,'ThreshMask '+ str(TotalMaskArea)+ " " + str(round(PercAreachan, 2)) + "%"]
				debugMFIsave = os.path.join(SpecificImgFolder,"MFI Debug 2"+ROINames[i])
				showImages(ShowIMG, titles=Titles, save = 1, path = debugMFIsave)				

				print('TotalMaskArea', TotalMaskArea)

		ROIPercAreaList.append(PercAreaList)

	#Add Results to Resultsdf
	
	for i in range(len(ROImaskList)):
		AreaTitle = ROINames[i] + " Area (mm^2)"
		df[AreaTitle] = ROIAreaList[i]
		for j in range(len(namChannels)):
			#print(ROIMFIList)
			MFITitle =  namChannels[j] + " MFI"
			PercAreaThreshTitle = namChannels[j] + " Percent Thresh Area"
			df[MFITitle] = ROIMFIList[i][j]
			df[PercAreaThreshTitle] = ROIPercAreaList[i][j]

		return df, ROINames, ROIAreaList, ROIMFIList, ROIPercAreaList




"""_____________________________________________________________________________________________________________________________"""

#Operational code
"""cells = [Index]{
					'oriImgName': ,
					'CellID',
					'centroids':[
								0 X
								1 Y
								], 
					'cellimg': , 
					'cellMarkers' : , 
					'skipped' : , 
					'stats' :	{	All areas for this are in pixels^2
									'namChannels[0]' : [[centIntensity,centArea], [allIntensity,allArea], [ otherIntensity,otherArea], [ backgroundIntensity,backgroundArea]],
									'namChannels[1]' : [[centIntensity,centArea], [allIntensity,allArea], [ otherIntensity,otherArea], [ backgroundIntensity,backgroundArea]], 
									'namChannels[2]' : [[centIntensity,centArea], [allIntensity,allArea], [ otherIntensity,otherArea], [ backgroundIntensity,backgroundArea]], 
									'namChannels[3]' : [[centIntensity,centArea], [allIntensity,allArea], [ otherIntensity,otherArea], [ backgroundIntensity,backgroundArea]], 
									...
									}
					'location': [
								'location_int' : 0 means not in any lesion, and lesions are numbered from 1 to n)
								'Areas_info' :		[
													0 Background Area
													1 Lesion 1 Area
													2 Lesio 2 Area
													...
													]
								

								] 
					8	'RGBs' : {
								  namChannels[1] : [RBBch_1, MaclearnPrediction]
								  namChannels[2] : [RBBch_2, MaclearnPrediction]
								  namChannels[3] : [RBBch_3, MaclearnPrediction]
								  ...
								  }
"""
#Settings
#See whole array
#np.set_printoptions(threshold=sys.maxsize, linewidth = 9999)




setup = settings.folder_dicts[41]
RabbitDescriptions = settings.RabbitDescriptions
Dataname = setup['name']
ImgFolderPath = setup['Path']

ROI_Draw_Channel = setup['ROI_Draw_Channel']
Nuclei_Identification_Channel = setup['Nuclei_Identification_Channel']

#What are the channels?
namChannels = setup['channels']
Relthreshs = setup['RelativeIntensityThreshold']

#What cell types are you looking to analyze?
#cell_types_to_analyze = ['OPC', 'Oligo', 'NonOligo']
	
#Desired cell image size
cropsize = setup['cropsize']

#How many ROIs do you want to define?
ROINumber = setup['ROINumber']

#Do you want to use the keras model?
useKeras = setup['useKeras']

#Change if using anything other then 10x
#Average scale for 10x images, pixel/micron
scale = setup['scale']

checkfiles = setup['checkfiles']

gammas = setup['gammas']

FastProcess = setup['FastProcess']

PercentCalcs = setup['PercentCalcs']

perilesionanalysis = setup['PerilesionAnalysis']

threshmethod = setup['threshmethod']

MFIPercAreaAnalysis = setup['MFIPercAreaAnalysis']

ROITitles = setup['ROITitles']



overwrite = False
overwriteROIS = False 
overwriteCells_Pred = True
overwriteProcessing = True
handAuditoverwrite = False

debug = False
debugThreshold = False
debugGamma = False
debugMarkers = False
debugChannels = False
debugMasking = False
debugImgPrepper = False 
debugcells = False
debugLesionIdenification1 = False
debugLesionIdenification2 = False
debugProcessRawResults = False 
debugCellLocations = True
debugperilesion = False
debugMFI = False


#Make Summary and  AllCellSpecificResults list of dictionaries
Summary = []

AllCellSpecificResults = pd.DataFrame()
Resultsdf = pd.DataFrame()
#Make the appropriate folder structure
ResultsFolderPath = os.path.join(ImgFolderPath,"Results")
if not os.path.exists(ResultsFolderPath):
	os.mkdir(ResultsFolderPath)

SummarySave = os.path.join(ResultsFolderPath, Dataname + '_Summary.csv')


SpecificImgResultsPath = os.path.join(ResultsFolderPath,"Image_Specific_Results")
if not os.path.exists(SpecificImgResultsPath):
	os.mkdir(SpecificImgResultsPath)

AllresultsSave = os.path.join(ResultsFolderPath, "AllCellSpecificResultsGood.csv")

#Build the appropriate image-specific structures and User Defined ROIs
#https://stackoverflow.com/questions/37099262/drawing-filled-polygon-using-mouse-events-in-open-cv-using-python
ImageID = 0
TotalImage = 0

# check to make sure each image has the specified number of channels
print("Checking Images for Uniformity")
badfiles = []
if checkfiles == True:
	for oriImgName in os.listdir(ImgFolderPath):
		fullpath = os.path.join(ImgFolderPath, oriImgName)
		if oriImgName.endswith('.tif'):
			img = cv.imreadmulti(fullpath, flags = -1)
			img = img[1]
			img = np.array(img)
			chanNum = img.shape[0]
			sizeh = img.shape[1]
			sizew = img.shape[2]
			if chanNum != len(namChannels) or sizeh == 512 or sizew ==512:
				badfiles.append(oriImgName)

# move bad files to a new folder
if len(badfiles) > 0:
	badfilespath = os.path.join(ImgFolderPath,"BadFiles")
	if not os.path.exists(badfilespath):
		os.mkdir(badfilespath)
	print(len(badfiles)," files were identified as bad and were moved to an adjoining folder")
	for file in badfiles:
		oldpath = os.path.join(ImgFolderPath, file)
		newpath = os.path.join(badfilespath, file)
		shutil.move(oldpath, newpath)

print('Draw ROIs')

for oriImgName in os.listdir(ImgFolderPath):
	fullpath = os.path.join(ImgFolderPath, oriImgName)
	if oriImgName.endswith('.tif'):
		SpecificImgFolder = os.path.join(SpecificImgResultsPath, oriImgName[:-4] + " Results")
		if not os.path.exists(SpecificImgFolder):
			os.mkdir(SpecificImgFolder)
		SampleCellsFolder = os.path.join(SpecificImgFolder,"Sample_Cells")
		if not os.path.exists(SampleCellsFolder):
			os.mkdir(SampleCellsFolder)
		BinarySave = os.path.join(SpecificImgFolder, "UserDefinedROIs.npy")
		if not os.path.exists(BinarySave) or overwriteROIS or overwrite:
			
			print('Image name:', oriImgName)
			img = cv.imreadmulti(fullpath, flags = -1)[1][ROI_Draw_Channel]
			#Dapi = adjust_visual(img, [0.05,0.98])
			#img = cv.bitwise_not(img)
			Dapi = gammaCorrect(img, gamma = gammas[Nuclei_Identification_Channel])
			#Dapi = cv.bitwise_not(proccessVisualImage(Dapi))
			Dapi = proccessVisualImage(Dapi)
			Dapi = np.array(Dapi)
			sizeh = Dapi.shape[0]
			sizew = Dapi.shape[1]
			'''
			if oriImgName.find('RB') > 0:
				RBstartread = oriImgName.find('RB')+2
				RBendread = RBstartread + 2
				windowname =
			'''

			if ROINumber > 0:
				windowname = str(oriImgName) +" : Draw " + str(ROINumber) + " ROIs"
				#Dapi = np.uint8(Dapi)
				polyDr = PolygonDrawer(windowname, Dapi, ROINumber,screensize)
				Lbinarr = polyDr.run()
				#print(Lbinarr)
				#np.savetxt(BinarySave, Lbinarr, delimiter=',')
				#Save fiji compatable boarder image

			else:
				Lbinarr = [[[1,1],[1,sizeh-1],[sizew-1,sizeh-1],[sizew-1,1]]]

			np.save(BinarySave, Lbinarr, allow_pickle=True, fix_imports=True)
			saveBorder(images=img, UserROIs=Lbinarr, path =SpecificImgFolder )
			#cv.imwrite(BinarySave,Lbinarr)
		TotalImage = TotalImage + 1




#Main For-Loop
for oriImgName in os.listdir(ImgFolderPath):
	fullpath = os.path.join(ImgFolderPath, oriImgName)
	
	if oriImgName.endswith('.tif'):
		ImageID = ImageID+1
		SpecificImgFolder = os.path.join(SpecificImgResultsPath, oriImgName[:-4] + " Results")
		if not os.path.exists(SpecificImgFolder):
			os.mkdir(SpecificImgFolder)

		SampleCellsFolder = os.path.join(SpecificImgFolder,"Sample_Cells")
		if not os.path.exists(SampleCellsFolder):
			os.mkdir(SampleCellsFolder)

		ImageResultsSave = os.path.join(SpecificImgFolder, "ImageCellSpecificResults.csv")
		print(" ")
		print("Image --> " + oriImgName)

		if not os.path.exists(ImageResultsSave) or overwriteCells_Pred or overwrite:
			
			#Additional folder structures

			print("Image ",ImageID, " of ", TotalImage,": Reading Image")
			oriImg = cv.imreadmulti(fullpath, flags = -1)
			oriImg = oriImg[1]
			oriImg = np.array(oriImg)
			visoriImg = np.copy(oriImg)
			
			for i in range(len(namChannels)): 
				visoriImg[i] = proccessVisualImage(visoriImg[i])
				visoriImg[i] = gammaCorrect(visoriImg[i], gammas[i])

			visoriImg = np.uint8(visoriImg)
			#MAKE DEEP COPIES (OR JUST ONE IMAGE AND ADJUST AS NEEDED)



			print("Image ",ImageID, " of ", TotalImage,": Processing Image ")

			if debugGamma or debug:
				for i in range(len(namChannels)):
					gamma1 = gammaCorrect(np.copy(oriImg[i]),gamma = 1)

					gamma0_75 = gammaCorrect(np.copy(oriImg[i]),gamma = 0.75)

					gamma0_5 = gammaCorrect(np.copy(oriImg[i]),gamma = 0.5)

					gamma0_25 = gammaCorrect(np.copy(oriImg[i]),gamma = 0.25)
					images = [gamma1, gamma0_75, gamma0_5, gamma0_25]
					titles = [ 'gamma: 1','gamma: 0.75','gamma: 0.5', 'gamma: 0.25']
					showImages(images,titles)

			print("Image ",ImageID, " of ", TotalImage,": Thresholding and Segmenting Image ")
			NucleiImg = np.copy(oriImg[Nuclei_Identification_Channel])
			NucleiImg = gammaCorrect(NucleiImg, gamma = gammas[Nuclei_Identification_Channel])
			NucleiImg = cv.bitwise_not(proccessVisualImage(NucleiImg))

			thresh = imageThreshold(NucleiImg,threshmethod)

			output = thresholdSegmentation(thresh,NucleiImg)
			centroids = output[1][3]
			markers = output[4]
			

			centroids_x = []
			centroids_y = []

			for i in range(len(centroids)):
				centroids_x.append(centroids[i][0])
				centroids_y.append(centroids[i][1])

			centroids_x = np.array(centroids_x)
			centroids_y = np.array(centroids_y)

			print("Image ",ImageID, " of ", TotalImage,": Getting Cell Images and making cells")
			cells = []
			cells = getCells(oriImg,visoriImg, centroids, markers)

			print("Image ",ImageID, " of ", TotalImage,": Processing User ROIs")
			BinarySave = os.path.join(SpecificImgFolder, "UserDefinedROIs.npy")
			UserROIs = np.load(BinarySave, allow_pickle=True)
			#_____________________________________________________________________________________________________________________________
			#Delete later
			'''
			ScaledUserROIs = os.path.join(SpecificImgFolder, "ScaledUserDefinedROIs.npy")
			if not os.path.exists(ScaledUserROIs):
				
				imgheight, imgwidth = oriImg[0].shape

				smallwidth = int(screensize[0] * 0.8)
				smallheight = int(smallwidth*(imgheight/imgwidth))
				
				if smallheight > screensize[1]:
					smallheight = int(screensize[1] * 0.8)
					smallwidth = int(smallheight*(imgwidth/imgheight))

				scaleheight = imgheight/smallheight
				scalewidth = imgwidth/smallwidth
				print('scaleheight', scaleheight)
				print('scalewidth', scalewidth)
				ScaledROIs = []
				print(UserROIs)
				for ROI in UserROIs:
					polygon = []
					for point in ROI:
						pointx = math.floor(point[0] * scalewidth)
						pointy = math.floor(point[1] * scaleheight)
						polygon.append([pointx,pointy])
					ScaledROIs.append(polygon)

				print(ScaledROIs)
				#np.save(ScaledUserROIs, UserROIs, allow_pickle=True, fix_imports=True)
				UserROIs = []
				UserROIs = ScaledROIs
				print(UserROIs)
				'''
			#_____________________________________________________________________________________________________________________________
			UserROIsOutput = LesionFigSave(DAPIImg=NucleiImg, UserROIs = UserROIs, screensize = screensize )

			(numLabels, labelsUserROI, stats, centroids, IntensityStats, modeStats) = UserROIsOutput

			
			print("Image ",ImageID, " of ", TotalImage,": Measuring Pixel Intensity for Each Cell")
			cells = AddStats(oriImg = oriImg ,cells = cells, labels = labelsUserROI, centroids = centroids, AreaStats = stats, IntensityStats = IntensityStats, modeStats = modeStats)
			if useKeras:
				print("Image ",ImageID, " of ", TotalImage,": Prepping Images for Keras")
			cells = MacLearnImgPrepper(cells)

			if debugcells or debug:
				for key in cells[3000]:
					print(key, " : ", cells[3000][key])
					print(" ")

			
			if useKeras:
				print("Image ",ImageID, " of ", TotalImage,": Beginning Keras Analysis")
			if useKeras:
				model = loadKerasModel(os.path.join(os.getcwd(), "CC1counting_wMar_5.8.h5"))
			else:
				model = 0
			cells = getPredictions(cells, model)
			if useKeras:
				print("End Keras")
			

			print("Image ",ImageID, " of ", TotalImage,": Saveing a Sample of the Cells")
			#Uncomment this to save x number of random cells (for survaying)
			#RandomSampler(cells, 10, SampleCellsFolder)

			print("Image ",ImageID, " of ", TotalImage,": Crafting the DataFrame and Saving the .csv file")
			#Build the Dataframe to analyse the data
			Resultsdf = Cells_to_df(cells)
	
			Resultsdf.to_csv(ImageResultsSave, index = False)

			#Get Summary data from Resultsdf for the lesions and save that to a persisting dataframe to construct the Summary.csv file
		#Shift to individual image analysis, as in just work with the current csv
		
		UpdateResultSave = os.path.join(SpecificImgFolder, "ImageCellSpecificResultsUpdate.csv")
		handAuditpath = os.path.join(SpecificImgFolder, "HandAudited.csv")
		HandAuditdfsave = os.path.join(SpecificImgFolder, "ImageCellSpecificResultsHandAudit.csv")
		
		if Resultsdf.empty:
			if os.path.exists(HandAuditdfsave):
				Resultsdf = pd.read_csv(HandAuditdfsave)
			elif os.path.exists(handAuditpath) or handAuditoverwrite:
				Resultsdf = pd.read_csv(ImageResultsSave)
				Resultsdf = ProcessHandaudit(path = handAuditpath, celldf = Resultsdf, clickTolerance = 10)
				Resultsdf.to_csv(HandAuditdfsave, index = False)
				
			else :
				Resultsdf = pd.read_csv(ImageResultsSave)

		if perilesionanalysis:
			oriImg = cv.imreadmulti(fullpath, flags = -1)
			oriImg = oriImg[1]
			oriImg = np.array(oriImg)
			BinarySave = os.path.join(SpecificImgFolder, "UserDefinedROIs.npy")
			UserROIs = np.load(BinarySave, allow_pickle=True)
			Resultsdf, pericoreAreapx = perilesionAnalyser(images = oriImg, df = Resultsdf, ROIs = UserROIs)

		if MFIPercAreaAnalysis:
			oriImg = cv.imreadmulti(fullpath, flags = -1)
			oriImg = oriImg[1]
			oriImg = np.array(oriImg)
			
			BinarySave = os.path.join(SpecificImgFolder, "UserDefinedROIs.npy")
			UserROIs = np.load(BinarySave, allow_pickle=True)
			Resultsdf, ROINames, ROIAreaList, ROIMFIList, ROIPercAreaList = MFI_PerctArea(df = Resultsdf, images = oriImg,UserROIs = UserROIs)


		if not os.path.exists(UpdateResultSave) or overwriteProcessing or overwrite:			
			#Define which cell types too look at for this analysis
			cell_types_to_analyze = setup['cell_types_to_analyze']
			#Define cell types. Channel names must match those defined in namChannel exactly.
			#1 indicates positive, 0 indictes negative
			cell_type_conditions = {
			'DAPI' : [['DAPI_ch', 1]],

			'CC1+' : [['DAPI_ch', 1],['CC1', 1]],

			'OligoLineage' : [['DAPI_ch', 1], ['Olig2', 1]],

			'OligoLineageRS' : [['DAPI_ch', 1], ['Olig2RS', 1]],

			'OPC' : [['DAPI_ch', 1], ['CC1', 0], ['Olig2', 1]],

			'OPCRS' : [['DAPI_ch', 1], ['PLP', 0], ['Olig2RS', 1]],
					
			'Mature Oligodendrocyte' : [['DAPI_ch', 1], ['CC1', 1], ['Olig2', 1]],

			'PLP Mature Oligodendrocyte' : [['DAPI_ch', 1], ['PLP', 1]],

			'CC1+' : [['DAPI_ch', 1], ['CC1', 1]],

			'NonOligo' : [['DAPI_ch', 1], ['Olig2', 0]],

			'Sox2Astro' : [['DAPI_ch', 1], ['Olig2', 0], ['Sox2', 1]],

			'ProlifNonOligo' : [['DAPI_ch', 1], ['Olig2', 0], ['Ki67', 1]],

			'CC1+Olig2-' : [['DAPI_ch', 1], ['CC1', 1], ['Olig2', 0]],

			'ActiveOPC' : [['DAPI_ch', 1], ['Olig2', 1], ['Sox2', 1]],

			'ProlifOPC' : [['DAPI_ch', 1], ['Olig2', 1], ['Ki67', 1]],

			'Activated-ProliferativeOPCs' : [['DAPI_ch', 1], ['Olig2', 1],['Sox2', 1], ['Ki67', 1]],

			'Human Cell' : [['DAPI_ch', 1], ['hNA', 1]],

			'Myelinating Human Cell' : [['DAPI_ch', 1], ['hNA', 1], ['MBP', 1]],

			'Alive' : [['DAPI_ch', 1], ['Phase', 1]],

			'Dead' : [['DAPI_ch', 1], ['Phase', 0]],

			'EGFP Tagged' : [['DAPI_ch', 1], ['Phase', 1], ['EGFP', 1]],

			'mCherry Tagged' : [['DAPI_ch', 1], ['H2B-mCherry', 1]],

			'O4_GFAP' : [['DAPI_ch', 1], ['O4_GFAPCh', 1]],

			'EDU+' : [['DAPI_ch', 1], ['EDU', 1]],

			'EDU+Olig2-' : [['DAPI_ch', 1], ['EDU', 1], ['Olig2', 0]],

			'EDU+Olig2+' : [['DAPI_ch', 1], ['EDU', 1], ['Olig2', 1]],
			}

			
			Summary = ProcessRawResults(df = Resultsdf, Summary=Summary, cell_type_conditions=cell_type_conditions, cell_types_to_analyze=cell_types_to_analyze)
			

			if debugCellLocations:

				Vischannels =[]
				
				for i in range(len(namChannels)):
					oriImg = cv.imreadmulti(fullpath, flags = -1)
					Img = gammaCorrect(oriImg[1][i], gamma = gammas[i])
					Img = proccessVisualImage(Img)
					Vischannels.append(Img)
				Vischannels = np.array(Vischannels)

				FigureSavePath = os.path.join(SpecificImgFolder, "Cell_Identification.pdf")
				showCentroids(images = Vischannels, path = FigureSavePath, df = Resultsdf, titles = namChannels, save = 0)
			
		#clear Resultsdf
		Resultsdf = pd.DataFrame()

Summarydf = pd.DataFrame(Summary)

Summarydf.to_csv(SummarySave, index=False)

print("All Done!")
