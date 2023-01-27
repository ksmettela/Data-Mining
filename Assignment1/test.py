from brainExtraction import find_edge_contour_call_fetchRect
import cv2
import shutil
import os

def import_data(path_local = os.getcwd()):
	print("reading data from testdata")

	#for reading Patient data (for our given dataset)
	print("PatientData/Data")
	local_cpath = os.path.isdir(os.path.join(path_local,"PatientData"))
	if local_cpath:
		print(local_cpath)
		test_data_folder = os.path.join(path_local,"PatientData","Data")
	
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
			find_edge_contour_call_fetchRect(test_data_folder,dataset)


def readFiles(path_local = os.getcwd()):
	# Checking if the path is existing in the directory or not
	print("Checking Slices folder in current directory")
	local_cpath = os.path.isdir(os.path.join(path_local,"Slices"))
	# Deleting the files if already exiting in Slices
	
	if local_cpath:
		print("Deleting Slices folder as it already exists")
		shutil.rmtree(os.path.join(path_local,"Slices"))

	print("Checking Boundaries folder in current directory")
	local_cpath = os.path.isdir(os.path.join(path_local,"Boundaries"))
	# Deleting the files if already exiting in Boundaries
	
	if local_cpath:
		print("Deleting Boundaries folder as it already exists")
		shutil.rmtree(os.path.join(path_local,"Boundaries"))
	
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

	# Creating Boundaries folder in current directory
	print("Creating Boundaries folder")
	local_cpath = os.path.isdir(os.path.join(path_local,"Boundaries"))
	# Setting to the boundaries folder in the main directory
	if not local_cpath:
		os.mkdir(os.path.join(path_local,"Boundaries"))
	local_cpath = os.path.isdir(os.path.join(os.path.join(path_local,"Boundaries"),file_name.split('.')[0]))
	if not local_cpath:
		os.mkdir(os.path.join(os.path.join(path_local,"Boundaries"),file_name.split('.')[0]))

# Calling the method readfiles to excute the code!!! 
readFiles()
# This gets printed when the execution stops.
print('----The End----')