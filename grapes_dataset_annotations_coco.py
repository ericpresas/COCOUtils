from src.lib.pascal_to_coco import PascalToCOCO
import src.utils.utils as utils
import config
import glob
import matplotlib.pyplot as plt
from PIL import Image
import random


def empty_output():
    return {
        "images": [],
        "type": "instances",
        "annotations": [],
        "categories": []
    }


def splitter(_list, percentages):
    data = _list.copy()
    random.shuffle(data)
    num_samples_train = int((len(data)+1)*percentages['train'])
    num_samples_val = int((len(data) + 1) * percentages['val'])
    num_samples_test = len(data) - num_samples_train - num_samples_val

    samples_train = data[:num_samples_train]
    samples_val = data[num_samples_train: num_samples_val + num_samples_train]
    samples_test = data[-num_samples_test:]

    return {
        "train": samples_train,
        "val": samples_val,
        "test": samples_test
    }


def showimg(coco, img_id, title):
    img_info = coco.loadImgs(img_id)[0]
    image = Image.open(img_info['path'])
    annIds = coco.getAnnIds(imgIds=img_info['id'], iscrowd=None)
    anns = coco.loadAnns(annIds)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(image)
    coco.showAnns(anns, draw_bbox=True)
    for i, ann in enumerate(anns):
        ax.text(anns[i]['bbox'][0], anns[i]['bbox'][1], anns[i]['id'], style='italic',
                bbox={'facecolor': 'white', 'alpha': 0, 'pad': 2}, size=7)

    fig.suptitle(f"{title} - {img_info['id']}")
    plt.show()


def main():
    categories = ["grapes"]

    directories = glob.glob(f"{config.GRAPES_DATASET['path']}/*")

    valid_anns = [0, 4, 5, 6]

    output_json_dict = {
        "all": empty_output(),
        "train": empty_output(),
        "val": empty_output(),
        "test": empty_output()
    }

    output_json_dict_no_anns = empty_output()

    directories.sort()
    last_annotation = 0
    for directory in directories:
        i = int(directory.split('/')[-1])
        pascal_to_coco = PascalToCOCO(
            images_path=directory,
            annotations_path=directory,
            cat_list=categories,
            offset_ann_id=last_annotation + 1,
            annotator=i
        )
        annotator_json_dict = pascal_to_coco.convert(output_path=f"{config.GRAPES_DATASET['output_ann_path']}/grapes_anns_{i}.json")
        last_annotation += len(annotator_json_dict['annotations'])
        output_json_dict['all']['categories'] = annotator_json_dict['categories']
        output_json_dict['train']['categories'] = annotator_json_dict['categories']
        output_json_dict['val']['categories'] = annotator_json_dict['categories']
        output_json_dict['test']['categories'] = annotator_json_dict['categories']
        output_json_dict_no_anns['categories'] = annotator_json_dict['categories']
        """output_json_dict['images'] += annotator_json_dict['images']
        output_json_dict['annotations'] += annotator_json_dict['annotations']
        output_json_dict['categories'] = annotator_json_dict['categories']"""

    ann_imgs_ids = {}
    all_coco_tools = {}

    ann_imgs_ids_no_anns = {}
    all_coco_tools_no_anns = {}
    for directory in directories:
        i = int(directory.split('/')[-1])
        coco_tools = utils.load_ann_file(path=f"{config.GRAPES_DATASET['output_ann_path']}/grapes_anns_{i}.json")
        if i in valid_anns:
            all_coco_tools[i] = coco_tools
            ann_imgs_ids[i] = coco_tools.getImgIds()
        else:
            all_coco_tools_no_anns[i] = coco_tools
            ann_imgs_ids_no_anns[i] = coco_tools.getImgIds()

    per_splits = {
        "train": 0.6,
        "val": 0.3,
        "test": 0.1
    }
    img_ids_all = list(set.intersection(*map(set, [items for key, items in ann_imgs_ids.items()])))
    for directory in directories:
        i = int(directory.split('/')[-1])
        if i in valid_anns:
            if i != 0:
                ann_imgs_ids[i] = list(set(ann_imgs_ids[i]) - set(img_ids_all))

            imgs_info_annotator = all_coco_tools[i].loadImgs(ids=ann_imgs_ids[i])
            anns_ids = all_coco_tools[i].getAnnIds(imgIds=ann_imgs_ids[i])
            anns_info = all_coco_tools[i].loadAnns(ids=anns_ids)
            output_json_dict['all']['images'] += imgs_info_annotator
            output_json_dict['all']['annotations'] += anns_info

            splits = splitter(ann_imgs_ids[i], per_splits)
            for stage, per in per_splits.items():
                imgs_info_annotator = all_coco_tools[i].loadImgs(ids=splits[stage])
                anns_ids = all_coco_tools[i].getAnnIds(imgIds=splits[stage])
                anns_info = all_coco_tools[i].loadAnns(ids=anns_ids)
                output_json_dict[stage]['images'] += imgs_info_annotator
                output_json_dict[stage]['annotations'] += anns_info

        else:
            ann_imgs_ids_no_anns[i] = list(set(ann_imgs_ids_no_anns[i]) - set(img_ids_all))
            imgs_info_annotator = all_coco_tools_no_anns[i].loadImgs(ids=ann_imgs_ids_no_anns[i])
            output_json_dict_no_anns['images'] += imgs_info_annotator

    utils.save_ann_file(output_json_dict['all'], f"{config.GRAPES_DATASET['output_ann_path']}/grapes_all_anns.json")
    utils.save_ann_file(output_json_dict['train'], f"{config.GRAPES_DATASET['output_ann_path']}/grapes_train_anns.json")
    utils.save_ann_file(output_json_dict['val'], f"{config.GRAPES_DATASET['output_ann_path']}/grapes_val_anns.json")
    utils.save_ann_file(output_json_dict['test'], f"{config.GRAPES_DATASET['output_ann_path']}/grapes_test_anns.json")
    utils.save_ann_file(output_json_dict_no_anns, f"{config.GRAPES_DATASET['output_ann_path']}/grapes_no_anns.json")

    """for idx_img in range(len(img_ids_all)):
        for annotator, coco_ann_tool in all_coco_tools.items():
            name = f"Annotator {annotator}"
            showimg(coco_ann_tool, img_ids_all[idx_img], name)"""


if __name__ == "__main__":
    main()