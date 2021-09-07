"""import numpy as np
import sys
import cv2 as cv
import math
length = [0] * 8
np.set_printoptions(threshold=sys.maxsize, linewidth = 9999)

UserROIs = np.zeros((20,20))
points = [(1,1),(1,4),(4,4),(4,1)]
cv.fillPoly(UserROIs, np.array([points]), 2)

points = [(19,1),(16,1),(16,8),(19,8)]
cv.fillPoly(UserROIs, np.array([points]), 1)

ret, Thresh1 = cv.threshold(UserROIs, 0, 255, cv.THRESH_BINARY)

Thresh1 = np.uint8(Thresh1)
output = cv.connectedComponentsWithStats(Thresh1)
cv.imshow("winname", Thresh1)
cv.waitKey()

def Reorder(UserROIs,output):
	(numLabels, labelsUserROI, stats, centroids) = output
	reorderstats = [[0,0,0,0,0]] * numLabels
	reordercentroids = [[0,0]] * numLabels
	for i in range(numLabels):
		if i > 0:
			ix = int(math.floor(centroids[i][0]))
			iy = int(math.floor(centroids[i][1]))
			for j in range(numLabels):
				if j > 0:
					jx = int(math.floor(centroids[j][0]))
					jy = int(math.floor(centroids[j][1]))
					if UserROIs[iy,ix] == labelsUserROI[jy,jx]:
						val = int(UserROIs[iy,ix])
						reorderstats[val] = stats[i]
						reordercentroids[val] = centroids[i]
	reordercentroids = np.array(reordercentroids)
	reorderstats = np.array(reorderstats)

	return reordercentroids, reorderstats

reordercentroids, reorderstats = Reorder(UserROIs,output)
centroids = output[3]
stats = output[2]
print(centroids)

print(reordercentroids)

print(" ")

print(stats)

print(reorderstats)
"""
"""___________________________________________________________________________________________________________________________________________________________"""


import keras

