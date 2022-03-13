import cv2 as cv
import sys

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
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
from io import BytesIO
import pandas as pd
import random
from scipy.stats import gaussian_kde
from scipy import stats
import csv
import tkinter as tk
import ctypes
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
screensize = [width, height]	

from settings import Settings
import tifffile as tiff

settings = Settings()
def saveCentroids(images, df, titles='', path = ' ', text_coords = []):
	"""Show centroids side-by-side with image."""

	celltypes = plotcelltypes
	sizeh = images.shape[1]
	sizew = images.shape[2]

	dpiscale = 1000
	scaleh = sizeh/dpiscale
	scalew = sizew/dpiscale

	colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
	
	dotsize = 0.5

	for j in range(len(celltypes)):
		fig = plt.figure(frameon=False, figsize=(scalew, scaleh), dpi=100)
		ax = plt.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)

		img = np.zeros((sizeh, sizew), np.uint8)
		ax.imshow(img, aspect='auto')
		celltype = celltypes[j]
		color = colors[j]
		celltypedf = df.loc[df[celltype] == 1]
		centroids_x = celltypedf['X']
		centroids_y = celltypedf['Y']
		ax.scatter(centroids_x,centroids_y, s=dotsize,c=color)
	
		if not len(text_coords) == 0:
			for i in range(len(text_coords)):
				if i > 0:
					x = text_coords[i][0]
					y = text_coords[i][1]
					s = str(i)
					plt.text(x, y, s, fontsize=12)
		#fig.savefig(fname, dpiscale)
		# Save the image in memory in PNG format
		png1 = BytesIO()
		fig.savefig(png1, format="png", dpi = dpiscale)

		# Load this image into PIL
		png2 = Image.open(png1)

		# Save as TIFF
		FigureSavePath = os.path.join(path, "Cell type location "+str(celltype)+" .tiff")
		png2.save(FigureSavePath)
		png1.close()

def showCentroids(images, df, titles='', save = 0, path = ' ', text_coords = []):
	"""Show centroids side-by-side with image."""

	celltypes = plotcelltypes
	
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
			for j in range(len(celltype)):
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
	plt.show()
	plt.close('all')


def proccessVisualImage(img):
    """Function to proccess a flourescence image with nuclear localized signal (e.g. DAPI)."""
    # normalize (stretch histogram and convert to 8-bit)

    img = cv.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    img = np.uint8(img)
    # invert image 
    # FUTURE: consider other normalization strategies
    
    #img = cv.bitwise_not(img)
    return img

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

'____________________________________________________________________________________'
setup = settings.folder_dicts[21]
#List of images you want to see, file names in he specified path
Images = ['RB47 S39 DCO LH 2_current_13600.tif',
		 ]
plotcelltypes = ['DAPI','OPC','Mature Oligodendrocyte']
#https://www.infobyip.com/detectmonitordpi.php
#my_dpi = [144,144]
my_dpi = [192,192]

'____________________________________________________________________________________'

RabbitDescriptions = settings.RabbitDescriptions
Dataname = setup['name']


ROI_Draw_Channel = setup['ROI_Draw_Channel']
Nuclei_Identification_Channel = setup['Nuclei_Identification_Channel']

#What are the channels?
namChannels = setup['channels']
Relthreshs = setup['RelativeIntensityThreshold']

#What cell types are you looking to analyze?
cell_types_to_analyze = setup['cell_types_to_analyze']

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

ImgFolderPath = setup['Path']

ResultsFolderPath = os.path.join(ImgFolderPath,"Results")
if not os.path.exists(ResultsFolderPath):
	os.mkdir(ResultsFolderPath)

SummarySave = os.path.join(ResultsFolderPath, Dataname + '_Summary.csv')

SpecificImgResultsPath = os.path.join(ResultsFolderPath,"Image_Specific_Results")
if not os.path.exists(SpecificImgResultsPath):
	os.mkdir(SpecificImgResultsPath)

for oriImgName in os.listdir(ImgFolderPath):
	fullpath = os.path.join(ImgFolderPath, oriImgName)
	if oriImgName in Images:
		if oriImgName.endswith('.tif'):
			SpecificImgFolder = os.path.join(SpecificImgResultsPath, oriImgName[:-4] + " Results")
			if not os.path.exists(SpecificImgFolder):
				os.mkdir(SpecificImgFolder)

			SampleCellsFolder = os.path.join(SpecificImgFolder,"Sample_Cells")
			if not os.path.exists(SampleCellsFolder):
				os.mkdir(SampleCellsFolder)

			ImageResultsSave = os.path.join(SpecificImgFolder, "ImageCellSpecificResultsUpdate.csv")
			print(" ")
			print("Image --> " + oriImgName)

			oriImg = cv.imreadmulti(fullpath, flags = -1)
			oriImg = oriImg[1]
			oriImg = np.array(oriImg)

			
			oriImg = cv.imreadmulti(fullpath, flags = -1)
			Vischannels =[]
			for i in range(len(namChannels)):
				Img = gammaCorrect(oriImg[1][i], gamma = gammas[i])
				Img = proccessVisualImage(Img)
				Vischannels.append(Img)
			Vischannels = np.array(Vischannels)
			Resultsdf = pd.read_csv(ImageResultsSave)

			#FigureSavePath = os.path.join(SpecificImgFolder, "Cell_Identification.pdf")
			#showCentroids(images = Vischannels, df = Resultsdf, titles = namChannels, save = 0)
			saveCentroids(images = Vischannels, path = SpecificImgFolder, df = Resultsdf, titles = namChannels)

