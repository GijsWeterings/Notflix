import cv2
import numpy as np

img = cv2.imread("similaritymatrix.png")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, gray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# cv2.imwrite("test.png", gray)
# cv2.waitKey(0)

# edges = cv2.Canny(gray,0,255,apertureSize = 3)
edges = blur = cv2.blur(gray,(3,3))
cv2.imwrite("t.png",edges)
print(edges)
lines = cv2.HoughLinesP(edges, 1, np.pi * 0.25, 100)
print(lines[0])
for (x1, y1, x2, y2) in lines[0]:
    print(x1, y1, x2, y2)
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',img)
