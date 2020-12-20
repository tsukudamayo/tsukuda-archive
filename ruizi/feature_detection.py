"""
feature detection
"""
import os
import cv2
import shutil

_CATEGORY = 'broccoli'
_TARGET_FILE = '9.png'
_IMAGE_DIR = os.path.join(
    '/Users/user/local/06_app/crawler/python/data/food_256/', _CATEGORY
)
_DST_DIR = os.path.join('/Users/user/tmp/data/food_256_by_akaze/', _CATEGORY)
_TEST_DIR = os.path.join(_DST_DIR, 'validation')
_TRAIN_DIR = os.path.join(_DST_DIR, 'train')
_IMAGE_SIZE = (224, 224)

target_image_path = os.path.join(_IMAGE_DIR, _TARGET_FILE)
target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
target_image = cv2.resize(target_image, _IMAGE_SIZE)

print('TARGET_FILE: %s' % _TARGET_FILE)

bf = cv2.BFMatcher(cv2.NORM_HAMMING)
detector = cv2.AKAZE_create()
target_kp, target_des = detector.detectAndCompute(target_image, None)

files = os.listdir(_IMAGE_DIR)
result = {}
for file in files:
    if file == '.DS_Store' or file == _TARGET_FILE:
        continue
    comparing_image_path = os.path.join(_IMAGE_DIR, file)
    comparing_image = cv2.imread(comparing_image_path, cv2.IMREAD_GRAYSCALE)
    comparing_image = cv2.resize(comparing_image, _IMAGE_SIZE)
    comparing_kp, comparing_des = detector.detectAndCompute(
        comparing_image, None
    )
    matches = bf.match(target_des, comparing_des)
    dist = [m.distance for m in matches]
    ret = sum(dist) / len(dist)

    result[str(file)] = ret

ascending_order_files = []
for k, v in sorted(result.items(), key=lambda x: x[1]):
    print(str(k) + ": " + str(v))
    ascending_order_files.append(k)

#---------------------
# copy 100 candidates
#---------------------
if os.path.isdir(_DST_DIR) is False:
    os.mkdir(_DST_DIR)
if os.path.isdir(_TEST_DIR) is False:
    os.mkdir(_TEST_DIR)
if os.path.isdir(_TRAIN_DIR) is False:
    os.mkdir(_TRAIN_DIR)

i = 0
for file in ascending_order_files:
    filepath = os.path.join(_IMAGE_DIR, file)
    print('file', filepath)
    if i <= 20:
        shutil.copy2(filepath, os.path.join(_TEST_DIR, file))
    elif i > 20:
        shutil.copy2(filepath, os.path.join(_TRAIN_DIR, file))
    i += 1
    if i == 200:
        break
