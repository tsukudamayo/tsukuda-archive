import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('messi5.jpg',0)
edges = cv2.Canny(img,100,200)

plt.subplot(121)
plt.imshow(img,cmap='gray')
plt.title('Original')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(edges,cmap='gray')
plt.title('Edge Image')
plt.xticks([])
plt.yticks([])

plt.show()
