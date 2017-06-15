import cv2
import numpy as np
from scipy import spatial
from multiprocessing import Pool

ep1 = cv2.imread("ep2.png")
ep2 = cv2.imread("ep2.png")

def inside(i):
    arr = np.zeros((7200,1), np.float64)
    for j in range(7200):
        sim = cosineSim(ep1[:,i,0], ep2[:,j,0])
        arr[j,0] = sim
    return (i, arr)

def cosineSim(v1, v2):
    return spatial.distance.cosine(v1, v2) * 256
pool = Pool(8)

img = np.zeros((7200, 7200, 1), np.float64)
rows = pool.map(inside, range(7200))

orderedImage = np.empty((7200, 7200, 1), dtype = float)
for (index, row) in rows:
    orderedImage[index] = row

result = orderedImage
print(result.shape)
cv2.imwrite('similaritymatrix.png', result)
cv2.waitKey(0)
pool.close()
