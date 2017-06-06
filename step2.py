import cv2
import numpy as np
from multiprocessing import Pool

ep1 = cv2.imread("ep1.png")
ep2 = cv2.imread("ep2.png")

def inside(i):
    arr = np.zeros((7200,1), np.float64)
    for j in range(7200):
        arr[j,0] = cosineSim(ep1[:,i,0],ep2[:,j,0])
    return arr

def cosineSim(v1, v2):
    return np.dot(v1, v2) / (len(v1) * len(v2))

pool = Pool(8)

img = np.zeros((7200, 7200, 1), np.float64)

rows = pool.map(inside, range(7200))


result = np.array(rows)
print(result.shape)
cv2.imwrite('similaritymatrix.png', result)
cv2.waitKey(0)
pool.close()
