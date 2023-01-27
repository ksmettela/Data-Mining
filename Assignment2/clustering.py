import cv2
import numpy as np
import os
import shutil
import csv
from sklearn import cluster
import math

def find_edge_contour_call_fetchRect(fig_path,file_name):

	# Reading figure path
	fig = cv2.imread(os.path.join(fig_path,file_name))
	contour_fig = cv2.imread(os.path.join(fig_path,file_name))

	# Highlighting ths figure with appropriate color
	grey_clr=cv2.cvtColor(fig,cv2.COLOR_BGR2GRAY)
	clr_val = 255
	threshold_val=cv2.inRange(grey_clr,clr_val,clr_val)

	# Finding the edges to highlight
	found_edges = cv2.Canny(threshold_val, clr_val, clr_val)
	(contours_val, _) = cv2.findContours(found_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# Calling function to draw the rectangle
	fetch_rectangle_draw_cl(contours_val, file_name, fig_path)


def fetch_rectangle_draw_cl(contours_val,file_name,fig_path):
	# 
	pointer = 0

	# returning an image that is loaded from the file.
	fig = cv2.imread(os.path.join(fig_path,file_name))

	#Drawing an approximate rectangle around the binary image
	print("getting coordinates")
	x_cord1, y_cord1, b_wid1, b_hgt1 = cv2.boundingRect(contours_val[len(contours_val)-1])
	for i in range(1,len(contours_val)):
		x_cord2, y_cord2, b_wid1, b_hgt1 = cv2.boundingRect(contours_val[len(contours_val)-i-1])
		if(y_cord2 != y_cord1 and abs(y_cord2-y_cord1) > b_wid1):
			break

	for i in range(1,len(contours_val)):
		x_cord3, y_cord3, b_wid1, b_hgt1 = cv2.boundingRect(contours_val[len(contours_val)-i-1])
		if(x_cord3 != x_cord1 and abs(x_cord3-x_cord1) > b_hgt1):
			break
	
	# Slicing the figure according to the Clusters
	x_max1, y_max1, b_wid1, b_hgt1 = cv2.boundingRect(contours_val[-1])
	slic_wid_fig =  x_cord3-x_cord1
	slic_hgt_fig = y_cord2 - y_cord1
	fig = cv2.imread(os.path.join(fig_path,file_name))

	# Arriving at the exact coordinate of the contour values
	for i in range(0,len(contours_val)):
		x_cord1, y_cord1, b_wid1, b_hgt1 = cv2.boundingRect(contours_val[len(contours_val) - i-1])
		x_cord2 = x_cord1 + slic_wid_fig - b_wid1
		y_cord2 = y_cord1 - slic_hgt_fig
		x_cord1 = x_cord1 + b_wid1+b_wid1
		y_cord1 = y_cord1 + b_hgt1

		#checking if the coordinates are with in the limits
		if(x_cord1 < x_max1 or y_cord2 < y_max1):
			continue

		#Creating new figure based on grey portion, edges and threshold of given data
		new_fig = fig[y_cord2:y_cord1, x_cord1:x_cord2]	
		grey_clr=cv2.cvtColor(new_fig,cv2.COLOR_BGR2GRAY)

		#setting the threshold value
		clr_val1 = 25
		threshold_val=cv2.inRange(grey_clr,0,clr_val1)

		#finding the edges with the threshold value
		clr_val2 = clr_val1 + 25
		clr_val3 = clr_val2 + clr_val1 + 25

		found_edges = cv2.Canny(threshold_val, clr_val2, clr_val3)

		path_local = os.getcwd()

		# Inializing Contour values from the edges found, end points and extreme out flags
		(contour_val, _) = cv2.findContours(found_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if(len(contour_val)):
			print("Creating Sclies images")
			new_fig = fig[y_cord2:y_cord1, x_cord1:x_cord2]
			cv2.imwrite(os.path.join(os.path.join(path_local,"Slices"),file_name.split('.')[0])+'/'+str(pointer) +'.png', new_fig)
			
			#Calling clustering method to form clusters in the sliced images 
			collection_clustering(file_name, os.path.join(os.path.join(path_local,"Slices"),file_name.split('.')[0]),pointer,os.path.join(os.path.join(os.path.join(path_local,"Clusters"),file_name.split('.')[0]),file_name.split('.')[0]+str(".csv")))
			'''
			print("Creating Boundaries images")
			clr_val4 = 255
			print("Drawing contour line for boundaries images")
			cv2.drawContours(new_fig, contour_val, -1, (0,clr_val4,0), 1)
			cv2.imwrite(os.path.join(os.path.join(path_local,"Boundaries"),file_name.split('.')[0])+'/'+str(pointer) +'.png', new_fig)
			'''

		else:
			continue
		pointer = pointer + 1

def processing_dbscan(cords):
	#Implementing DBSCAN as a unsupervised clustering technique
	processing_cluster = cluster.DBSCAN(eps = math.sqrt(2), n_jobs=100).fit(cords)
	#finding out unique clusters in the cluster image
	_, sum = np.unique(processing_cluster.labels_[processing_cluster.labels_>=0], return_counts=True)
	#checking for the pixel image which has a higher threshold of 135 and return the number of clusters
	sums = 0
	for i in sum:
		if(i>135):
			sums = sums + 1
	return sums

def finding_cords(fig):
	#finding height and width from the figure using shape function
	hgt , wid = fig.shape
	cords_list = []
	#finding coordinates list with the help of width and height of clusters formed
	for i in range(hgt):
		for j in range(wid):
			if(fig[i,j]):
				cords_list.append([i,j])
	return cords_list

def collection_clustering(file_name, fig_path, pointer, csv_file):
	clr_val = 255
	blue = 204
	zero_val = 0
	# Initalizing current directory path to local path variable
	path_local = os.getcwd()
	#Reading the image from the image path, index location containg .png as an extention
	fig = cv2.imread(os.path.join(fig_path,str(pointer)+".png"))
	# Converting the value of BGR to HSV value to have a better image of a cluster
	bgr_toconvert_hsv = cv2.cvtColor(fig, cv2.COLOR_BGR2HSV)
	
	# Finding the noise in the image after converting from BGR to HSV
	noise = cv2.inRange(bgr_toconvert_hsv, (zero_val, zero_val, zero_val), (zero_val, zero_val, clr_val))
	#Chaning all the sliced images which are having grey background to a black
	new_fig = cv2.imread(os.path.join(fig_path,str(pointer)+".png")) 
	new_fig[np.where(noise)] = 0
	grey_portion = cv2.cvtColor(new_fig,cv2.COLOR_BGR2GRAY)

	#finding threshold using threshold inbuilt function with 255 as color value
	(_, threshold_valu) = cv2.threshold(grey_portion, 1, clr_val, cv2.THRESH_BINARY)

	#fetching the coordinates/points with threshold in finding cords method
	cords = finding_cords(threshold_valu)
	new_fig = cv2.cvtColor(threshold_valu, cv2.COLOR_GRAY2BGR)
	# Fetching the cluster where the colour of the cluster formed is blue
	new_fig[np.where(threshold_valu)] = [zero_val, blue, blue]
	if(len(cords)>0):	
		#checking the cords/points formed is > 0 and implementing the DBSCAN unsupervised clustering technique
		sums = processing_dbscan(cords)
	else:
		sums = 0
	cv2.imwrite(os.path.join(os.path.join(path_local,"Clusters"), file_name.split('.')[0])+'/'+str(pointer) +'.png', new_fig)

	# Creating the CSV file with open inbulit fuction in python
	d_file = open(csv_file,'a', newline='')
	# implementing the writer function to write in csv file
	writer = csv.writer(d_file)
	#appending image number and number of clusters into csv
	writer.writerow([pointer, sums])
	#closing the csv file for the better implementation of code
	d_file.close()


