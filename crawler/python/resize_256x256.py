import os
from PIL import Image

_IMAGE_DIR = 'data/'
_TARGET_DIR = 'resize'

image_dir = _IMAGE_DIR
target_dir = _IMAGE_DIR + _TARGET_DIR

#-----------------------
# genereate directories
#-----------------------
print(os.listdir(image_dir))
sub_directories = []
for sub_directorie in os.listdir(image_dir):
    sub_directories.append(sub_directorie)

if os.path.isdir(target_dir) is False:
    os.mkdir(target_dir)
    for sub_directorie in sub_directories:
        directory = os.path.join(target_dir, sub_directorie)
        os.mkdir(directory)
#--------
# resize
#--------
for root, dirs, files in os.walk(os.getcwd()):
    for f in files:
        try:
            filepath = os.path.join(root, f)
            img = Image.open(filepath)
            img_resize = img.resize((256,256))
            targetpath = filepath.replace('data/', 'data/food_256/')
            img_resize.save(targetpath)
        except OSError:
            print('%s can not convert by OSERROR' % f)
            pass
