# Extracting Brain boundaries from rs-fMRI data
This project aims to extract the brain boundaries from the resting state functional magnetic resonance imaging (rs-fMRI) scans using Python 3.6 to 3.9.

## Purpose
The purpose of this project is to automate the process of extracting brain slices and boundaries from the rs-fMRI scans. By completing this project, extracting brain slices from the dataset and extract the brain boundary (periphery) from those slices.

## Objectives
- Extract brain slices from the rs-fMRI dataset.
- Extract the brain boundary (periphery) from those slices using MELODIC software.
- Automate the process of brain slice and boundary extraction for a given patient's rs-fMRI scan's spatial independent components (ICs).

## Technology Requirements
Python 3.6 to 3.9

## Dataset
Provided with one patient's dataset which contains approximately 100 spatial ICs images of that patient's rs-fMRI scan.

## Analysis Procedure
Given the spatial images of patients, the task is divided into two parts:

- Brain slice extraction: Given a spatial IC, automate the brain slices extraction process. So, if a patient has N such images, task is to automate the slice extraction for all the N images.
- Brain boundary extraction: Once there are extracted the brain slices, the next task is to extract the boundary of the brain in every extracted slice.

## File Structure
- brainExtraction.py: This file reads all the images (images that end with the word "thresh") from the given data and performs the brain slice extraction and brain boundary extraction.
- test.py: This file reads a folder named testPatient and outputs two folders: one folder named Slices and another folder named Boundaries. The Slices folder will further have N number of folders where N is the number of images that end with "thresh". For example, in the given data we have N=112 (testPatient will have different N). Every image folder should contain the brain slices images of that IC_thresh image. Similarly, the Boundaries folder will also have N number of folders, and every folder will have boundary highlighted images of that IC_thresh image.

## Conclusion
This project provides an opportunity to gain experience in utilizing Python to extract brain slices and boundaries from rs-fMRI scans. Furthermore, it offers a chance to learn how to automate this process for a specific patient's rs-fMRI scan's spatial independent components (ICs). 