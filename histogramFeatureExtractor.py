import cv2
import numpy as np
from matplotlib import pyplot as plt

DEBUG = True

FPS = 24
NUMBER_OF_FRAMES_TO_SAMPLE = FPS * 60 * 5

def extractFeaturesToFile(inputVideo="videos/House.Of.Cards.S01E01.720p.BluRay.x265.mp4", filename="ep1.png"):
    """
    Runs the extractFeatures and writes the resulting file to disk.
    """
    features = extractFeatures(inputVideo)
    cv2.imwrite(filename, features)

def extractFeatures(inputVideo):
    """
    Step 1: Loads a video. Then, for NUMBER_OF_FRAMES_TO_SAMPLE frames, we calculate the histogram of the grayscaled frame.
    This is then normalized and scaled to a [0, 256] range, and added to the final matrix as a column.

    Output: Once all frames are analyzed and added to the final matrix, the image is returned.

    """
    cap = cv2.VideoCapture(inputVideo) 

    videoHistTotal = np.array([np.ones(256)], np.float64).T
    for i in range(0, NUMBER_OF_FRAMES_TO_SAMPLE):
        retrieved, colorimg = cap.read()
        image = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)

        if(retrieved):
            frameHist = cv2.calcHist([image], [0], None, [256], [0,256])
            normalizedFrameHist = (frameHist / sum(frameHist)) * 256
            if(DEBUG and i % 1000 == 0):
                print("frame dimensions: ", colorimg.shape)
                print("histogram shape: ", normalizedFrameHist.shape)
                print("totalHist shape: ", videoHistTotal.shape)
                plt.plot(normalizedFrameHist)
                plt.show()
            videoHistTotal = np.concatenate([videoHistTotal, frameHist], axis=1)
            
    # Remove initial column
    videoHistTotal = np.delete(videoHistTotal, 0, axis=1)

    cap.release()
    return videoHistTotal

if __name__ == "__main__":
    extractFeaturesToFile()
