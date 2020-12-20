import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('histeq_numpy1.jpg')
hist, bins = np.histogram(img.flatten(),256,[0,256])

cdf = hist.cumsum()
cdf_normalized = cdf*hist.max() / cdf.max()

# original
plt.subplot(1,2,1)
plt.imshow(img,cmap='gray')
plt.xticks([])
plt.yticks([])
plt.title('image')

plt.subplot(1,2,2)
plt.plot(cdf_normalized,color='b')
plt.hist(img.flatten(),256,[0,256],color='r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'),loc='upper left')

plt.show()


# histogram flatten
cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype('uint8')

img2 = cdf[img]

hist, bins = np.histogram(img2.flatten(),256,[0,256])
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max() / cdf.max()

plt.subplot(1,2,1)
plt.imshow(img2,cmap='gray')
plt.xticks([])
plt.yticks([])
plt.title('image')

plt.subplot(1,2,2)
plt.plot(cdf_normalized,color='b')
plt.hist(img2.flatten(),256,[0,256],color='r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'),loc='upper left')

plt.show()
