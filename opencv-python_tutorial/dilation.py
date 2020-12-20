import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('j.png',0)
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

plt.subplot(121)
plt.imshow(img)
plt.title('Original')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(opening)
plt.title('Opening')
plt.xticks([])
plt.yticks([])

plt.show()

