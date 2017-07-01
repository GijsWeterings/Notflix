import cv2
import numpy as np
from multiprocessing import Pool

NUM_CPU_CORES = 8

def calculateRow(i):
    normalizer = 256.0**2
    row = np.zeros((video.shape[1],1), np.float64)
    for j in range(video.shape[1]):
        product = float(video[i][j]) * float(audio[i][j])
        row[j] = (product / normalizer) * 256
    return row


video = cv2.imread("pllsimilaritymatrix.png",0)
audio = cv2.imread("pllaudiosimilaritymatrix.png",0)

pool = Pool(NUM_CPU_CORES)

result = np.array(pool.map(calculateRow, range(video.shape[0])))

cv2.imwrite("combinedSimilarityMatrix.png", result)