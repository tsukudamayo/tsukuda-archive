import numpy as np
import matplotlib.pyplot as plt

import cv2


BLUE = [255,0,0]
img1 = cv2.imread('opencv-logo.png')

replicate = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REPLICATE)
refrect = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT)
refrect101 = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT101)
wrap = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_WRAP)
constant = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_CONSTANT, value=BLUE)

plt.subplot(231)
plt.imshow(img1, 'gray')
plt.title('ORIGINAL')

plt.subplot(232)
plt.imshow(replicate, 'gray')
plt.title('REPLICATE')

plt.subplot(233)
plt.imshow(refrect, 'gray')
plt.title('REFLECT')

plt.subplot(234)
plt.imshow(refrect101, 'gray')
plt.title('REFLECT_101')

plt.subplot(235)
plt.imshow(wrap, 'gray')
plt.title('WRAP')

plt.subplot(236)
plt.imshow(constant, 'gray')
plt.title('CONSTANT')

plt.show()



