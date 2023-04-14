# Unsupervised Learning - Clustering Techniques for Brain Slices Detection
This project involves the detection of the number of clusters present in extracted brain slices of resting state functional magnetic resonance imaging (rs-fMRI) scans. The project requires the implementation of clustering techniques to detect the number of clusters present in the extracted brain slices.

## Project Requirements
Python 3.6 to 3.9

## Project Overview
The project involves two main parts:

- Extracting brain slices in every image.
- Applying clustering techniques to detect the number of clusters present in every brain slice.
To extract the noticeable big enough cluster, the program should only report the number of clusters whose pixel value is greater than 135 pixels.

## Project Deliverables
The project requires the submission of two Python files: clustering.py and test.py.

- clustering.py reads all the images (images those end with word “thresh”) from the given data and performs slices extraction. It counts the number of clusters every slice contains using clustering techniques like DBSCAN.

- test.py imports all the clustering.py functions and reads the ‘testPatient’ folder. It outputs two folders named ‘Slices’ and ‘Clusters’. ‘Slices’ folder will further have ‘N’ number of folders where N is number of images that end with ‘thresh”. Every image folder contains the brain slices images of that IC_thresh image. Similarly, another folder ‘Clusters’ will also have N number of folders and every folder will have clusters detected images along with one ‘csv’ file which will report the number of clusters for every slice in that image folder. If the IC_thresh image has 33 brain slices images, then that IC image folder will contain cluster detected images of those 33 slices along with a ‘csv’ file reporting their count.

## Dataset
The project provides one patient’s dataset which will contain approximately 100 spatial ICs of that patient’s rs-fMRI scan.

## How to Use
- Clone the repository to your local machine.
- Ensure that Python 3.6 to 3.9 is installed.
- Run clustering.py to extract the brain slices images and detect the number of clusters present in every slice.
- Import all the clustering.py functions to test.py.
- Run test.py to generate two folders named ‘Slices’ and ‘Clusters’. ‘Slices’ folder will further have ‘N’ number of folders where N is number of images that ends with ‘thresh”. Every image folder contains the brain slices images of that IC_thresh image. Similarly, another folder ‘Clusters’ will also have N number of folders and every folder will have clusters detected images along with one ‘csv’ file which will report the number of clusters for every slice in that image folder.

## Conclusion
The project has successfully implemented clustering techniques to detect the number of clusters present in extracted brain slices of resting state functional magnetic resonance imaging (rs-fMRI) scans.