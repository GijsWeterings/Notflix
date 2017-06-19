import cv2
import numpy as np
from matplotlib import pyplot as plt

DEBUG = True

cap = cv2.VideoCapture("videos/House.Of.Cards.S01E01.720p.BluRay.x265.mp4") 

totalhist = np.array([np.ones(256)], np.float64).T
for i in range(0, 7200): #5 minutes of footage, based on 24 fps
    retrieved, colorimg = cap.read()
    image = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(colorimg, cv2.COLOR_BGR2HSV)

    if(retrieved):
        hist = cv2.calcHist([colorimg], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([colorimg], [1], None, [256], [0, 256])
        hist3 = cv2.calcHist([colorimg], [2], None, [256], [0, 256])
        # hist = cv2.calcHist([image], [0], None, [256], [0,256])
        # hist = (hist / sum(hist)) * 256 * 1
        if(DEBUG and i % 1000 == 0):
            print("frame dimensions: ", colorimg.shape)
            print("histogram shape: ", hist.shape)
            print("histogram shape: ", hist2.shape)
            print("histogram shape: ", hist3.shape)
            print("totalHist shape: ", totalhist.shape)
            # cv2.imshow("a", hsv)
            # cv2.waitKey(0)
            plt.plot(hist)
            plt.show()
        totalhist = np.concatenate([totalhist, hist], axis=1)
        
# Remove initial column
totalhist = np.delete(totalhist, 0, axis=1)
print(totalhist.shape)
cv2.imwrite('ep1.png', totalhist)
cv2.waitKey(0)

cap.release()
