#Put all 10x images that you want counted into a single folder 
#All images in the folder need to have the same number and order of stained Vischannels
import cv2 as cv
import sys

import numpy as np 
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
import math
import os, errno
from pathlib import Path

# to enable VSI file support
#import javabridge
#import bioformats
from PIL import Image 
import PIL 
import imageio
import pandas as pd
import random
from scipy.stats import gaussian_kde
from keras.models import load_model

def openVSI(fullpath):
    images = bioformats.load_image(fullpath, rescale=False)
    images = cv.split(images)

    return images

def imageThreshold(img,):

    """IMAGE THRESHOLDING."""
    # based on - https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html

    #img = cv.medianBlur(img,5)
    img_blur = cv.GaussianBlur(img,(5,5),0)

    #ret,th1 = cv.threshold(img_blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    th2 = cv.adaptiveThreshold(img_blur,255,cv.ADAPTIVE_THRESH_MEAN_C,
        cv.THRESH_BINARY,11,2)
    #th3 = cv.adaptiveThreshold(img_blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        #cv.THRESH_BINARY,11,2)
    titles = ['Original Image (Blur)', 'Global Otsu Thresholding',
        'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    #images = [img_blur, th1, th2, th3]

    if debug:
        showImages(images, titles)

    return cv.bitwise_not(th2)

def proccessNuclearImage(img):
    """Function to proccess a flourescence image with nuclear localized signal (e.g. DAPI)."""
    # normalize (stretch histogram and convert to 8-bit)
    img = cv.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    # invert image 
    img = cv.bitwise_not(img)
    # FUTURE: consider other normalization strategies
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
def thresholdSegmentation( 
    thresh, 
    img, 
    opening_kernel = np.ones((3,3),np.uint8),
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

    # img = self.proccessNuclearImage(self.images[channel])
    #img = cv.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    markers = cv.watershed(img,markers)

    img[markers == -1] = [255,0,0]

    titles = ['threshold', 'opening', 'dist_transform', 'sure_fg', 'unknown', 'watershed']
    images = [thresh, opening, dist_transform, sure_fg, unknown, img]
    
    if debugThreshold or debug:
        showImages(images, titles)

    count = markers.max()-1
    output = cv.connectedComponentsWithStats(sure_fg)

    return([count, output, sure_fg, img, markers])
# other functions of potential interest - findContours
# NEXT FILTER ON SIZE, CIRCULARITY - GET X-Y centroid
# https://www.learnopencv.com/blob-detection-using-opencv-python-c/ - for circularity

def showCentroids(img,centroids_x,centroids_y):
    """Show centroids side-by-side with image."""
    """plt.subplot(1,2,1),plt.imshow(img,'gray')
    plt.subplot(1,2,2),plt.scatter(centroids_x,-centroids_y)
    plt.show()"""

    implot = plt.imshow(img,'gray')
    plt.scatter(centroids_x,centroids_y, s=1,c="red")
    plt.show()

def getCells(Vischannels, Rawchannels, centroids, markers):
	"""Returns the image of each cell, and builds cells as a dictionary"""
	for i in range(len(centroids)):
	#print(type(channels))
	#for i in range(100):
		Viscellimg = []
		Rawcellimg = []
		X = centroids[i][0]
		Y = centroids[i][1]
		#print(X,Y)
		shape = Vischannels[0].shape
		width = shape[1]
		height = shape[0]

		x_min = math.ceil((X - cropsize/2).astype(int))
		x_max = math.ceil((X + cropsize/2).astype(int))
		y_min = math.ceil((Y - cropsize/2).astype(int))
		y_max = math.ceil((Y + cropsize/2).astype(int))
		#print(x_min,x_max,y_min,y_max)
		#if x_min < 0 or x_max < 0 or y_min < 0 or y_max < 0:
		if x_min < 0 or x_max > width or y_min < 0 or y_max > height:
			for y in range(len(namChannels)):
				blank = np.zeros((cropsize,cropsize,1), np.uint8)
				Viscellimg.append(blank)
			#print("exclude")
			skipped = "Yes"
		else:
			for y in range(len(namChannels)):
				Visstain = Vischannels[y][y_min:y_max,x_min:x_max]
				Rawstain = Rawchannels[y][y_min:y_max,x_min:x_max]
				cellMarkers = markers[y_min:y_max,x_min:x_max]

				Visstain = cv.bitwise_not(Visstain)
				Viscellimg.append(Visstain)
				Rawcellimg.append(Rawstain)
				skipped = "No"


		
		filename = 'Cell ID ' + str(i) + '.tif'
		savepa = os.path.join(SampleCellsFolder,filename)
		Viscellimg = np.array(Viscellimg)
		Rawcellimg = np.array(Rawcellimg)
		
		#Uncomment this to save ALL cell images
		#imageio.mimwrite(savepa,cellimg)


		cell =  {
				'oriImgName' : oriImgName,
				'CellID' :  str(i),
				'centroids' : centroids[i], 
				'cellimg' : [Rawcellimg,Viscellimg],
				'cellMarkers': cellMarkers, 
				'skipped' : skipped
				}

		#print("include")
		cells.append(cell)

	return cells

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
	for randcellID in randomlist:
		filename = cells[randcellID]['CellID'] + '.tif'
		savepa = os.path.join(path,filename)
		cellimg = np.array(cells[randcellID]['cellimg'][1])
		imageio.mimwrite(savepa,cellimg)

def AddStats(cells, labels, AreaStats):
	#isolate the pixels of the nuclei and bakground regions using masking, the report area and intensity data for each channel
	AreaStatsPix = AreaStats[:,4]
	AreaStatsmm2 = []
	np.array(AreaStats)
	for area in AreaStatsPix:
		AreaStatsmm2.append((area/(scale**2))/1000000)




	for cell in cells:
		skipped = cell['skipped']
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


				#Alternative masking method
				""" 
				src = channel
				mask = centMarker/1
				print(mask.dtype, mask.min(), mask.max())
				dst = src * mask
				nucleiCent = dst.astype(np.uint8)
				
				print(channel)
				print(" ")
				print(otherMarker)
				print(" ")
				"""

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
							'Areas_info' : AreaStatsmm2
							}

		cell['stats'] = stats
		cell['location'] = location

	return cells

def MacLearnImgPrepper(cells):
	#Takes the cell image and makes an RGB with blue being dapi and green and red being one of the channels
	for cell in cells:
		skipped = cell['skipped']
		img = cell['cellimg'][1]
		#print(img.shape)
		DAPI_ch = img[0]
		RGBs = {}
		if skipped == "No":
			i = 1
			for i in range(len(namChannels)):
				if i > 0:
					

					blue = DAPI_ch
					green = img[i]
					red = img[i]
					rgb = []
					rgb.append(cv.merge((blue,green,red)))
					

					if debugImgPrepper or debug:
						print(i)
						print(rgb[0].shape)
						print(rgb[0])
						cv.imshow("sfsf", rgb[0])
						cv.waitKey(0)

					RGBs[namChannels[i]] = rgb

		cell['RGBs'] = RGBs

	return cells

def LesionIdenification(DAPIImg,UserROIs):
	UserROIs = cv.cvtColor(UserROIs, cv.COLOR_BGR2GRAY)
	contours, hierarchy = cv.findContours(UserROIs, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cv.drawContours(DAPIImg, contours, -1, (0,0,255), 6)
	#print(Lbinarr.shape)
	images = [ UserROIs, DAPIImg]
	titles = ["Mask","Boarder" ]
	
	output = cv.connectedComponentsWithStats(UserROIs)
	(numLabels, labels, stats, centroids) = output
	
	FigureSavePath = os.path.join(SpecificImgFolder, "Lesion_Boarder_Visualization.pdf")
	showImages(images, titles, save = 1, path = FigureSavePath, text_coords = centroids)

	return output

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

def PlotHistogram(data):
	# Creating histogram
	fig, ax = plt.subplots(figsize =(10, 7))
	ax.hist(data, bins = 20)
	 
	# Show plot
	plt.show()

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
				print("          Keras ",float_value, " % complete")
				p=0
				c= c+1
			else:
				p=p+1
				c=c+1
			for i in range(len(namChannels)):
				if i > 0:
					img = cell['RGBs'][namChannels[i]][0]
					img = img.astype('float64')
					img = np.expand_dims(img, axis=0)

					#Comment these out to make the code go faster when debugging
					predict = model.predict(img)
					predict = predict[0][0]
					#predict = 0
					cell['RGBs'][namChannels[i]].append(predict)
		
	return cells

def Cells_to_df(cells):
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
	for i in range(numLabels):
		if i == 0:
			LesAreaNam = "Background Area (mm^2)"
		else :
			LesAreaNam = "Lesion " + str(i) + " Area (mm^2)"
		
		LesTitles.append(LesAreaNam)
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
			for i in range(numLabels):
				areaPix = cell['location']['Areas_info'][i]
				cellAnno.append(areaPix)

			cellsAnno.append(cellAnno)


	#might need to fill empty spaces with 0's here
	
	df = pd.DataFrame(data=cellsAnno, columns=columnTitles)

	return df

def ProcessRawResults(df, Summary, cell_type_conditions, cell_types_to_analyze):
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
		sizeThresh = [10,250]
		df["SizeThreshed"] = np.where((df[AreaColumnTitle] > sizeThresh[0]) & (df[AreaColumnTitle] < sizeThresh[1]), 1, 0)

		IntensMean = np.mean(df[IntensColumnTitle])
		IntensStd = np.std(df[IntensColumnTitle])		
		IntensThresh = IntensMean + (0.25*IntensStd)
		IntensThreshedTitle = ch + " IntensThreshed"
		df[IntensThreshedTitle] = np.where((df[IntensColumnTitle] >= IntensThresh), 1, 0)

		#based on bkg mean intensity
		MeanThresh = np.mean(df[bkgMeanTitle]) + (0.5 * np.std(df[bkgMeanTitle]))
		MeanThreshedTitle = ch + " MeanThreshed"
		df[MeanThreshedTitle] = np.where((df[MeanNewcolumnTitle] >= MeanThresh), 1, 0)

		#assuming most will be about 1
		RelMean = np.mean(df[RelNewcolumnTitle])
		RelStd = np.std(df[RelNewcolumnTitle])		
		RelIntensThresh = RelMean + (0.25*RelStd)
		RelThreshedTitle = ch + " RelThreshed"
		df[RelThreshedTitle] = np.where((df[RelNewcolumnTitle] >= RelIntensThresh), 1, 0)

		if i > 0:
			MacLearnThreshedTitle = ch + " MacLearnThreshed"
			df[MacLearnThreshedTitle] = np.where((df[MacLearnPredTitle] >= 0.5), 1, 0)


		#Identify different types of positivity
		# 1 means just maclearn predicted
		# 2 means predicted positive in the traditional sense
		# 3 both maclearn and traditional positive

		Postivity_RankTitle = ch + " Postivity_Rank"
		if i == 0:
			df[Postivity_RankTitle] = np.where((df[IntensColumnTitle] > 0), 1, 0)
		else:
			df[Postivity_RankTitle] = 0
			df[Postivity_RankTitle] = np.where((df[MacLearnThreshedTitle] == 1), 1, df[Postivity_RankTitle])
			df[Postivity_RankTitle] = np.where((df[MacLearnThreshedTitle] == 0) & (df["SizeThreshed"] == 1) & (df[RelThreshedTitle] == 1) & (df[MeanThreshedTitle] == 1), 1, df[Postivity_RankTitle])
			df[Postivity_RankTitle] = np.where((df[MacLearnThreshedTitle] == 1) & (df["SizeThreshed"] == 1) & (df[RelThreshedTitle] == 1) & (df[MeanThreshedTitle] == 1), 1, df[Postivity_RankTitle])
	

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
		plt.savefig(FigureSavePath)
		if debugProcessRawResults or debug:
			plt.show()
		plt.close(fig)
	

	#Visual Validation? Need to load cells

	#Define positive cell types
	df['Cell_Type'] = "Not Classified"
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

		df['Cell_Type'] = np.where(callapsedConditions,celltypename, df['Cell_Type'])

	df.to_csv(UpdateResultSave, index = False)

		






				
class PolygonDrawer(object):
	def __init__(self, window_name, img, ROINumber):
		self.window_name = window_name # Name for our window
		self.img = img
		self.imgheight, self.imgwidth = self.img.shape[0:2]
		
		self.smallwidth = 800
		self.smallheight = int(self.smallwidth*(self.imgheight/self.imgwidth))
		self.smallImg = cv.resize(self.img, (self.smallwidth,self.smallheight))

		self.done = False # Flag signalling we're done with one polygon
		self.doneAll = False # Flag signalling we're done with all polygons

		self.current = (0, 0) # Current position, so we can draw the line-in-progress
		self.points = [] # List of points defining our polygon
		self.polygons = [] # List of all polygons
		self.FINAL_LINE_COLOR = (255, 255, 255)
		self.WORKING_LINE_COLOR = (127, 127, 127)


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
			self.points.append((x, y))

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
			while(not self.done):
				# This is our drawing loop, we just continuously draw new images
				# and show them in the named window
				canvas = np.copy(Polycanvas, subok= True)
				if (len(self.points) > 0):
					# Draw all the current polygon segments
					cv.polylines(canvas, np.array([self.points]), False, self.FINAL_LINE_COLOR, 1)
					# And  also show what the current segment would look like
					cv.line(canvas, self.points[-1], self.current, self.WORKING_LINE_COLOR)
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

			self.polygons.append(self.points)
			self.points = []

			# Waiting for the user to press any key
			i = i+1


		cv.destroyWindow(self.window_name)
		bincanvas = np.zeros((self.smallheight,self.smallwidth), dtype= np.uint8)
		for polygon in self.polygons:
			polygon = np.array([polygon])
			cv.fillPoly(bincanvas, polygon, self.FINAL_LINE_COLOR)
		bincanvas = cv.resize(bincanvas, (self.imgwidth, self.imgheight))
		return bincanvas

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
#Average scale for 10x images, pixel/micron
scale = 1.5385


#Path to image folder
#ImgFolderPath = "/Users/james/Desktop/Working Folder/AutoCount2.0"
ImgFolderPath ="C:\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0"
#What are the channels?
namChannels = ["DAPI_ch","CC1","594_ch","Olig2"]

#What cell types are you looking to analyze?
#cell_types_to_analyze = ['OPC', 'Oligo', 'NonOligo']

#Desired cell image size
cropsize = 46

#How many ROIs do you want to define?
ROINumber = 2


overwrite = False
overwriteCells_Pred = False
overwriteROIS = False
overwriteProcessing = True

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

#Make Summary and  AllCellSpecificResults list of dictionaries
Summary = {}

AllCellSpecificResults = pd.DataFrame()
Resultsdf = pd.DataFrame()
#Make the appropriate folder structure
ResultsFolderPath = os.path.join(ImgFolderPath,"Results")
if not os.path.exists(ResultsFolderPath):
	os.mkdir(ResultsFolderPath)

SpecificImgResultsPath = os.path.join(ResultsFolderPath,"Image_Specific_Results")
if not os.path.exists(SpecificImgResultsPath):
	os.mkdir(SpecificImgResultsPath)

AllresultsSave = os.path.join(ResultsFolderPath, "AllCellSpecificResultsGood.csv")

#Build the appropriate image-specific structures and User Defined ROIs
#https://stackoverflow.com/questions/37099262/drawing-filled-polygon-using-mouse-events-in-open-cv-using-python
ImageID = 0
TotalImage = 0
for oriImgName in os.listdir(ImgFolderPath):
	fullpath = os.path.join(ImgFolderPath, oriImgName)
	if oriImgName.endswith('.tif'):

		SpecificImgFolder = os.path.join(SpecificImgResultsPath, oriImgName[:-4] + " Results")
		if not os.path.exists(SpecificImgFolder):
			os.mkdir(SpecificImgFolder)

		SampleCellsFolder = os.path.join(SpecificImgFolder,"Sample_Cells")
		if not os.path.exists(SampleCellsFolder):
			os.mkdir(SampleCellsFolder)

		BinarySave = os.path.join(SpecificImgFolder, "UserDefinedROIs.tif")
		if not os.path.exists(BinarySave) or overwriteROIS or overwrite:
			img = cv.imreadmulti(fullpath, flags = -1)
			Dapi = proccessNuclearImage(img[1][0])
			gamma = 0.35
			Dapi = adjust_gamma(Dapi, gamma)
			Dapi = cv.bitwise_not(Dapi)
			Dapi = np.array(Dapi)
			windowname = str(oriImgName) +" : Draw " + str(ROINumber) + " ROIs"
			polyDr = PolygonDrawer(windowname, Dapi, ROINumber)
			Lbinarr = polyDr.run()
			
			cv.imwrite(BinarySave,Lbinarr)
		TotalImage = TotalImage + 1




#Main For Loop
for oriImgName in os.listdir(ImgFolderPath):
	fullpath = os.path.join(ImgFolderPath, oriImgName)
	
	if oriImgName.endswith('.tif'):
		SpecificImgFolder = os.path.join(SpecificImgResultsPath, oriImgName[:-4] + " Results")
		if not os.path.exists(SpecificImgFolder):
			os.mkdir(SpecificImgFolder)

		SampleCellsFolder = os.path.join(SpecificImgFolder,"Sample_Cells")
		if not os.path.exists(SampleCellsFolder):
			os.mkdir(SampleCellsFolder)

		ImageResultsSave = os.path.join(SpecificImgFolder, "ImageCellSpecificResults.csv")
		
		if not os.path.exists(ImageResultsSave) or overwriteCells_Pred or overwrite:
			
			ImageID = ImageID+1
			#Additional folder structures

			print("Image ",ImageID, " of ", TotalImage,": Reading Image ")
			oriImg = cv.imreadmulti(fullpath, flags = -1)

			print("Image ",ImageID, " of ", TotalImage,": Processing Image ")
			Vischannels =[]
			for i in range(len(namChannels)):
				Img = proccessNuclearImage(oriImg[1][i])
				gamma = 0.35
				Img = adjust_gamma(Img, gamma)
				Vischannels.append(Img)
			Vischannels = np.array(Vischannels)

			Rawchannels = []
			for i in range(len(namChannels)):
				Img = oriImg[1][i]
				Rawchannels.append(Img)
			Rawchannels = np.array(Rawchannels)

			if debugGamma or debug:
				Titles = ["Dapi", "ch1", "ch2", "ch3"]
				showImages(Vischannels,Titles)

			print("Image ",ImageID, " of ", TotalImage,": Thresholding and Segmenting Image ")
			new = imageThreshold(Vischannels[0])
			output = thresholdSegmentation(new, Vischannels[0])
			centroids = output[1][3]
			markers = output[4]


			if debugMarkers or debug:
				print(Vischannels.shape)
				print(markers.shape)
				print(markers)
				#cv.imshow(markers)
				#cv.waitKey(0)
			
			
			if debugChannels or debug:
				Titles = ["Dapi", "ch1", "ch2", "ch3", "markers"]
				showImages(Vischannels,Titles)

			centroids_x = []
			centroids_y = []

			for i in range(len(centroids)):
				centroids_x.append(centroids[i][0])
				centroids_y.append(centroids[i][1])

			centroids_x = np.array(centroids_x)
			centroids_y = np.array(centroids_y)
			
			if debug:
				showCentroids(Vischannels[0],centroids_x,centroids_y)

			print("Image ",ImageID, " of ", TotalImage,": Getting Cell Images and making cells")
			cells = []
			cells = getCells(Vischannels, Rawchannels, centroids, markers)

			print("Image ",ImageID, " of ", TotalImage,": Processing User ROIs")
			BinarySave = os.path.join(SpecificImgFolder, "UserDefinedROIs.tif")
			UserROIs = cv.imread(BinarySave)
			UserROIsOutput = LesionIdenification(DAPIImg=Vischannels[0],UserROIs = UserROIs )

			(numLabels, labelsUserROI, stats, centroids) = UserROIsOutput
			
			print("Image ",ImageID, " of ", TotalImage,": Measuring Pixel Intensity for Each Cell")
			cells = AddStats(cells, labelsUserROI, stats)

			print("Image ",ImageID, " of ", TotalImage,": Prepping Images for Keras")
			cells = MacLearnImgPrepper(cells)

			if debugcells or debug:
				for key in cells[3000]:
					print(cells[3000][key])
					print(" ")

			
			print("Image ",ImageID, " of ", TotalImage,": Begining Keras Analysis")
			model = loadKerasModel("C:\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0\\CC1counting_wMar_5.8.h5")
			cells = getPredictions(cells, model)
			print("End Keras")
			

			print("Image ",ImageID, " of ", TotalImage,": Saveing a Sample of the Cells for")
			#Uncomment this to save x number of random cells (for survaying)
			RandomSampler(cells, 100, SampleCellsFolder)

			print("Image ",ImageID, " of ", TotalImage,": Crafting the DataFrame and Saving the .csv file")
			#Build the Dataframe to analyse the data
			Resultsdf = Cells_to_df(cells)
	
			Resultsdf.to_csv(ImageResultsSave, index = False)

			#Get Summary data from Resultsdf for the lesions and save that to a persisting dataframe to construct the Summary.csv file
		
		#Shift to individual image analysis, as in just work with the current csv
		if Resultsdf.empty :
			Resultsdf = pd.read_csv(ImageResultsSave)	

		UpdateResultSave = os.path.join(SpecificImgFolder, "ImageCellSpecificResultsUpdate.csv")
		if not os.path.exists(UpdateResultSave) or overwriteProcessing or overwrite:
			#Define which cell types too look at for this analysis
			cell_types_to_analyze = ['OPC', 'Oligo', 'NonOligo']
			#Define cell types. Channel names must match those defined in namChannel exactly.
			#1 indicates positive, 0 indictes negative
			cell_type_conditions = {
			'OPC' : [['DAPI_ch', 1], ['CC1', 0], ['Olig2', 1]],
					
			'Oligo' : [['DAPI_ch', 1], ['CC1', 1], ['Olig2', 1]],

			'ActiveOPC' : [['DAPI_ch', 1], ['Olig2', 1], ['Sox2', 1]],

			'ProlifOligo' : [['DAPI_ch', 1], ['Olig2', 1], ['Ki67', 1]],

			'Sox2Astro' : [['DAPI_ch', 1], ['Olig2', 0], ['Sox2', 1]],

			'NonOligo' : [['DAPI_ch', 1], ['Olig2', 0]],

			}
			ProcessRawResults(df = Resultsdf, Summary=Summary, cell_type_conditions=cell_type_conditions, cell_types_to_analyze=cell_types_to_analyze)

print("All Done!")
