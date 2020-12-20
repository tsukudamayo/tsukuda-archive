import numpy as np
import matplotlib.pyplot as plt

import cv2


im = cv2.imread('india.png')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,127,255,0)
image, contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE,
)
cnt = contours[1]


# aspect ratio
x,y,w,h = cv2.boundingRect(cnt)
aspect_ratio = float(w)/h
print('aspect ratio = %f' % aspect_ratio)

# extent
area = cv2.contourArea(cnt)
x,y,w,h = cv2.boundingRect(cnt)
rect_area = w*h
extent = float(area)/rect_area
print('extent = %f' % extent)

# solidity
area = cv2.contourArea(cnt)
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area)/hull_area
print('solidity = %f' % solidity)

# equi_diameter
area = cv2.contourArea(cnt)
equi_diameter = np.sqrt(4*area/np.pi)
print('equi_diameter = %f' % equi_diameter)

# orientation
(x,y), (MA,ma), angle = cv2.fitEllipse(cnt)
print('x = %d, y = %d, MA = %d, ma = %d, angle = %f'
      % (x, y, MA, ma, angle))

# mask and pixelpoints
mask = np.zeros(imgray.shape, np.uint8)
cv2.drawContours(mask,[cnt],0,255,-1)
pixelpoints = np.transpose(np.nonzero(mask))

# min_val, min_loc　and its position
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(imgray,mask=mask)
print('min_val=%d, max_val=%d' % (min_val, max_val))
print('min_loc = ', min_loc, ' max_loc =', max_loc)

# mean_val
mean_val = cv2.mean(im,mask=mask)
print('mean val = ', mean_val)

# extreme points
leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

cv2.circle(im,leftmost,3,(255,0,255),3)
cv2.circle(im,rightmost,3,(0,255,255),3)
cv2.circle(im,topmost,3,(255,0,0),3)
cv2.circle(im,bottommost,3,(0,0,255),3)

plt.subplot(1,2,1)
plt.imshow(mask)
plt.title('india')
plt.xticks([])
plt.yticks([])

plt.subplot(1,2,2)
plt.imshow(im)
plt.title('Extreme points')
plt.xticks([])
plt.yticks([])

plt.show()
