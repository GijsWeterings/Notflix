import numpy as np
import cv2
import glob
import fnmatch, re
import itertools
import time
import openface
from collections import OrderedDict

DEBUG = False

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
align = openface.AlignDlib('shape_predictor_68_face_landmarks.dat')
net = openface.TorchNeuralNet('openface.nn4.small2.v1.t7', 77)

def getRep(bgrImg):
    if bgrImg is None:
        raise Exception("Unable to load image")
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        # No face detected
        return 0

    alignedFace = align.align(77, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image")

    start = time.time()
    rep = net.forward(alignedFace)
    if DEBUG:
        print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
        print("Representation:")
        print(rep)
        print("-----\n")
    return rep

    # tuple matching
def labelMatches(matches, tupleLabel):
    relevantLabel = filter(lambda x : x[0] == tupleLabel, matches)
    mappedLabels = map(lambda x : x[1], relevantLabel)
    remainingMatches = [x for x in matches if x not in mappedLabels]
    result = [tupleLabel]
    for x in mappedLabels:
        result.extend(labelMatches(remainingMatches, x))
    return OrderedDict((x, True) for x in result).keys()


cap = cv2.VideoCapture('testEpisode.mp4')

fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
frameSize = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
videoWrite = cv2.VideoWriter('example.mp4', int(fourcc), int(fps), frameSize, 1)

nframe = 1
while(nframe < 33):
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

    videoWrite.write(old_frame)
    nframe = nframe + 1

framess = []
framesID = []
for frame in range(nframe):
    files = glob.glob ("faces/" + "frame" +  str(frame) + "face*.png")
    X_data = []
    Y_data = []
    for myFile in files:
        image = cv2.imread(myFile)
        X_data.append(image)
        Y_data.append(myFile)
    framess.append(X_data)
    framesID.append(Y_data)

matchingFaces = []
for (frame1, frame2) in itertools.combinations(framess, 2):
    for face1 in frame1:
        for face2 in frame2:
            d = getRep(face1) - getRep(face2)
            if float("{:.3f}".format(np.dot(d,d,))) <= 0.100:
                com1 = (framess.index(frame1),frame1.index(face1) + 1)
                com2 = (framess.index(frame2),frame2.index(face2) + 1)
                paired = (com1,com2)
                matchingFaces.append(paired)

                if DEBUG:
                    print (matchingFaces)
                    print("Frame1: " + str(framesID[framess.index(frame1)]) + " Frame2: " + str(framesID[framess.index(frame2)]))
                    print("Frame1: " + str(framess.index(frame1)) + " Frame2: " + str(framess.index(frame2)))
                    print ("Face1 : " + str ((frame1.index(face1)) + 1))+ " Face2: " + str(frame2.index(face2) + 1)
                    print("  + Squared l2 distance between representations: {:0.3f}".format(np.dot(d, d)))
labels = {}
while(matchingFaces != []):
    eigenFace = str(matchingFaces[0][0])
    result = labelMatches(matchingFaces, matchingFaces[0][0])
    matchingFaces = filter(lambda (x,y): x not in result, matchingFaces)
    labels[eigenFace] = result

print(labels.keys())
print(labels)
