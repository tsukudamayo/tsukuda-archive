from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import pathlib
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.preprocessing import image

from models import create_model
from utils import process_image


_DATA_DIR = './data/'


epochs = 15
BATCH_SIZE = 10
IMG_HEIGHT = 224
IMG_WIDTH = 224


def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20, 20))
    axes = axes.flatten()
    for img, ax in zip(images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join('sample_dir', 'sample_img.jpg'))
    print('save image')

    return


def output_labels_txt(class_names: List):
    with open('labels.txt', 'w', encoding='utf-8') as w:
        for i, c in enumerate(class_names):
            w.write(str(i) + ':' + c + '\n')

    return


def plot_loss(epochs_range, acc, val_acc, loss, val_loss):
    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.savefig(os.path.join('sample_dir', 'result.jpg'))

    return


def plot_metrics(history):
    metrics = ['loss', 'roc', 'precision', 'recall', 'pr']
    for n, metric in enumerate(metrics):
        name = metric.replace('_', ' ').capitalize()
        plt.subplot(3,2,n+1)
        plt.plot(
            history.epoch,
            history.history[metric],
            label='Train'
        )
        plt.plot(
            history.epoch,
            history.history['val_'+metric],
            linestyle='--',
            label='Val'
        )
        plt.xlabel('Epoch')
        plt.ylabel(name)
        if metric == 'loss':
            plt.ylim([0, plt.ylim()[1]])
        elif metric == 'roc' or metric == 'pr':
            plt.ylim([0.8, 1])
        else:
            plt.ylim([0,1])
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join('sample_dir', 'metrics.jpg'))


def main():
    # ----------
    # Load data
    # ----------
    train_dir = os.path.join(_DATA_DIR, 'train')
    validation_dir = os.path.join(_DATA_DIR, 'val')
    data_dir_pathlib = pathlib.Path(_DATA_DIR)
    total_train = len(list(data_dir_pathlib.glob('train/*/*.jpg')))
    total_val = len(list(data_dir_pathlib.glob('*val/*/*.jpg')))
    print('total_train')
    print(total_train)
    print('total_val')
    print(total_val)

    CLASS_NAMES = np.array([d for d in os.listdir(train_dir)])
    print('CLASS_NAMES')
    print(CLASS_NAMES)
    output_labels_txt(CLASS_NAMES)

    # ---------------------
    # Data Augumentation 
    # ---------------------
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

    train_data_gen = image_generator.flow_from_directory(
        directory=train_dir,
        batch_size=BATCH_SIZE,
        shuffle=True,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        classes=list(CLASS_NAMES)
    )
        
    val_data_gen = image_generator.flow_from_directory(
        batch_size=BATCH_SIZE,
        directory=validation_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        classes=list(CLASS_NAMES)
    )

    if os.path.isdir('sample_dir') is False:
        os.makedirs('sample_dir')

    sample_training_images, _ = next(train_data_gen)

    plotImages(sample_training_images[:5])

    checkpoint_path = 'training_1/cp.ckpt'
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_weights_only=True,
        verbose=1
    )

    model = create_model()

    model.summary()
        
    summary_writer = tf.summary.create_file_writer('summaries')
    with summary_writer.as_default():
      tf.summary.scalar('loss', 0.1, step=1)


    history = model.fit_generator(
        train_data_gen,
        steps_per_epoch=total_train,
        epochs=epochs,
        validation_data=val_data_gen,
        validation_steps=total_val,
        callbacks=[cp_callback]
    )

    tf.saved_model.save(model, 'saved_model/1/')

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(epochs)

    plot_loss(epochs_range, acc, val_acc, loss, val_loss)
    plot_metrics(history)

    test_img_path = '/workspace/16class_random_train_data_labeled/images/val/cl/cl_fore_27.jpg'
    pImg = process_image(test_img_path)
    print('prediction')
    prediction = model.predict(pImg)
    print(prediction)
    print(prediction.shape)
    print('CLASS_NAME')
    print(CLASS_NAMES)
    print(np.argmax(prediction))
    print(np.max(prediction))
    print(CLASS_NAMES[np.argmax(prediction)])


if __name__ == '__main__':
    main()
