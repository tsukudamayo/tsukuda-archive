import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('j.png',0)
kernel = np.ones((5,5),np.uint8)
gradient = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)

plt.subplot(121)
plt.imshow(img)
plt.title('Original')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(gradient)
plt.title('Gradient')
plt.xticks([])
plt.yticks([])

plt.show()

