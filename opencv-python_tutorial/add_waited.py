import numpy as np
import matplotlib.pyplot as plt

import cv2


x = np.uint8([250])
y = np.uint8([10])

print('cv2.add(x, y)', cv2.add(x, y))
print('x + y', x + y)

img1 = cv2.imread('ml.png')
img2 = cv2.imread('opencv-logo.png')

print('img1.shape', img1.shape)
print('img2.shape', img2.shape)

img1 = cv2.resize(img1, (256, 256))
img2 = cv2.resize(img2, (256, 256))

print('img1.shape', img1.shape)
print('img2.shape', img2.shape)

dst = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
