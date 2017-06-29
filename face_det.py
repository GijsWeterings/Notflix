import numpy as np
import cv2
import glob
import fnmatch, re
import itertools
import time
import openface

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
align = openface.AlignDlib('shape_predictor_68_face_landmarks.dat')
net = openface.TorchNeuralNet('openface.nn4.small2.v1.t7', 77)

# .dlibFacePredictor

def getRep(bgrImg):
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format("imgPath"))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    start = time.time()
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        return 0
    start = time.time()
    print(rgbImg.shape)
    alignedFace = align.align(77, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format("imgPath"))

    start = time.time()
    rep = net.forward(alignedFace)
    if True:
        print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
        print("Representation:")
        print(rep)
        print("-----\n")
    return rep

#img = cv2.imread('testpicGOT.png')
cap = cv2.VideoCapture('testEpisode.mp4')


#fourcc = cv2.CV_FOURCC('X','2','6','4')#cap.get(cv2.CAP_PROP_FRAME_COUNT)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
# to do : cap.get(cv2.CAP_PROP_FPS)
#get(cv2.cv.CV_CAP_PROP_FPS)
frameSize = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
videoWrite = cv2.VideoWriter('example.mp4', int(fourcc), int(fps), frameSize, 1)

nframe = 1
while(nframe < 50):
    ret, old_frame = cap.read()
    gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face = 1
    for(x,y,w,h) in faces:
        cv2.rectangle(old_frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = old_frame[y:y+h, x:x+w]
        crop_img = old_frame[y: y + h, x: x + w]
        cv2.imwrite("faces/frame" + str(nframe) + "face" + str(face) + ".png", crop_img)
        face = face + 1
        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
            #cv2.rectangle(old_frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    videoWrite.write(old_frame)
    nframe = nframe + 1
framess = []
for frame in range(nframe):
    files = glob.glob ("faces/" + "frame" +  str(frame) + "*.png")
    X_data = []
    for myFile in files:
        #print(myFile)
        image = cv2.imread(myFile)
        X_data.append(image)
    framess.append(X_data)
#print(framess)



for (frame1, frame2) in itertools.combinations(framess, 2):
    for face1 in frame1:
        for face2 in frame2:
            d = getRep(face1) - getRep(face2)
            print("Comparing {} with {}.".format(face1, face2))
            print("  + Squared l2 distance between representations: {:0.3f}".format(np.dot(d, d)))
#cv2.imwrite("firstFramesFaceDet.png", old_frame)
