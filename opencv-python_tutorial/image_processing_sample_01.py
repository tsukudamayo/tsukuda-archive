import numpy as np
import matplotlib.pyplot as plt

import cv2


def image_show(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.show()


img = cv2.imread('messi5.jpg')
px = img[100,100]
print('px', px)

blue = img[100,100,0]
print('blue', blue)

# better how to acsess for image
# accessing red value
print('accesing RED value img.item(10,10,2) :', img.item(10,10,2))

# modifying red value.
print('modifying RED value img.itemset((10,10,2),100) :', img.itemset((10,10,2),100))

# shape
print('img.shape :', img.shape)

# size
print('img.size :', img.size)

# dtype
print('img.dtype :', img.dtype)

# show
image_show(img)

print('*'*10 + ' ROI ' + '*'*10)
ball = img[280:340, 330:390]
img[273:333, 100:160] = ball
image_show(img)
