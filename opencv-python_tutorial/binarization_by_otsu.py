import numpy as np
import matplotlib.pyplot as plt

import cv2


img = cv2.imread('noisy.png', 0)

ret1, th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
