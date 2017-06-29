import cv2
import numpy as np
import math
from scipy import spatial
from multiprocessing import Pool

NUM_CPU_CORES = 8
FPS = 24
NUMBER_OF_FRAMES_TO_SAMPLE = FPS * 60 * 5

def cosine_similarity(x,y):
    """
    Calculates the cosine similarity between the two vectors, scaled to a 0-256 range.
    """
    # This will prevent overflow issues with scipy
    a, b = x.astype(float), y.astype(float)

    # We have to do the "1 -" because we want similarity, not distance.
    return (1 - spatial.distance.cosine(a,b)) * 256

def calculateRow(i):
    """
    For an entire row, calculate and store the cosine similarity.
    """
    row = np.zeros((NUMBER_OF_FRAMES_TO_SAMPLE,1), np.float64)
    for j in range(NUMBER_OF_FRAMES_TO_SAMPLE):
        row[j,0] = cosine_similarity(episode1[:,i,0],episode2[:,j,0])
    return row

episode1 = np.array(cv2.imread("pllep1.png"))
episode2 = np.array(cv2.imread("pllep2.png"))

pool = Pool(8)

result = np.array(pool.map(calculateRow, range(7200)))
cv2.imwrite('pllsimilaritymatrix.png', result)
pool.close()