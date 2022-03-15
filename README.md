# COCOUtils

Useful tools to work with COCO annotations.

## COCO annotations reducer

Define the number of classes and number of images per class to define a reduced version of a coco type annotations.

### Usage

- Define input/output annotations file path in `config.py.

```python
INPUT_ANNS_FILE_PATH = "resources/instances_val2017.json"
OUTPUT_ANNS_FILE_PATH = "resources/new_instances_val2017.json"
```

- Define `num_classes` and `max_samples_class` in `config.py`.

```python
REDUCED_DATASET_PARAMS = {
    "num_classes": 20,
    "max_samples_class": 100
}
```

Simple usage of `COCOReducer` class by calling `reduce()` method. See `reduce_coco.py`.

## Pacal to COCO conversor

Asumes that images and annotations are in the same directory. Converts pascal annotations `.xml` files to coco format `.json`.

### Usage
 - Define images, annotations and output paths in `config.py`.
 ```python
IMAGES_PATH = "/datasets/trainset"
ANNOTATIONS_PATH = "/datasets/trainset"
OUTPUT_COVERSION_PATH = "resources/pascal_to_coco.json"
```

Simple usage of `PascalToCOCO` class by calling `convert()` method. See `pascal_to_coco.py`

Support for datasets with various annotators using `annotator` and `offset_ann_id` parameters. The config variables are defined in `config.py`.
```python
GRAPES_DATASET = {
    "path": "/datasets/grapes_dataset",
    "output_ann_path": "/datasets/grapes_annotations"
}
```

See an example of custom dataset with various annotators splitted in folders `0,1,2,3,4,5,6,7`. See `grapes_dataset_annotations.py`.
Outputs produced are:

- `grapes_anns_x`: Annotation file for a single annotator.
- `grapes_all_ans`: Annotation file for all annotators.
- `grapes_no_ans`: Annotation file for invalid annotators (note that annotations will come as empty lists).
- `grapes_{split}_anns`: Split of all annotators file (train/val/test).