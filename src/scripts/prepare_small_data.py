import requests
from multiprocessing.pool import ThreadPool
import subprocess

import argparse
import os
import shutil
import logging
import sys
import glob
from pathlib import Path
from typing import Dict, Any, Set


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(name)s  %(levelname)s: %(message)s',
    datefmt='%y-%b-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)

train_path = "/Users/nguyendangquang/master/DeepLearning/deep-metric-learning/data/TsinghuaDogs/TrainAndValList/train.lst"
val_path = "/Users/nguyendangquang/master/DeepLearning/deep-metric-learning/data/TsinghuaDogs/TrainAndValList/validation.lst"

DATA_DIR = Path("data/")
TSINGHUA_DOGS_ROOT_DIR = str(DATA_DIR / "New_TsinghuaDogs")

def make_small_set(train_path: str, val_path: str):
    with open(train_path, 'r') as f:
        train_images = f.readlines()
    with open(val_path, 'r') as f:
        val_images = f.readlines()

    count = 0
    train_lst = []
    val_lst = []

    for ind in range(len(train_images)-1):
        dir_name = os.path.dirname(train_images[ind])
        next_dir_name = os.path.dirname(train_images[ind + 1])
        if dir_name == next_dir_name:
            if count < 5:
                count += 1
                train_lst.append(train_images[ind])
            else:
                continue
        else:
            count = 1
            train_lst.append(train_images[ind])
    
    for ind in range(len(val_images)-1):
        dir_name = os.path.dirname(val_images[ind])
        next_dir_name = os.path.dirname(val_images[ind + 1])
        if dir_name == next_dir_name:
            if count < 5:
                count += 1
                val_lst.append(val_images[ind])
            else:
                continue
        else:
            count = 1
            val_lst.append(val_images[ind])
    with open("data/train_small.txt", "w") as f:
        for image in train_lst:
            f.write(image)
    with open("data/val_small.txt", "w") as f:
        for image in val_lst:
            f.write(image)        

def make_small_label(label_path: str, new_dir: str, true_dir: str):
    for dir in os.listdir(label_path):
        dir_path = os.path.join(label_path, dir)
        try:
            for label in os.listdir(dir_path):
                label = label + ".xml"
                label_p = os.path.join(true_dir, dir, label)
                dest_p = os.path.join(new_dir, dir, label)
                # print(dest_p)
                os.makedirs(dest_p, exist_ok=True)

                logging.info(f"Copying {label_p} to {dest_p}")
                shutil.copy(label_p, dest_p)
            # sys.exit()
        except:
            continue


def main():
    # make_small_set(train_path, val_path)
    label_train_path = "data/New_TsinghuaDogs/train"
    label_val_path = "data/New_TsinghuaDogs/val"
    true_dir = "data/TsinghuaDogs/High-Annotations"
    new_dir = "data/New_TsinghuaDogs/High-Annotations"
    make_small_label(label_train_path, new_dir, true_dir)
    make_small_label(label_val_path, new_dir, true_dir)

if __name__ == "__main__":
    main()