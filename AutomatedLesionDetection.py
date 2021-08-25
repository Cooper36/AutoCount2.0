def LesionIdenification( OriginalImg, cells, windowsize, threshold = 0, ):
	#windowsize needs to be odd (75,75 seemed best)
	#make a binary image the same size and oriImg, where cell centroid locations are marked with a 1
	#then that imaged is "scanned" at window sized chuncs where density is calculated for each window

	windowArea = ((windowsize[0]/scale) * (windowsize[1]/scale))/1000000
	densities = []
	centers_x = []
	centers_y = []
	shape = OriginalImg.shape
	width = shape[1]
	height = shape[0]
	cellLocImg = np.zeros((height,width), dtype=int)
	
	for cell in cells:
		centroid_x = round(cell['centroids'][0])
		centroid_y = round(cell['centroids'][1])

		cellLocImg[centroid_y,centroid_x] = 1

	
	fitCol = math.floor(width/windowsize[0])
	fitRow = math.floor(height/windowsize[1])

	numWindows = fitCol * fitRow

	remainCol = width - (fitCol * windowsize[0])
	shiftCol = math.floor(remainCol/2)

	remainRow = height - (fitRow * windowsize[1])
	shiftRow = math.floor(remainRow/2)

	row = 0
	col = 0
	#go over the image and get the number of cells in the window (size of which is set when called)
	densities = []
	densityImg = np.zeros((fitRow,fitCol), dtype=int)
	p=0
	c=0
	
	for y in range(fitRow):
		y_min = ((y * windowsize[1]) + shiftRow)
		y_max = ((y * windowsize[1]) + windowsize[1] + shiftRow)		
		for j in range(fitCol):
			x_min = ((j * windowsize[0]) + shiftCol)
			x_max = ((j * windowsize[0]) + windowsize[0] + shiftCol)
			
			window = cellLocImg[y_min:y_max,x_min:x_max]
			
			center_x = (x_min + math.ceil(windowsize[0]/2))
			center_y = (y_min + math.ceil(windowsize[1]/2))

			#centers_x.append(center_x)
			#centers_y.append(center_y)
			#make this a scaled density, modify windowArea
			windowDensity = np.sum(window)/windowArea
			#list of non-Zero densities
			if windowDensity > 0:
				densities.append(windowDensity)
			#making density map
			densityImg[y, j] = windowDensity
			if p == 50:
				value = (c/numWindows)*100
				formatted_string = "{:.2f}".format(value)
				float_value = float(formatted_string)
				p=0
				c= c+1
			else:
				p=p+1
				c=c+1
				
				#print("densityImg = ", sys.getsizeof(densityImg))
	"""
	print("          Make and fill in the density map")
	densityImg = np.zeros((fitRow,fitCol), dtype=int)
	for density in densities:
		densityImg[density[0][1], density[0][0]] = density[2]
	"""
	#FigureSavePath = os.path.join(SpecificImgFolder, "Lesion_Density_Visualization.pdf")
	#showDensities(OriginalImg, densities, save = 1, path = FigureSavePath)
	
	if not threshold > 0:
		median = np.median(densities)
		std = np.std(densities)
		threshold = median 
	

	#identify peaks
	binarr = np.where(densityImg>threshold, 255, 0)
	#print(binarr.dtype, binarr.shape)
	binarr = np.uint8(binarr)
	#print(binarr.dtype, binarr.shape)
	#get rid of narrow peaks
	kernel = np.ones((3,3),np.uint8)
	binarr = cv.morphologyEx(binarr, cv.MORPH_OPEN, kernel,iterations=1)
	#Smooth binary image
	#CAN ADD REGION/EDGE DETECTION IN THIS SECTION
	
	binarrBlur = cv.GaussianBlur(binarr,(5,5),cv.BORDER_DEFAULT)
	ret,binarrBlur = cv.threshold(binarrBlur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
	#binarrBlur = cv.erode(binarrBlur,kernel,iterations = 2)
	#binarrBlur = cv.dilate(binarrBlur,kernel,iterations = 2)
	binarrBlur = np.uint8(binarrBlur)
	#NOW TAKE THE NEW BINARY IMAGE AND MAKE THAT INTO A MASK TO GET THE LESION BOUNDARY

	Lbinarr = np.zeros((height,width), dtype=int)
	for i in range(len(binarr)):
		for y in range(fitRow):
			y_min = ((y * windowsize[1]) + shiftRow)
			y_max = ((y * windowsize[1]) + windowsize[1] + shiftRow)		
			for j in range(fitCol):
				x_min = ((j * windowsize[0]) + shiftCol)
				x_max = ((j * windowsize[0]) + windowsize[0] + shiftCol)
				
				Lbinarr[y_min:y_max,x_min:x_max] = binarrBlur[y,j] #np.broadcast_to(binarr[y,j], windowsize)

	#smooth binary image so its not so jagged
	Lbinarr = np.uint8(Lbinarr)

	
	contours, hierarchy = cv.findContours(Lbinarr, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cv.drawContours(OriginalImg, contours, -1, (0,0,255), 6)
	#print(Lbinarr.shape)
	images = [ Lbinarr, OriginalImg]
	titles = ["Mask","Boarder" ]
	
	output = cv.connectedComponentsWithStats(Lbinarr)
	(numLabels, labels, stats, centroids) = output
	
	FigureSavePath = os.path.join(SpecificImgFolder, "Lesion_Boarder_Visualization.pdf")
	showImages(images, titles, save = 1, path = FigureSavePath, text_coords = centroids)

	return output