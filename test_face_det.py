import numpy as np
import cv2
import glob
import fnmatch, re
import itertools
import time
import openface


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
net = openface.TorchNeuralNet('openface.nn4.small2.v1.t7', 77)
align = openface.AlignDlib('shape_predictor_68_face_landmarks.dat')

old_frame = cv2.imread("videos/MichelGill.jpg")
gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
face = 1
for(x,y,w,h) in faces:
    cv2.rectangle(old_frame,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = old_frame[y:y+h, x:x+w]
    crop_img = old_frame[y: y + h, x: x + w]
    cv2.imwrite("faces/test.png", crop_img)
