import numpy as np
import matplotlib.pyplot as plt

import cv2


roi = cv2.imread('rose_red.png')
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

target = cv2.imread('rose.png')
hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

roihist = cv2.calcHist([hsv],[0,1],None,[180,256],[0,180,0,256])

cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)

disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(dst,-1,disc,dst)

ret, thresh = cv2.threshold(dst,50,255,0)
thresh = cv2.merge((thresh,thresh,thresh))
res = cv2.bitwise_and(target,thresh)

#
plt.subplot(2,2,1)
plt.imshow(target)
plt.xticks([])
plt.yticks([])
plt.title('Original')

plt.subplot(2,2,3)
plt.imshow(thresh,cmap='gray')
plt.xticks([])
plt.yticks([])
plt.title('Backprojection')

plt.subplot(2,2,4)
plt.imshow(res)
plt.xticks([])
plt.yticks([])
plt.title('Results')

plt.show()
