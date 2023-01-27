import os
import csv
from PIL import Image
from numpy import asarray
import numpy as np
import cv2
from sklearn.model_selection import train_test_split 
from keras.utils.np_utils import to_categorical
from tensorflow.keras.applications import VGG16
from keras.models import Sequential,model_from_json
from keras.layers import Conv2D, Dense, Dropout, Flatten, Activation
from tensorflow.keras.metrics import BinaryAccuracy, Precision,Recall,AUC
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
import tensorflow as tf
import keras.backend as K
import datetime

image_folder = os.path.join(os.getcwd(), "testPatient")
list_dir = [i for i in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder,i))]
image = []
label = []
trained_model=Sequential()
# Creating labels for model
def creating_labels(image_folder,i,file_name,row_value):
  fig = cv2.imread(os.path.join(image_folder,i,file_name))
  fig = cv2.resize(fig, (256,256))
  fig = cv2.cvtColor(fig, cv2.COLOR_BGR2RGB)
  image.append(fig)
  if(row_value>0):
    label.append(1)
  else:
    label.append(0)


def creating_model(base_model):
  # Adding base model
  trained_model.add(base_model)
  trained_model.add(Dropout(0.3))
  # Initializing layer with 8190 weights
  trained_model.add(Dense(8190))
  # Adding dropout of 0.3
  trained_model.add(Dropout(0.3))
  # Adding activation layer of relu
  trained_model.add(Activation('relu'))
  # Initializing layer with 1020 weights
  trained_model.add(Dense(1020))
  # Adding dropout of 0.2
  trained_model.add(Dropout(0.2))
  # Adding activation layer of relu
  trained_model.add(Activation('relu'))
  # Initializing layer with 130 weights
  trained_model.add(Dense(130))
  # Adding dropout of 0.2
  trained_model.add(Dropout(0.2))
  # Adding activating layer of relu
  trained_model.add(Activation('relu'))
  # Initializing layer with 20 layers
  trained_model.add(Dense(20))
  # Adding dropout of 0.2
  trained_model.add(Dropout(0.25))
  # Adding activating layer of relu
  trained_model.add(Activation('relu'))
  # Initializing layer with 2 layers
  trained_model.add(Dense(2))
  # Adding dropout of 0.25
  trained_model.add(Dropout(0.25))
  # Adding activating layer of relu
  trained_model.add(Activation('relu'))
  # Flattening the model
  trained_model.add(Flatten())
  # Initializing layer with 1 layer and activation layer sigmoid
  trained_model.add(Dense(1,activation='sigmoid'))

for i in list_dir:
  for file_name in os.listdir(os.path.join(image_folder,i)):
    if("_thresh" in file_name ):
      file_name2 = file_name.split("_")
      # Reading labels of each image into labels.csv file
      labels_file = csv.reader(open(os.path.join(image_folder,i+str("_Labels.csv")), "r"), delimiter=",")
      next(labels_file,None)
      for row in labels_file:
        if(file_name2[1] == row[0]):
          creating_labels(image_folder,i,file_name,int(row[1]))
          # if(int(row[1])>0):
          #   fig = cv2.imread(os.path.join(image_folder,i,file_name))
          #   fig = cv2.resize(fig, (256,256))
          #   fig = cv2.cvtColor(fig, cv2.COLOR_BGR2RGB)
          #   image.append(fig)
          #   label.append(1)
          # else:
          #   fig = cv2.imread(os.path.join(image_folder,i,file_name))
          #   fig = cv2.resize(fig, (256,256))
          #   fig = cv2.cvtColor(fig, cv2.COLOR_BGR2RGB)
          #   image.append(fig)
          #   label.append(0)

X = np.array(image)
Y = np.array(label)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=25)
model_id='base_model'
no_epochs = 100
early_stopping_patience = 50

base_model = VGG16(input_shape=(256,256, 3),include_top=False,weights="imagenet")
for layer in base_model.layers:
    layer.trainable=True
    
creating_model(base_model)

# Calculating accuracy, precision, recall and auc
Calculated_metrics = [BinaryAccuracy(name='accuracy'),Precision(name='precision'),Recall(name='recall'),AUC(name='auc')]

# Reducing the learning rate by a factor of 0.75
reduce_rate = ReduceLROnPlateau(monitor = 'val_loss',patience = 5,verbose = 1,factor = 0.75, min_lr = 1e-10)

# Modeling check point  to save the model
model_checkpoint = ModelCheckpoint(filepath=image_folder + '/' + model_id + '.h5',save_freq='epoch',period=1)

# Stopping the training when the metric has stopped improving
early_stopping = EarlyStopping(verbose=1, patience=early_stopping_patience)

# compiling the model with learning rate 1e-5 and categorical_crossentropy
trained_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), loss='categorical_crossentropy',metrics=Calculated_metrics)

# Fitting the model with early stopping, model checkpoint, reduce_rate
history=trained_model.fit(X_train, Y_train,validation_data=(X_test, Y_test),verbose = 1,epochs = no_epochs,callbacks=[reduce_rate,model_checkpoint,early_stopping])
# Saving the model
trained_model.save(os.path.join(os.getcwd(), model_id+".h5"))

