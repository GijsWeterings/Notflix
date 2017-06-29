import cv2
import numpy as np
from multiprocessing import Pool

NUM_CPU_CORES = 8

def calculateRow(i):
    row = np.zeros((video.shape[1],1), np.float64)
    for j in range(video.shape[1]):
        row[j] = float(video[i][j]) / 2.0 + float(audio[i][j]) / 2.0
    return row


video = cv2.imread("pllsimilaritymatrix.png",0)
audio = cv2.imread("similaritymatrix.png",0)

pool = Pool(NUM_CPU_CORES)

result = np.array(pool.map(calculateRow, range(video.shape[0])))

cv2.imwrite("combinedSimilarityMatrix.png", result)