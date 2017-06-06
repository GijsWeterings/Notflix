import cv2
import numpy as np
from matplotlib import pyplot as plt

#cap = cv2.VideoCapture("House.Of.Cards.S01E01.720p.BluRay.x265.mp4")
cap = cv2.VideoCapture("House.Of.Cards.S01E02.720p.BluRay.x265.mp4") 

totalhist = np.array([np.ones(256)], dtype="f").T
for i in range(0, 7200): #5 minutes of footage, based on 24 fps
    retrieved, colorimg = cap.read()
    image = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)
    if(retrieved):
        hist = cv2.calcHist([image], [0], None, [256], [0,256])
        hist = (hist / sum(hist))
#        print(hist.shape)
#        print(totalhist.shape)
        totalhist = np.concatenate([totalhist, hist], axis=1)
        
# Remove initial column
totalhist = np.delete(totalhist, 0, axis=1)
print(totalhist.shape)
cv2.imwrite('ep2.png', totalhist)
cv2.waitKey(0)

# while(True):
#x, y = cap.read()
#print(y)
# cv2.imshow('', y)
#cv2.imshow('output.png', y)
#cv2.waitKey(0)


cap.release()
