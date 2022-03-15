import glob
import os
import xml.etree.ElementTree as ET
import re
import src.utils.utils as utils


class PascalToCOCO(object):
    def __init__(self, images_path, annotations_path, cat_list, offset_ann_id=1, annotator=None):
        self.images_path = images_path
        self.annotations_path = annotations_path
        labels_ids = list(range(1, len(cat_list) + 1))
        self.categories_map = dict(zip(cat_list, labels_ids))
        self.offset_ann_id = offset_ann_id
        self.annotator = annotator

    def convert(self, output_path=None, save_file=True):
        output_json_dict = {
            "images": [],
            "type": "instances",
            "annotations": [],
            "categories": []
        }
        os.chdir(self.annotations_path)
        bnd_id = self.offset_ann_id
        for ann_file in glob.glob("*.xml"):
            ann_path = f"{self.annotations_path}/{ann_file}"
            ann_tree = ET.parse(ann_path)
            ann_root = ann_tree.getroot()
            img_info = self.get_image_info(ann_root)

            img_id = img_info['id']
            output_json_dict['images'].append(img_info)

            for obj in ann_root.findall('object'):
                ann = self.get_coco_annotation_from_obj(obj=obj, label2id=self.categories_map)
                ann.update({'image_id': img_id, 'id': bnd_id})
                output_json_dict['annotations'].append(ann)
                bnd_id = bnd_id + 1

        for label, label_id in self.categories_map.items():
            category_info = {'supercategory': 'none', 'id': label_id, 'name': label}
            output_json_dict['categories'].append(category_info)

        if save_file:
            utils.save_ann_file(output_json_dict, output_path)

        return output_json_dict

    def get_image_info(self, annotation_root, extract_num_from_imgid=True):
        filename = annotation_root.findtext('filename')
        img_name = os.path.basename(filename)
        img_id = os.path.splitext(img_name)[0]
        if extract_num_from_imgid and isinstance(img_id, str):
            img_id = int(re.findall(r'\d+', img_id)[0])

        size = annotation_root.find('size')
        width = int(size.findtext('width'))
        height = int(size.findtext('height'))

        composed_filename = f"{self.annotator}/{filename}" if self.annotator is not None else filename

        image_info = {
            'file_name': composed_filename,
            'path': f"{self.images_path}/{filename}",
            'height': height,
            'width': width,
            'id': img_id
        }
        if self.annotator is not None:
            image_info['annotator'] = self.annotator

        return image_info

    @staticmethod
    def get_coco_annotation_from_obj(obj, label2id):
        label = obj.findtext('name')
        assert label in label2id, f"Error: {label} is not in label2id !"
        category_id = label2id[label]
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.findtext('xmin')) - 1
        ymin = int(bndbox.findtext('ymin')) - 1
        xmax = int(bndbox.findtext('xmax'))
        ymax = int(bndbox.findtext('ymax'))
        assert xmax > xmin and ymax > ymin, f"Box size error !: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}"
        o_width = xmax - xmin
        o_height = ymax - ymin
        ann = {
            'area': o_width * o_height,
            'iscrowd': 0,
            'bbox': [xmin, ymin, o_width, o_height],
            'category_id': category_id,
            'ignore': 0,
            'segmentation': []  # This script is not for segmentation
        }
        return ann