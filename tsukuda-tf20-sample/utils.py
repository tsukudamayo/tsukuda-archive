import os
from typing import Iterator


def parse_category_map(labels_txt):
    with open(labels_txt, 'r', encoding='utf-8') as r:
        lines = r.readlines()
        category_map = {int(line.split(':')[0]): line.split(':')[1].rstrip() for line in lines}

    return category_map


def fetch_filelist(filepath: str) -> Iterator[str]:
    if os.path.isdir(filepath) is False:
        yield filepath
    else:
        itr = os.listdir(filepath)
        for i in itr:
            nextpath = os.path.join(filepath, i)
            yield from fetch_filelist(nextpath)


def process_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    pImg = tf.keras.applications.mobilenet.preprocess_input(img_array)

    return pImg
