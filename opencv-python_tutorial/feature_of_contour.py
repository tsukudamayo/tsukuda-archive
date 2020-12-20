import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('collapsedSquare.png',0)
ret,thresh = cv2.threshold(img,127,255,0)
imgEdge, contours, hierarchy = cv2.findContours(
    thresh,
    1,
    2,
)

# compute moments
print('****************' + 'compute moments' + '****************')
cnt = contours[0]
M = cv2.moments(cnt)
print('momonts :',M)

# compute centroid
print('****************' + 'compute centroid' + '****************')
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print('cx :', cx)
print('cy :', cy)

# compute contoour area
print('****************' + 'compute contour area' + '****************')
area = cv2.contourArea(cnt)
print('contour area :', area)

# compute arc length
print('****************' + 'compute arc length' + '****************')
perimeter = cv2.arcLength(cnt,True)
print('perimeter :', perimeter)

# approximation of contour
print('****************' + 'approximation of contour' + '****************')
epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)
print('approximation of contour :', approx)

# convex hull
print('****************' + 'compute convex hull' + '****************')
hull = cv2.convexHull(cnt)
print('compute convex hull :', hull)

# validation convex or not
print('****************' + 'validation convex or not' + '****************')
k = cv2.isContourConvex(cnt)
print('validation convex or not :', k)

# circumscribed rectangle
print('****************' + 'circumscribed rectangle' + '****************')

img = cv2.imread('target.png')
im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(im,127,255,0)
imgEdge, contours, hierarchy = cv2.findContours(
    thresh,
    1,
    2,
)

cnt = contours[0]

# FittingRectangle
x,y,w,h = cv2.boundingRect(cnt)
imgR = img.copy()
imgR = cv2.rectangle(imgR,(x,y),(x+w,y+h),(0,255,0),3)
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
imgR = cv2.drawContours(imgR,[box],0,(255,0,0),3)

# FittingCircle
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
imgC = img.copy()
imgC = cv2.circle(imgC,center,radius,(0,255,0),3)

# FittingEclipse
ellipse = cv2.fitEllipse(cnt)
imgE = img.copy()
imgE = cv2.ellipse(imgE,ellipse,(0,255,0),3)

# FittingLane
rows,cols = img.shape[:2]
[vx,vy,x,y] = cv2.fitLine(cnt,cv2.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx) + y)
imgL = img.copy()
imgL = cv2.line(imgL,(cols-1,righty),(0,lefty),(0,255,0),3)

# circumscribed rectangle
images = [img, imgR, imgC, imgE, imgL]
titles = [
    'Original',
    'FittingRectangle',
    'FittingCircle',
    'FittingEclipse',
    'FittingLane',
]

for i in range(len(images)):
    plt.subplot(2,3,i+1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
