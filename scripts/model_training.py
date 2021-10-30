import face_recognition
import cv2
import numpy as np
import os
import glob

print('### Loading files ###')

# Variable declaration and image loading
faces_encodings = []
faces_names = []
cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'app/data/test-pictures/')
list_of_files = [f for f in glob.glob(path+'*.jpg')]
number_files = len(list_of_files)
names = list_of_files.copy()

print(f'Found {number_files} images under {path}.')

# Model training

print('### Model Training ###')

for i in range(number_files):
    formatted_file_name = f'image_{i}'
    formatted_encoding_name = f'image_{i}'

    file_name = face_recognition.load_image_file(list_of_files[i])
    encoding_result = face_recognition.face_encodings(globals()[formatted_file_name])[0]
    faces_encodings.append(encoding_result)

    print(file_name)

    names[i] = names[i].replace(cur_direc, "")  
    faces_names.append(names[i])

print('Model trained successfully')