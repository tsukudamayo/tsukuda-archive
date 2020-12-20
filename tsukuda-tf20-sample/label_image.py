from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np
from PIL import Image
import tensorflow as tf
import tflite_runtime.interpreter as tflite


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--image',
        default='./16class_random_train_data_labeled/images/val/cl/cl_fore_46.jpg',
        help='image to classified')
    parser.add_argument(
        '-m',
        '--model_file',
        default='./converted_model.tflite',
        help='.tflite model to be executed')
    parser.add_argument(
        '-l',
        '--label_file',
        default='./labels.txt',
        help='name of file containg labels')
    parser.add_argument(
        '--input_mean',
        default=127.5, type=float,
        help='input_mean')
    parser.add_argument(
        '--input_std',
        default=127.5, type=float,
        help='input standard deviation')
    args = parser.parse_args()


    interpreter = tf.lite.Interpreter(model_path=args.model_file)
    interpreter.allocate_tensors()
    print(interpreter.allocate_tensors())
    
    input_details = interpreter.get_input_details()
    print('input_details')
    print(input_details)

    output_details = interpreter.get_output_details()
    print('output_details')
    print(output_details)


