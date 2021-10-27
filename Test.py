import numpy as np
import sys
import cv2 as cv
import math
"""
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

"""
import csv

with open('test.csv') as f:
    Summary = [{k : v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

print(a)

"""
"""
def showCentroids(images, df, titles='', save = 0, path = ' ', text_coords = []):
    Show centroids side-by-side with image.
    plt.subplot(1,2,1),plt.imshow(img,'gray')
    plt.subplot(1,2,2),plt.scatter(centroids_x,-centroids_y)
    plt.show()
    celltypes = set(df['Cell_Type'].values)
    for celltype in celltypes:
    	celltypedf = df.loc[df['Cell_Type'] == cell_type]
    	centroids_x = celltypedf['X']
    	centroids_y = celltypedf['Y']

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
			ax.scatter(centroids_x,centroids_y, s=1,c="red")
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



showCentroids(images)
"""

"""import tkinter as tk

root = tk.Tk()

v = tk.IntVar()
v.set(1)  # initializing the choice, i.e. Python

languages = [("Yes, Skip", True),("No, Don't Skip", False)]

def ShowChoice():
	if v.get():
		print("ROI skipped")
	root.destroy()

tk.Label(root, 
		
		justify = tk.LEFT,
		padx = 20).pack()

for language, val in languages:
	tk.Radiobutton(root, 
		text=language,
		indicatoron = 0,
		width = 20,
		padx = 20, 
		variable=v, 
		command=ShowChoice,
		value=val).pack(anchor=tk.W)


root.mainloop()
done = v.get()
print(done)"""


y = np.ones((5,5))
y = y + 1
print(y)
