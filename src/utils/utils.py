from pycocotools.coco import COCO
import random
import json


def load_ann_file(path):
    return COCO(path)


def save_ann_file(annotations, path):
    with open(path, 'w') as outfile:
        json.dump(annotations, outfile, indent=4)


def random_sample(_list, num_samples):
    if len(_list) < num_samples:
        num_samples = len(_list)
    return random.sample(_list, num_samples)
