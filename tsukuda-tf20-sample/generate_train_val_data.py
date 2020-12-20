import os
import random
import shutil
from typing import Callable, Iterator, List

from utils import fetch_filelist


_RANDOM_SEED = 1234
_DATA_DIR = './data/16class_random_train_data'
_TEST_DATA_RATE = 0.1


def category_generator(filelist: Callable[[str], Iterator[str]]) -> List:
    return set([define_category_name(f) for f in filelist if f.find('.jpg') >= 0])


def define_category_name(filepath: str) -> str:
    return os.path.basename(filepath).split('_')[0]


def filter_by_category(filelist: Callable[[str], Iterator[str]], category: str) -> List:
    return filter(lambda x: os.path.basename(x).find(category + '_') == 0, filelist)


def split_train_val(random_data: List, category: str, validation_rate=_TEST_DATA_RATE) -> dict:
    print('category')
    print(category)
    
    num_of_val_data = int(len(random_data) * validation_rate)

    print('num_of_val_data')
    print(num_of_val_data)

    train_data = random_data[:(-num_of_val_data)]
    val_data = random_data[(-num_of_val_data):]

    print('train_data : ', len(train_data))
    print('val_data : ', len(val_data))

    return {'category': category, 'train': train_data, 'val': val_data}


def copy_file_to_train_val_directory(train_val_data_map: dict, train_dir: str, val_dir: str):
    for data in train_val_data_map:
        category = data['category']
        for f in data['train']:
            dstpath = os.path.join(train_dir, category, os.path.basename(f))
            shutil.copy2(f, dstpath)
        for f in data['val']:
            dstpath = os.path.join(val_dir, category, os.path.basename(f))
            shutil.copy2(f, dstpath)


def main():
    random.seed(_RANDOM_SEED)
    all_file_list = fetch_filelist(_DATA_DIR)

    category_list = category_generator(fetch_filelist(_DATA_DIR))
    print('category_list')
    print(category_list)
    print(len(category_list))

    train_dir = os.path.join(_DATA_DIR, 'train')
    val_dir = os.path.join(_DATA_DIR, 'val')
    if os.path.isdir(train_dir) is True:
        shutil.rmtree(train_dir)
    if os.path.isdir(val_dir) is True:
        shutil.rmtree(val_dir)

    for di in [train_dir, val_dir]:
        for dj in category_list:
            if os.path.isdir(os.path.join(di, dj)) is False:
                os.makedirs(os.path.join(di, dj))
            else:
                pass

    category_file_map = {c: list(filter_by_category(fetch_filelist(_DATA_DIR), c)) for c in category_list }
    print('category_file_map')
    print(category_file_map)

    random_data_map = {c: random.sample(list(category_file_map[c]), len(list(category_file_map[c])))
                                        for c in category_list}

    train_val_data_map = [split_train_val(random_data_map[c], c) for c in category_list]

    copy_file_to_train_val_directory(train_val_data_map, train_dir, val_dir)


if __name__ == '__main__':
    main()
