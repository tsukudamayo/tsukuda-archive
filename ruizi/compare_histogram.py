"""
histogram matching
"""
import os
import cv2


_TARGET_FILE = '3.png'
_IMAGE_DIR = '/Users/user/local/06_app/crawler/python/data/food_256/cucumber/'
_IMAGE_SIZE = (224, 224)

target_image_path = _IMAGE_DIR + _TARGET_FILE
target_image = cv2.imread(target_image_path)
target_image = cv2.resize(target_image, _IMAGE_SIZE)
target_hist = cv2.calcHist([target_image], [0], None, [256], [0, 256])

print('TARGET_FILE: %s' % _TARGET_FILE)

files = os.listdir(_IMAGE_DIR)
result = {}
for file in files:
    if file == '.DS_Store' or file == _TARGET_FILE:
        continue

    comparing_image_path = _IMAGE_DIR + file
    comparing_image = cv2.imread(comparing_image_path)
    comparing_image = cv2.resize(comparing_image, _IMAGE_SIZE)
    comparing_hist = cv2.calcHist([comparing_image],
                                   [0],
                                   None,
                                   [256],
                                   [0, 256],)

    ret = cv2.compareHist(target_hist, comparing_hist, 0)
    # print(file, ret)
    result[str(file)] = ret

for k, v in sorted(result.items(), key=lambda x: x[1]):
    print(str(k) + ": " + str(v))
