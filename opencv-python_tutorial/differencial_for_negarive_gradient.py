import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('box.png',0)

sobelx8u = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)

sobelx64f = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
abs_sobel64f = np.absolute(sobelx64f)
sobel_8u = np.uint8(abs_sobel64f)

images = [img, sobelx8u, sobel_8u]
titles = ['Original', 'Sobel CV 8U', 'Sobel abs(CV_64F)']

for i in range(3):
    plt.subplot(1,3,i+1)
    plt.imshow(images[i],cmap='gray')
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
