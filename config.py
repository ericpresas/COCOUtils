# Configuration for COCO dataset reducer

INPUT_ANNS_FILE_PATH = "resources/instances_val2017.json"
OUTPUT_ANNS_FILE_PATH = "resources/new_instances_val2017.json"


REDUCED_DATASET_PARAMS = {
    "num_classes": 20,
    "max_samples_class": 100
}

# Configuration Pascal -> COCO conversor

IMAGES_PATH = "/datasets/trainset"
ANNOTATIONS_PATH = "/datasets/trainset"
OUTPUT_COVERSION_PATH = "resources/pascal_to_coco.json"

# Configuration Grapes dataset

GRAPES_DATASET = {
    "path": "/datasets/grapes_dataset",
    "output_ann_path": "/datasets/grapes_annotations"
}