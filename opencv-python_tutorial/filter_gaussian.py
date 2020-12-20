import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('opencv-logo.png')
blur = cv2.GaussianBlur(img,(5,5),0)

plt.subplot(121)
plt.imshow(img)
plt.title('Original')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(blur)
plt.title('Blurred')
plt.xticks([])
plt.yticks([])

plt.show()
