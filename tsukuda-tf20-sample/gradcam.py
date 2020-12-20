import os

import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img, save_img
from tensorflow.keras.models import load_model

from utils import fetch_filelist
from utils import parse_category_map
from models import create_model


K.set_learning_phase(1) #set learning phase


_CHECKPOINT_DIR = './training_1'
_DATA_DIR = './data/16class_random_train_data/val'
_DST_DIR = './data/cam'


def grad_cam(model, x, layer_name):

    X = np.expand_dims(x, axis=0)

    X = X.astype('float32')
    preprocessed_input = X / 255.0

    predictions = model.predict(preprocessed_input)
    class_idx = np.argmax(predictions[0])
    score = np.max(predictions[0])
    class_output = model.output[:, class_idx]

    conv_output = model.get_layer(layer_name).output
    grads = K.gradients(class_output, conv_output)[0]
    gradient_function = K.function([model.input], [conv_output, grads])

    output, grads_val = gradient_function([preprocessed_input])
    output, grads_val = output[0], grads_val[0]

    weights = np.mean(grads_val, axis=(0, 1))
    cam = np.dot(output, weights)

    cam = cv2.resize(cam, (224, 224), cv2.INTER_LINEAR)
    cam = np.maximum(cam, 0) 
    cam = cam / cam.max()

    jetcam = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    jetcam = cv2.cvtColor(jetcam, cv2.COLOR_BGR2RGB) 
    jetcam = (np.float32(jetcam) + x / 2) 

    return jetcam, score, class_idx


def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)

    test_files = fetch_filelist(_DATA_DIR)
    category_map = parse_category_map('labels.txt')
    
    g = tf.Graph()
    with g.as_default():
        model = create_model()
        model.summary()
        latest = tf.train.latest_checkpoint(_CHECKPOINT_DIR)
        model.load_weights(latest)

        for f in test_files:
            dst_dir = os.path.join(_DST_DIR, os.path.basename(os.path.dirname(f)))
            if os.path.isdir(dst_dir) is False:
                os.makedirs(dst_dir)
            dst_filepath = os.path.join(dst_dir, os.path.basename(f))
            x = img_to_array(load_img(f, target_size=(224,224)))
            array_to_img(x)
            image, score, class_idx = grad_cam(model, x, 'conv_pw_13_relu')
            cam = array_to_img(image)
            save_img(dst_filepath, cam)
            score_filepath = dst_filepath.replace('.jpg', '.txt')
            category_name = category_map[class_idx]
            with open(score_filepath, 'w', encoding='utf-8') as w:
                w.write(category_name + ':' + str(score))
                    

if __name__ == '__main__':
    main()
