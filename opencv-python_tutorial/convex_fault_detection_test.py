import numpy as np
import cv2

img1 = cv2.imread('star2.png',0)
ret, thresh = cv2.threshold(img1,127,255,0)
_, contours, hierarchy = cv2.findContours(thresh,2,1)
cnt1 = contours[0]

for num in range(2,5):
    img2 = cv2.imread('star' + str(num) + '.png', 0)
    ret, thresh = cv2.threshold(img2,127,255,0)
    _, contours, hierarchy = cv2.findContours(thresh2,2,1)
    cnt2 = contours[0]
    ret = cv2.matchShapes(cnt1,cnt2,2,0,0)
    print('Matching image A with image %d = %f' % (num, ret))
