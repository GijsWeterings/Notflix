import cv2
import numpy as np
import math
from scipy import spatial
from multiprocessing import Pool

ep1 = np.array(cv2.imread("ep1.png"))
ep2 = np.array(cv2.imread("ep2.png"))

def cosine_similarity(x,y):
    a, b = x.astype(float), y.astype(float)
    return (1 - spatial.distance.cosine(a,b)) * 256

def inside(i):
    arr = np.zeros((7200,1), np.float64)
    for j in range(7200):
        arr[j,0] = cosine_similarity(ep1[:,i,0],ep2[:,j,0])
    return arr

pool = Pool(8)

rows = pool.map(inside, range(7200))

result = np.array(rows)
cv2.imwrite('similaritymatrix.png', result)
pool.close()


