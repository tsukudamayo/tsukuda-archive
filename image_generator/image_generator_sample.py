import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.contrib.keras.api.keras.preprocessing import image


img_path = 'data/5.png'
img = image.load_img(img_path, target_size=(224,224))

x = image.img_to_array(img)
x = x.reshape((1,) + x.shape)

datagen = image.ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
)

i = 0
for batch in datagen.flow(x, batch_size=1):
    plt.figure(1)
    imgplot = plt.imshow(image.array_to_img(batch[0]))
    plt.show()
    i += 1
    if i % 4 == 0:
        break

