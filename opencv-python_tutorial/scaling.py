import numpy as np
import matplotlib.pyplot as plt

import cv2

img = cv2.imread('messi5.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
res1 = cv2.resize(img,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)

height, width = img.shape[:2]
res2 = cv2.resize(img,(2*width,2*height),interpolation=cv2.INTER_CUBIC)

plt.subplot(1,3,1)
plt.imshow(img)
plt.title('Original')

plt.subplot(1,3,2)
plt.imshow(res1)
plt.title('Resize 1')

plt.subplot(1,3,3)
plt.imshow(res2)
plt.title('Resize 2')
plt.show()


