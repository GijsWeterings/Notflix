import cv2
import numpy as np
from scipy import spatial


def cosine_similarity(x,y):
    """
    Calculates the cosine similarity between the two vectors, scaled to a 0-256 range.
    """
    # We have to do the "1 -" because we want similarity, not distance.
    return (1 - spatial.distance.cosine(x, y)) * 256

ep1 = np.load("np/ep1.npy")
ep2 = np.load("np/ep2.npy")

(x, y) = ep1.shape

rows = []
for i in range(x):
    row = np.zeros((x ,1), np.float64)
    for j in range(x):
        row[j,0] = cosine_similarity(ep1[i], ep2[j])
    rows.append(row)

result = np.array(rows)
cv2.imwrite('pllaudiosimilaritymatrix.png', result)