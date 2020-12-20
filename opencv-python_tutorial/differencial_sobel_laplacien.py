import numpy as np
import matplotlib.pyplot as plt

import cv2

img = cv2.imread('sudoku.png',0)

laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

images = [img, laplacian, sobelx, sobely]
titles = ['Original', 'Laplacian', 'Sobel X', 'Sobel Y']

for idx, image, title in zip(range(4), images, titles):
    plt.subplot(2,2,idx+1)
    plt.imshow(image,cmap='gray')
    plt.title(title)
    plt.xticks([])
    plt.yticks([])

plt.show()
