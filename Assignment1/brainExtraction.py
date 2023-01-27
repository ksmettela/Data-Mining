import cv2
import shutil
import os

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
	
	# Slicing the figure according to the boundaries
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

			print("Creating Boundaries images")
			clr_val4 = 255

			print("Drawing contour line for boundaries images")
			cv2.drawContours(new_fig, contour_val, -1, (0,clr_val4,0), 1)
			cv2.imwrite(os.path.join(os.path.join(path_local,"Boundaries"),file_name.split('.')[0])+'/'+str(pointer) +'.png', new_fig)

		else:
			continue
		pointer = pointer + 1

