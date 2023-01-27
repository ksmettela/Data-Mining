from clustering import find_edge_contour_call_fetchRect
import cv2
import shutil
import os
import csv

def import_data(path_local = os.getcwd()):
	#Importing data from testPatient dataset
	'''
	print("reading data from testdata")
	#for reading Patient data (for our given dataset)
	print("PatientData/Data")
	local_cpath = os.path.isdir(os.path.join(path_local,"PatientData"))
	if local_cpath:
		print(local_cpath)
		test_data_folder = os.path.join(path_local,"PatientData","Data")
	'''

	'''
	#for reading testPatient data with data folder
	# If the test patient folder contains all the data inside the data folder then this has to be excecuted
	print("testPatient/Data")
	local_cpath = os.path.isdir(os.path.join(path_local,"testPatient","Data"))
	if local_cpath:
		print(local_cpath)
		test_data_folder = os.path.join(path_local,"testPatient","Data")
	'''

	#for reading testPatient data
	# If the test patient folder contains all the data with the folder to perform the extraction then this has to be exceuted
	print("testPatient")
	local_cpath = os.path.isdir(os.path.join(path_local,"testPatient"))
	if local_cpath:
		print(local_cpath)
		test_data_folder = os.path.join(path_local,"testPatient")
	# Selecting test_data_ folder from the list directory
	for dataset in os.listdir(test_data_folder):
		# From the dataset selecting only fig names ending having thresh
		if("thresh" in dataset ):
			create_files_s_b(dataset)


def readFiles(path_local = os.getcwd()):
	# Checking if the path is existing in the directory or not
	print("Checking Slices folder in current directory")
	local_cpath = os.path.isdir(os.path.join(path_local,"Slices"))
	# Deleting the files if already exiting in Slices
	
	if local_cpath:
		print("Deleting Slices folder as it already exists")
		shutil.rmtree(os.path.join(path_local,"Slices"))

	print("Checking Clusters folder in current directory")
	local_cpath = os.path.isdir(os.path.join(path_local,"Clusters"))
	# Deleting the files if already exiting in Clusters
	
	if local_cpath:
		print("Deleting Clusters folder as it already exists")
		shutil.rmtree(os.path.join(path_local,"Clusters"))
	
	import_data()

def create_files_s_b(file_name):
	path_local = os.getcwd()
	# Creating Slices folder in current directory
	print("Creating Slices folder")
	local_cpath = os.path.isdir(os.path.join(path_local,"Slices"))
	# Setting the slicies folder in the main directory
	if not local_cpath:
		os.mkdir(os.path.join(path_local,"Slices"))
	local_cpath = os.path.isdir(os.path.join(os.path.join(path_local,"Slices"),file_name.split('.')[0]))
	if not local_cpath:
		os.mkdir(os.path.join(os.path.join(path_local,"Slices"),file_name.split('.')[0]))

	# Creating Clusters folder in current directory
	print("Creating Clusters folder")
	local_cpath = os.path.isdir(os.path.join(path_local,"Clusters"))
	# Setting to the Clusters folder in the main directory
	if not local_cpath:
		os.mkdir(os.path.join(path_local,"Clusters"))
	local_cpath = os.path.isdir(os.path.join(os.path.join(path_local,"Clusters"),file_name.split('.')[0]))
	if not local_cpath:
		os.mkdir(os.path.join(os.path.join(path_local,"Clusters"),file_name.split('.')[0]))

	
	#Naming the csv file columns as slice number and cluster count to notedown all the count of sliced images
	header = ["SliceNumber", "ClusterCount"]
	# Creating the CSV file with open inbulit fuction in python
	d_file = open(os.path.join(os.path.join(os.path.join(path_local,"Clusters"),file_name.split('.')[0]),file_name.split('.')[0]+str(".csv")),'w')
	# implementing the writer function to write in csv file
	writer = csv.writer(d_file)
	#Headers into csv file
	writer.writerow(header)
	#closing the csv file for the better implementation of code
	d_file.close()
	#calling find_edge_contour_call_fetchRect from clustering.py file
	find_edge_contour_call_fetchRect(os.path.join(path_local,"testPatient"),file_name)


# Calling the method readfiles to excute the code!!! 
readFiles()
# This gets printed when the execution stops.
print('----The End----')