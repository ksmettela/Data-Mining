import os
import csv
from PIL import Image
from numpy import asarray
import numpy as np
import cv2
from keras.models import load_model
from sklearn.metrics import confusion_matrix

image_folder = os.path.join(os.getcwd(),"testPatient")
image, label = [], []
final_model = load_model(os.path.join(os.getcwd() , 'base_model.h5'))
# print("Loaded model from disk")
final_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
y_pred, result=[],[]


def creating_labels(image_folder, file_name, final_model, result, y_pred,label,row_value, file_list):
    # Reading each image from test_data folder and creating matrix array 
    individual_image = cv2.imread(os.path.join(image_folder,"test_Data",file_name))
    # Resizing image of each image
    individual_image = cv2.resize(individual_image, (256,256))
    individual_image = cv2.cvtColor(individual_image, cv2.COLOR_BGR2RGB)
    # Reshaping the image
    individual_image = np.array(individual_image).reshape(-1,256,256, 3)
    # Predicting the image based on weights of final_model
    ynew = final_model.predict(individual_image)
    # Converting the predicted values to list
    pred = ynew.tolist()
    temp=pred[0].index(max(pred[0]))
    # Creating result
    result.append([file_list[1],temp])
    y_pred.append(temp)
    if(row_value>0):
        label.append(1)
    else:
        label.append(0)

# Writing accuracy, precision, sensitity, specificity to a file named matrics.csv
def write_matrics_file(accuracy,precision,sensivity,specificity):
    with open(os.path.join(os.getcwd(),"Matrics.csv"), 'w') as file:
        writer = csv.writer(file)
        # Writing Accuracy row
        writer.writerow(["Accuracy", accuracy])
        # Writing Precision row
        writer.writerow(["Precision", precision])
        # Writing Sensivity row
        writer.writerow(["Sensivity", sensivity])
        # Writing Specificity row
        writer.writerow(["Specificity", specificity])

    file.close()

# Storing IC_Number with its label into results.csv file
def write_results_file():
    with open(os.path.join(os.getcwd(),"Results.csv"), 'w') as file:
        writer = csv.writer(file)
        # Creating headers 
        header = ["IC_Number", "Label"]
        writer.writerow(header)
        for row_data in result:
            writer.writerow(row_data)
    file.close()

def run_model():
    for file_name in os.listdir(os.path.join(image_folder,"test_Data")):
        if("_thresh" in file_name ):
            file_list = file_name.split("_")
            csv_file = csv.reader(open(os.path.join(image_folder,"test_Label.csv"), "r"), delimiter=",")
            next(csv_file,None)
            for row in csv_file:
                if(file_list[1] == row[0]):
                    # Creating labels for each image folder
                    creating_labels(image_folder,file_name,final_model,result,y_pred,label,int(row[1]), file_list)
    y_axis_value = label
    # Creating confusion matrix
    true_negative, false_positive, false_negative, true_positive = confusion_matrix(y_axis_value, y_pred).ravel()
    # Calculating specific value
    specificity_value = str(true_negative*100 / (true_negative+false_positive))+str("%")
    # Calculating Sensivity value
    sensivity_value = str(true_positive*100/(true_positive+false_negative))+str("%")
    # Calculating Precision value
    precision_value = str(true_positive*100/(true_positive + false_positive))+str("%")
    # Calculating Accuracy Value
    accuracy_value = str((true_positive+true_negative)*100/np.sum(confusion_matrix(y_axis_value, y_pred)).astype('float'))+str("%")
    # Writing results to results file
    write_results_file()
    # Storing accuracy of each image into matrics file
    write_matrics_file(accuracy_value,precision_value,sensivity_value,specificity_value)
    print("Running of model done successfully")


run_model()



