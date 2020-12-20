import os

import tensorflow as tf

import sklearn
from sklearn.metrics import confusion_matrix
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

from utils import fetch_filelist
from models import create_model


_DATA_DIR = './data/16class_random_train_data/val'
_CHECKPOINT_DIR = './training_1'
mpl.rcParams['figure.figsize'] = (20, 15)


def plot_cm(labels, predictions, p=0.5):
    cm = confusion_matrix(labels, predictions)
    plt.figure(figsize(5,5))
    sns.heatmap(cm)
    plt.title('Confusion matrix')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.savefig('confusion_matrix.jpg')

    print('Legitimate Transactions Detected (True Negatives): ', cm[0][0])
    print('Legitimate Transactions Incorrectly Detected (False Positives): ', cm[0][1])
    print('Fraudulent Transactions Missed (False Negatives): ', cm[1][0])
    print('Fraudulent Transactions Detected (True Positives): ', cm[1][1])
    print('Total Fraudulent Transactions: ', np.sum(cm[1]))

    return


def separate_filename_and_label(file_list):
    filepath_list, label_list = [], []
    
    for f in file_list:
        filepath_list.append(f)
        label_list.append(os.path.basename(os.path.dirname(f)))

    return filepath_list, label_list


def read_class_name(labes_txt):
    with open('labels.txt', 'r', encoding='utf-8') as r:
        lines = r.readlines()
        class_names = [f.split(':')[1].rstrip() for f in lines]

    return class_names


def main():
    test_files = fetch_filelist(_DATA_DIR)
    filepath_list, label_list = separate_filename_and_label(test_files)
    print(filepath_list)
    print(label_list)
    CLASS_NAMES = read_class_name('labels.txt')

    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    val_data_gen = image_generator.flow_from_directory(
        batch_size=10,
        directory=_DATA_DIR,
        target_size=(224, 224),
        classes=list(CLASS_NAMES)
    )
    
    model = create_model()
    model.summary()
    latest = tf.train.latest_checkpoint(_CHECKPOINT_DIR)
    model.load_weights(latest)

    test_predictions = model.predict(
        val_data_gen,
    )
    print(test_predictions)

    results = model.evaluate(
        val_data_gen,
    )
    print(results)
    for name, value in zip(model.metrics_names, results):
        print(name, ': ', value)
    print()

    print(label_list)
    plot_cm(label_list, test_predictions)


if __name__ == '__main__':
    main()
