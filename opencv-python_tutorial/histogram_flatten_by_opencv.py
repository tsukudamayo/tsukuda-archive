import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('tsukuba_l.jpg',0)


clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)

plt.subplot(1,2,1)
plt.imshow(img,cmap='gray')
plt.xticks([])
plt.yticks([])
plt.title('Original')

plt.subplot(1,2,2)
plt.imshow(cl1,cmap='gray')
plt.xticks([])
plt.yticks([])
plt.title('CLAHEd')

plt.show()
